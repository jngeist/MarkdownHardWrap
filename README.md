# MarkdownHardWrap #

MarkdownHardWrap (hereafter MHW) is a simple plugin for adding hard line breaks to Markdown/MultiMarkdown documents in a syntax-friendly way.

## What it does ##

### List items ###

MHW preserves hanging indents for list items.

Input: 

    *   Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aliquam hendrerit mi posuere lectus. Vestibulum enim wisi, viverra nec, fringilla in, laoreet vitae, risus.

Standard hard wrap:

    *   Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aliquam hendrerit
    *   mi posuere lectus. Vestibulum enim wisi, viverra nec, fringilla in, laoreet
    *   vitae, risus.

MHW:

    *   Donec sit amet nisl. Aliquam semper ipsum sit amet velit. Suspendisse id
        sem consectetuer libero luctus adipiscing.

This is particularly useful for proper alignment of multi-paragraph list items, and for lazy `ol`s:

    1.  Aliquam erat volutpat. Donec massa augue, faucibus non sollicitudin a,
        venenatis fermentum metus. Ut blandit dignissim metus eu vulputate. Duis
        aliquam tempus velit, eu viverra risus eleifend ac. Sed pellentesque
        cursus auctor. Vestibulum id lacus id justo vestibulum tristique vitae ut
        mauris. Vivamus ut velit non purus dictum consequat. In non metus ac nibh
        interdum malesuada. Aliquam tempor scelerisque posuere. Phasellus
        consequat scelerisque lectus, vitae aliquet sem imperdiet sit amet.

        Pellentesque sed mauris ante. Vivamus at neque massa, vel eleifend lacus.
        Aenean commodo fermentum libero tempor pellentesque. Class aptent taciti
        sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos.
        Duis suscipit congue tempor. Integer nec augue nibh, ut convallis velit.
        Nam ut augue orci, et ullamcorper quam. Nam dictum, libero eget congue
        vehicula, tortor neque accumsan risus, in pharetra felis est eu ligula.
        Sed sit amet erat sit amet ligula accumsan elementum.

    -   Morbi sem neque, eleifend id gravida nec, ultrices nec diam. Aenean
        iaculis pellentesque nisl, ut porta massa bibendum id. Etiam vitae sem
        orci, nec venenatis urna. Duis non libero tellus. Curabitur quis diam
        quam, sit amet venenatis est. Aliquam erat volutpat. Nunc lacinia porta
        nibh quis tincidunt. Phasellus vel nisl velit, id cursus justo. In hac
        habitasse platea dictumst. Ut ac urna ut leo pharetra volutpat. Cras
        mollis convallis ligula, et iaculis nisl ullamcorper euismod. Etiam diam
        dolor, bibendum quis rhoncus ac, pharetra ut sem. Sed lobortis blandit
        urna, at molestie sem facilisis pellentesque. Quisque eget nunc turpis.
        Pellentesque laoreet leo ac libero venenatis placerat. Nunc et nibh id
        justo ullamcorper ullamcorper.

### Initial emphasis

MHW correctly detects emphasis/strength at the beginning of paragraphs.

Input:

    *Lorem ipsum dolor sit amet,* consectetur adipiscing elit. Integer nec odio. Praesent libero. Sed cursus ante dapibus diam. 

    **Sed nisi.** Nulla quis sem at nibh elementum imperdiet. Duis sagittis ipsum. Praesent mauris. Fusce nec tellus sed augue semper porta. 

Standard hard wrap:

    *Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer nec odio.
    *Praesent libero. Sed cursus ante dapibus diam.

    **Sed nisi. Nulla quis sem at nibh elementum imperdiet. Duis sagittis ipsum.
    **Praesent mauris. Fusce nec tellus sed augue semper porta.

MHW:

    *Lorem ipsum dolor sit amet,* consectetur adipiscing elit. Integer nec odio.
    Praesent libero. Sed cursus ante dapibus diam.

    **Sed nisi.** Nulla quis sem at nibh elementum imperdiet. Duis sagittis ipsum.
    Praesent mauris. Fusce nec tellus sed augue semper porta.

### Avoids problems with combined soft/hard wrap.

While MHW provides a `hard_wrap_lines` setting to automatically hard wrap paragraphs as needed, there may be some cases where a mix of longer and hard-wrapped lines is desirable (as in this particular [Github-flavored Markdown][] document.) Leaving `word_wrap` enabled with the standard hard wrap command will sometimes result in lines breaking twice, such that the newline character (and sometimes the word preceding it) appears *after* the soft wrap. MHW avoids this problem by providing a separate `hard_wrap_width` setting which allows you to add a character or two of padding to your `wrap_width` setting, such that this problem is avoided.


 [Github-flavored Markdown]: http://github.github.com/github-flavored-markdown/

### Not yet implemented ###

At this point, I haven't sorted out dealing with nested Markdown within blockquotes. 

Input:

    > -  Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aliquam hendrerit mi posuere lectus. Vestibulum enim wisi, viverra nec, fringilla in, laoreet vitae, risus. 

Output:

    > -  Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aliquam
    > hendrerit mi posuere lectus. Vestibulum enim wisi, viverra nec, fringilla
    > in, laoreet vitae, risus.

Desired:

    > -  Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aliquam
    >    hendrerit mi posuere lectus. Vestibulum enim wisi, viverra nec, 
    >    fringilla in, laoreet vitae, risus.

This is finicky enough that I don't much care, but it is an existing shortfall.
