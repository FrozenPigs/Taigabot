from util import hook,http  

time = 3600
touhou_list = {}

def gather_subsection(section, key):
    if section.depth > 1:
        print "Subsection " + section.name


@hook.command(channeladminonly=True)
def check_touhou(inp,chan=None,bot=None):
    #if channel[chan]:

    channels = bot.channelconfig.walk(gather_subsection)
    for channel in channels:
        print channel

    return

    chan_url = http.quote('{channel|%s}/1' % '#pantsumen') #str(chan)
    url='http://booru.touhouradio.com/post/list/%s' % chan_url

    try: html = http.get_html(url)
    except ValueError: return None

    firstimage = html.xpath("//span[@class='thumb']//img/@src")[0]

    try:
        if firstimage in touhou_list[chan]:
            return "New Activity on TouhouRadio!"
    except: 
        pass
    
    touhou_list[chan] = firstimage
    print touhou_list[chan]
    

@hook.command('touhou',channeladminonly=True)
def touhoucheck(inp, conn=None, chan=None, notice=None, bot=None):
    "touhou [channel] <enable|disable> -- Check touhouradio.com for new updates."
    inp = inp.lower()
    if inp[0][0] == "#": 
        chan = inp.split()[0]
        inp = inp.replace(chan,'').strip()
    channel = chan.lower()
    
    if 'enable' in inp or 'on' in inp: setting=True
    elif 'disable' in inp or 'off' in inp: setting=False
    else: return __help__

    try: bot.channelconfig[channel]
    except: bot.channelconfig[channel] = {}

    bot.channelconfig[channel]['touhou_check'] = setting
    if setting: notice("Touhou checking is now enabled.")
    else: notice("Touhou checking is now disabled.")

    bot.channelconfig.write()
    return