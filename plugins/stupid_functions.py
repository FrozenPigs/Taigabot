from util import hook
@hook.regex(r'^(same)$')
def same(inp):
    "<word>? -- Shows what data is associated with <word>."
    return 'same'

@hook.regex(r'^(TETETE)$')
@hook.regex(r'^(tetete)$')
def same(inp, nick=None):
    "<word>? -- Shows what data is associated with <word>."
    return 'tetete %s%s%s' % (nick, nick, nick)