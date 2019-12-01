# IMDb lookup plugin by Ghetto Wizard (2011).

from util import hook, http
import re

import datetime
import urllib2
import urllib
from bs4 import BeautifulSoup
from urllib2 import URLError
from zipfile import ZipFile
from cStringIO import StringIO

from lxml import etree
from util import hook, http, web

base_url = "http://thetvdb.com/api/"
api_key = "469B73127CA0C411"

# http://thetvdb.com/api/GetSeries.php?seriesname=clannad


def get_zipped_xml(*args, **kwargs):
    try:
        path = kwargs.pop("path")
    except KeyError:
        raise KeyError("must specify a path for the zipped file to be read")
    zip_buffer = StringIO(http.get(*args, **kwargs))
    return etree.parse(ZipFile(zip_buffer, "r").open(path))


def get_series_info(seriesname):
    res = {"error": None, "ended": False, "episodes": None, "name": None}
    # http://thetvdb.com/wiki/index.php/API:GetSeries
    try:
        query = http.get_xml(
            base_url + 'GetSeries.php', seriesname=seriesname)
    except URLError:
        res["error"] = "error contacting thetvdb.com"
        return res
    series_id = ""
    try:
        series_id = query.xpath('//id/text()')
    except:
        print "Failed"

    if not series_id:
        result = "\x02Could not find show:\x02 %s" % seriesname
    else:
        series_name = query.xpath('//SeriesName/text()')[0]
        overview = query.xpath('//Overview/text()')[0]
        firstaired = query.xpath('//FirstAired/text()')[0]
        #imdb_id = query.xpath('//IMDB_ID/text()')[0]
        #imdb_url = web.isgd("http://www.imdb.com/title/%s" % imdb_id)
        tvdb_url = web.isgd("http://thetvdb.com/?tab=series&id=%s" %
                            series_id[0])
        status = tv_next(seriesname)
        result = '\x02%s\x02 (%s) \x02-\x02 \x02%s\x02 - [%s] - %s' % (
            series_name, firstaired, status, tvdb_url, overview)

    return result


def get_episodes_for_series(seriesname):
    res = {"error": None, "ended": False, "episodes": None, "name": None}
    # http://thetvdb.com/wiki/index.php/API:GetSeries
    try:
        query = http.get_xml(
            base_url + 'GetSeries.php', seriesname=seriesname)
    except URLError:
        res["error"] = "error contacting thetvdb.com"
        return res

    series_id = query.xpath('//seriesid/text()')

    if not series_id:
        res["error"] = "unknown tv series (using www.thetvdb.com)"
        return res

    series_id = series_id[0]

    try:
        series = get_zipped_xml(
            base_url + '%s/series/%s/all/en.zip' % (api_key, series_id),
            path="en.xml")
    except URLError:
        res["error"] = "error contacting thetvdb.com"
        return res

    series_name = series.xpath('//SeriesName/text()')[0]

    if series.xpath('//Status/text()')[0] == 'Ended':
        res["ended"] = True

    res["episodes"] = series.xpath('//Episode')
    res["name"] = series_name
    return res


def get_episode_info(episode):
    first_aired = episode.findtext("FirstAired")

    try:
        airdate = datetime.date(*map(int, first_aired.split('-')))
    except (ValueError, TypeError):
        return None

    episode_num = "S%02dE%02d" % (int(episode.findtext("SeasonNumber")),
                                  int(episode.findtext("EpisodeNumber")))

    episode_name = episode.findtext("EpisodeName")
    # in the event of an unannounced episode title, users either leave the
    # field out (None) or fill it with TBA
    if episode_name == "TBA":
        episode_name = None

    episode_desc = '%s' % episode_num
    if episode_name:
        episode_desc += ' - %s' % episode_name
    return (first_aired, airdate, episode_desc)


@hook.command
@hook.command('show')
@hook.command('series')
def tv(inp):
    ".tv <series> -- get info for the <series>"
    return get_series_info(inp)


@hook.command('next')
@hook.command
def tv_next(inp):
    ".tv_next <series> -- get the next episode of <series>"
    episodes = get_episodes_for_series(inp)

    if episodes["error"]:
        return episodes["error"]

    series_name = episodes["name"]
    ended = episodes["ended"]
    episodes = episodes["episodes"]

    if ended:
        return "%s has ended." % series_name

    next_eps = []
    today = datetime.date.today()

    for episode in reversed(episodes):
        ep_info = get_episode_info(episode)

        if ep_info is None:
            continue

        (first_aired, airdate, episode_desc) = ep_info

        if airdate > today:
            next_eps = ['%s (%s)' % (first_aired, episode_desc)]
        elif airdate == today:
            next_eps = ['Today (%s)' % episode_desc] + next_eps
        else:
            #we're iterating in reverse order with newest episodes last
            #so, as soon as we're past today, break out of loop
            break

    if not next_eps:
        return "No new episodes scheduled for %s" % series_name

    if len(next_eps) == 1:
        #return "The next episode of %s airs %s" % (series_name, next_eps[0])
        return "Next episode: %s" % (next_eps[0])
    else:
        next_eps = ', '.join(next_eps)
        return "Airs: %s" % (next_eps)


