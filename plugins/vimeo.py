# vimeo info plugin by ine (2020)
from util import hook, timeformat
from utilities import request

# the v2 api is deprecated and only does simple public video information
# new one is at https://api.vimeo.com/videos/{id} but needs a key


def info(id):
    info = request.get_json('http://vimeo.com/api/v2/video/' + id + '.json')

    if not info or len(info) == 0:
        return

    title = info[0]['title']
    length = timeformat.format_time(info[0]["duration"], simple=True)
    likes = format(info[0]['stats_number_of_likes'], ',d')
    views = format(info[0]['stats_number_of_plays'], ',d')
    uploader = info[0]['user_name']
    upload_date = info[0]['upload_date']

    output = []
    output.append('\x02' + title + '\x02')
    output.append('length \x02' + length + '\x02')
    output.append(likes + ' likes')
    output.append(views + ' views')
    output.append('\x02' + uploader + '\x02 on ' + upload_date)

    return ' - '.join(output)


@hook.regex(r'https?://player\.vimeo\.com/video/([0-9]+)')
@hook.regex(r'https?://vimeo\.com/([0-9]+)/?')
def vimeo_url(match):
    """<vimeo url> -- automatically returns information on the Vimeo video at <url>"""
    output = info(match.group(1))

    if not output:
        return

    return output
