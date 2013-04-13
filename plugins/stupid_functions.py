from util import hook
@hook.regex(r'^(same)$')
def same(inp, say=None, db=None, bot=None, me=None, conn=None, input=None):
    "<word>? -- Shows what data is associated with <word>."
    return 'same'