@hook.command
@hook.command('tv_prev')
@hook.command('prev')
@hook.command('last')
def tv_last(inp):
    ".tv_last <series> -- gets the most recently aired episode of <series>"
    episodes = get_episodes_for_series(inp)

    if episodes["error"]:
        return episodes["error"]

    series_name = episodes["name"]
    ended = episodes["ended"]
    episodes = episodes["episodes"]

    prev_ep = None
    today = datetime.date.today()

    for episode in reversed(episodes):
        ep_info = get_episode_info(episode)

        if ep_info is None:
            continue

        (first_aired, airdate, episode_desc) = ep_info

        if airdate < today:
            #iterating in reverse order, so the first episode encountered
            #before today was the most recently aired
            prev_ep = '%s (%s)' % (first_aired, episode_desc)
            break

    if not prev_ep:
        return "There are no previously aired episodes for %s" % series_name
    if ended:
        return '%s ended. The last episode aired %s' % (series_name, prev_ep)
    return "The last episode of %s aired %s" % (series_name, prev_ep)


id_re = re.compile("tt\d+")


@hook.command('movie')
@hook.command
def imdb(inp):
    "imdb <movie> -- Gets information about <movie> from IMDb."
    base_url = 'http://www.imdb.com'
    search = base_url + "/find?q={}&s=all".format(
        urllib.quote(inp.encode('utf-8')))
    response = urllib2.urlopen(search)
    soup = BeautifulSoup(response.read(), 'lxml')
    result = base_url + soup.find_all(
        'table', 'findList')[0].find_all('td')[1].find_all(
            'a', href=True)[0]['href']
    response = urllib2.urlopen(result)
    soup = BeautifulSoup(response.read())
    title = soup.find_all('h1')[1].get_text()[0:-8].strip()
    year = soup.find_all('h1')[1].find_all('span')[0].get_text().strip()
    genres = soup.find_all('div', 'subtext')[0].find_all('span', 'itemprop')
    tmp = []
    if len(genres) >= 2:
        for i in genres:
            tmp.append(i.get_text())
    else:
        tmp = genres[0].get_text()
    genres = ', '.join(tmp)
    plot = soup.find_all('div', 'summary_text')[0].get_text().strip()
    runtime = soup.find_all('div', 'subtext')[0].find_all('time')[0].get_text(
    ).strip()
    score = soup.find_all('div', 'ratingValue')[0].get_text().strip()
    votes = soup.find_all('span', 'small')[0].get_text().strip()
    return u"\x02{}\x02 {} ({}): {} {}. {} with {} votes. {}".format(
        title, year, genres, plot, runtime, score, votes,
        result.split('?')[0])

    #strip = inp.strip()

    #if id_re.match(strip):
    #    content = http.get_json("http://www.omdbapi.com/?apikey={}&".format('f293592e'), i=strip)
    #else:
    #    content = http.get_json("http://www.omdbapi.com/?apikey={}&".format('f293592e'), t=strip)

    #if content.get('Error', None) == 'Movie not found!':
    #    return 'Movie not found!'
    #elif content['Response'] == 'True':
    #    content['URL'] = 'http://www.imdb.com/title/%(imdbID)s' % content

    #    out = '\x02%(Title)s\x02 (%(Year)s) (%(Genre)s): %(Plot)s'
    #    if content['Runtime'] != 'N/A':
    #        out += ' \x02%(Runtime)s\x02.'
    #    if content['imdbRating'] != 'N/A' and content['imdbVotes'] != 'N/A':
    #        out += ' \x02%(imdbRating)s/10\x02 with \x02%(imdbVotes)s\x02' \
    #               ' votes.'
    #    out += ' %(URL)s'
    #    return out % content
    #else:
    #    return 'Unknown error.'


api_root = 'http://api.rottentomatoes.com/api/public/v1.0/'
movie_search_url = api_root + 'movies.json'
movie_reviews_url = api_root + 'movies/%s/reviews.json'


@hook.command('rt')
@hook.command
def rottentomatoes(inp, bot=None):
    '.rt <title> -- gets ratings for <title> from Rotten Tomatoes'

    api_key = bot.config.get("api_keys", {}).get("rottentomatoes", None)
    if not api_key:
        return "error: no api key set"

    results = http.get_json(movie_search_url, q=inp, apikey=api_key)
    if results['total'] == 0:
        return 'no results'

    movie = results['movies'][0]
    title = movie['title']
    id = movie['id']
    critics_score = movie['ratings']['critics_score']
    audience_score = movie['ratings']['audience_score']
    url = movie['links']['alternate']

    if critics_score == -1:
        return

    reviews = http.get_json(
        movie_reviews_url % id, apikey=api_key, review_type='all')
    review_count = reviews['total']

    fresh = critics_score * review_count / 100
    rotten = review_count - fresh

    return u"%s - critics: \x02%d%%\x02 (%d\u2191/%d\u2193) audience: \x02%d%%\x02 - %s" % (
        title, critics_score, fresh, rotten, audience_score, url)
