import pystache


bold_template = pystache.parse(unicode("<strong>{{string}}</strong>"))
italic_template = pystache.parse(unicode("<em>{{string}}</em>"))
code_template = pystache.parse(unicode("<code>{{string}}</code>"))
code_block_template = "<div class='highlight test_log'>%s</div>"
code_block_template = code_block_template % ("<pre>%s</pre>")
code_block_template = code_block_template % ("<code>%s</code>")
code_block_template = code_block_template % ("{{&string}}")
code_block_template = pystache.parse(unicode(code_block_template))
link_template = pystache.parse(unicode("<a href='{{href}}' target='_blank'>{{text}}</a>"))

def bold(string):
    return pystache.render(bold_template, {'string':string})

def italic(string):
    return pystache.render(italic_template, {'string':string})

def code(string):
    return pystache.render(code_template, {'string':string})

def code_block(string):
    return pystache.render(code_block_template, {'string':string})

def link(text, href):
    return pystache.render(link_template, {'text':text, 'href':href})

def breakline():
    return "<br/>"

def parse(string):
    return pystache.parse(unicode(string))

def render(template, view):
    return pystache.render(template, view)

def build_output(view, status, get_template, output):

    briefing_template, message_template = get_template()
    briefing = render(briefing_template, view)
    message = render(message_template, view)
    return status, briefing, message, output
