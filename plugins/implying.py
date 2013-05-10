from util import hook, http
import re

def get_image_result(html,num):
    link = html.xpath("//table[@class='images_table']//a/@href")[num]
    image = http.unquote(re.search('.+?imgurl=(.+)&imgrefurl.+', link).group(1))
    return image

@hook.regex(r'^\> ?(.+\.tiff)')
@hook.regex(r'^\> ?(.+\.TIFF)')
@hook.regex(r'^\> ?(.+\.png)')
@hook.regex(r'^\> ?(.+\.PNG)')
@hook.regex(r'^\> ?(.+\.jpg)')
@hook.regex(r'^\> ?(.+\.JPG)')
@hook.regex(r'^\> ?(.+\.jpeg)')
@hook.regex(r'^\> ?(.+\.JPEG)')
@hook.regex(r'^\> ?(.+\.gif)')
@hook.regex(r'^\> ?(.+\.GIF)')
@hook.command('mfw')
def implying(inp):
    ">imagename.gif -- Returns first Image result."
    num = 0
    is_active = False
    try: search = inp.group(1)
    except: search = inp
    url = "https://www.google.com/search?q=%s&hl=en&sa=G&gbv=2&tbm=isch&sout=1" % search.replace(' ','_').replace("'",'')
    html = http.get_html(url)

    try:
        while not is_active and num < 6: #check if link is dead, if so get the next image
            image = get_image_result(html,num)
            is_active = http.is_active(image)
            num = num + 1
    except IndexError:
        return 'No image found.'

    return '\x033\x02>%s\x02\x03 %s' % (search, image.decode('utf-8'))