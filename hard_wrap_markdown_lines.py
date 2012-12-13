import sublime
import sublime_plugin
import paragraph as par
import textwrap
import string
import re


def get_width(view):
    """
    Utility function used to determine at what line width to wrap lines in
    MarkdownHardWrap.
    """

    width = 0
    for key in ["hard_wrap_width", "wrap_width"]:
        if width == 0 and view.settings().get(key):
            try:
                width = int(view.settings().get(key))
            except TypeError:
                pass

    if width == 0 and view.settings().get("rulers"):
        # try and guess the wrap width from the ruler, if any
        try:
            width = int(view.settings().get("rulers")[0])
        except ValueError:
            pass
        except TypeError:
            pass

    if width == 0:
        width = 78

    return width


class MarkdownWrapLinesCommand(par.WrapLinesCommand):
    """
    Command for adding hard line breaks to paragraphs in a Markdown-friendly
    way. Preserves indentation and Markdown syntax.
    """

    persistent_prefixes = re.compile("^\s*(>\s+)+")
    initial_prefixes = re.compile("^\s*([-*+]|\d+\.)?\s+")
    MARKER = u"\u200B"

    def extract_prefix(self, sr):
        lines = self.view.split_by_newlines(sr)

        if len(lines) == 0:
            return None

        lineone = self.view.substr(lines[0])
        prefix_match = self.persistent_prefixes.match(lineone)
        if prefix_match:
            prefix_type = 'persistent'
        else:
            prefix_match = self.initial_prefixes.match(lineone)
            prefix_type = 'initial'

        if not prefix_match:
            return None

        prefix = self.view.substr(sublime.Region(lines[0].begin(),
                                                 lines[0].begin() + prefix_match.end()))

        if prefix_type == 'persistent':
            for line in lines[1:]:
                if self.view.substr(sublime.Region(line.begin(),
                                                   line.begin() + len(prefix))) != prefix:
                    return None
            return (prefix, prefix)
        return (prefix, re.sub('.', ' ', prefix))

    def run(self, edit, width=0):
        width = get_width(self.view)
        settings = self.view.settings()
        # Make sure tabs are handled as per the current buffer
        tab_width = 8
        if settings.get("tab_size", False):
            try:
                tab_width = int(self.view.settings().get("tab_size"))
            except TypeError:
                pass

        if tab_width == 0:
            tab_width == 8

        paragraphs = []
        for s in self.view.sel():
            #self.view.insert(edit, s.begin(), self.MARKER)
            paragraphs.extend(
                par.all_paragraphs_intersecting_selection(self.view, s))

        if len(paragraphs) > 0:
            self.view.sel().clear()
            for p in paragraphs:
                self.view.sel().add(p)

            # This isn't an ideal way to do it, as we loose the position of the
            # cursor within the paragraph: hence why the paragraph is selected
            # at the end.
            for s in self.view.sel():
                wrapper = textwrap.TextWrapper()
                wrapper.expand_tabs = False
                wrapper.replace_whitespace = settings.get(
                    'replace_whitespace', True)
                wrapper.drop_whitespace = settings.get(
                    'drop_whitespace', True)
                wrapper.width = width
                prefix = self.extract_prefix(s)
                if prefix:
                    wrapper.initial_indent = prefix[0]
                    wrapper.subsequent_indent = prefix[1]
                    wrapper.width -= self.width_in_spaces(prefix, tab_width)

                if wrapper.width < 0:
                    continue

                txt = self.view.substr(s)
                if prefix:
                    txt = txt.replace(prefix[0], u"")

                txt = string.expandtabs(txt, tab_width)

                txt = wrapper.fill(txt) + u"\n"
                self.view.replace(edit, s, txt)

            # It's unhelpful to have the entire paragraph selected, just leave the
            # selection at the end
            ends = [s.end() - 1 for s in self.view.sel()]
            self.view.sel().clear()
            for pt in ends:
                self.view.sel().add(sublime.Region(pt))
            #sel = self.view.sel()
            #sel = self.view.find_all(self.MARKER)

#            sel.clear()
#            for c in self.view.find_all(self.MARKER):
#                sel.add(sublime.Region(c.begin(), c.begin()))
#                self.view.erase(edit, c)


class ToggleHardWrapCommand(sublime_plugin.WindowCommand):
    def run(self):
        self.window.run_command('toggle_setting', 'hard_wrap_lines')

    def is_visible(self):
        view = sublime.active_window().active_view()
        if view and 'Markdown' in view.settings().get('syntax'):
            print "Returning true"
            return True
        else:
            print "Returning false"
            return False

#class ToggleHardWrapCommand(sublime_plugin.TextCommand):
#    """
#    Toggles hard_wrap_lines setting for a given view.
#    Used to disable/enable hard wrap on a per-buffer basis.
#    """
#
#    def is_enabled(self):
#        return 'Markdown' in self.view.settings().get('syntax')
#
#    def run(self, *args):
#        s = self.view.settings()
#        enable = not s.get('hard_wrap_lines')
#        s.set('hard_wrap_lines', enable)


class AutoHardWrapLines(sublime_plugin.EventListener):
    """
    Automatically applies MarkdownWrapLinesCommand when the buffer
    is modified if the current line is longer than the wrap width.

    Can be enabled/disabled with the hard_wrap_lines setting.
    """

    TARGET_SETTINGS = ['hard_wrap_lines', 'hard_wrap_width',
                       'wrap_width', 'ruler']

    width = 0
    callback_is_registered = False

    def _add_callback(self, view):
        s = view.settings()
        for key in self.TARGET_SETTINGS:
            s.add_on_change(key, lambda: self._update_width(view))

    def active(self, view):
        s = view.settings()
        return (
            "Markdown" in s.get('syntax') and
            s.get('hard_wrap_lines')
        )

    def _update_width(self, view):
        self.width = get_width(view)

    def on_activated(self, view):
        s = view.settings()
        if s.has('syntax') and "Markdown" in s.get('syntax'):
            if not self.callback_is_registered:
                self._add_callback(view)

    def on_modified(self, view):
        if self.active(view):
            if len(view.sel()) == 1:
                s = view.sel()[0]
                llen = view.line(s).size()
                if llen > self.width:
                    view.run_command('markdown_wrap_lines')
