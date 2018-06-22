from util import hook, http, web
import json
import requests

url = "http://www.genius.com/search?q={}"


@hook.command
def lyrics(inp, reply=None, bot=None):
    """lyrics <search> - Search genius.com for song lyrics"""
    
    base_url = "http://api.genius.com"
    headers = {'Authorization': bot.config['api_keys']['genius']}
    search_url = base_url + "/search"
    song_title = inp
    params = {'q': song_title}
    response = requests.get(search_url, params=params, headers=headers)
    return json.loads(response.text)['response']['hits'][0]['result']['url']

    #inp = '+'.join(inp.split())
    #soup = http.get_soup(url.format(inp))
    #print soup
    #result = soup.findAll('a', {'class': 'mini_card'})
    #print 'penis'
    #print result
    #reply(result[0]['href'])
    # if "pastelyrics" in inp:
    #     dopaste = True
    #     inp = inp.replace("pastelyrics", "").strip()
    # else:
    #     dopaste = False
    # soup = http.get_soup(url + inp.replace(" ", "+"))
    # if "Try to compose less restrictive search query" in soup.find('div', {'id': 'inn'}).text:
    #     return "No results. Check spelling."
    # div = None
    # for i in soup.findAll('div', {'class': 'sen'}):
    #     if "/lyrics/" in i.find('a')['href']:
    #         div = i
    #         break
    # if div:
    #     title = div.find('a').text
    #     link = div.find('a')['href']
    #     if dopaste:
    #         newsoup = http.get_soup(link)
    #         try:
    #             lyrics = newsoup.find('div', {'style': 'margin-left:10px;margin-right:10px;'}).text.strip()
    #             pasteurl = " " + web.haste(lyrics)
    #         except Exception as e:
    #             pasteurl = " (\x02Unable to paste lyrics\x02 [{}])".format(str(e))
    #     else:
    #         pasteurl = ""
    #     artist = div.find('b').text.title()
    #     lyricsum = div.find('div').text
    #     if "\r\n" in lyricsum.strip():
    #         lyricsum = " / ".join(lyricsum.strip().split("\r\n")[0:4])  # truncate, format
    #     else:
    #         lyricsum = " / ".join(lyricsum.strip().split("\n")[0:4])  # truncate, format
    #     return u"\x02{}\x02 by \x02{}\x02 {}{} - {}".format(title, artist, web.try_isgd(link), pasteurl,
    #                                                          lyricsum[:-3])
    # else:
    #     return "No song results. " + url + inp.replace(" ", "+")
