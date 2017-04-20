from util import hook, http
import re
import math
import json
import time
import requests
from time import sleep
from threading import *
from collections import deque
from bs4 import BeautifulSoup

def get_json_data(url, sleep_time=0):
    """Returns a json data object from a given url."""
    # Respect 4chan's rule of at most 1 JSON request per second
    sleep(sleep_time)
    try:
        response = requests.get(url)
        if response.status_code == 404:
            print ("url {} 404".format(url))
            return None
        json_data = json.loads(response.text.encode())
        return json_data
    except Exception as e:
        print ("url: {}".format(url))
        print (e)
        raise


def sanitise(string):
    """Strips a string of all non-alphanumeric characters"""
    return re.sub(r"[^a-zA-Z0-9 ]", "", string)


def get_title(url):
    soup = http.get_soup(url)

    if '#' in url:
        postid = url.split('#')[1]
        post = soup.find('div', {'id': postid})
    else:
        post = soup.find('div', {'class': 'opContainer'})
    
    comment = http.process_text(post.find('blockquote', {'class': 'postMessage'}).renderContents().strip())
    return u"{} - {}".format(url, comment) #


def sprunge(data):
    sprunge_data = {"sprunge": data}
    response = requests.post("http://sprunge.us", data=sprunge_data)
    message = response.text.encode().strip('\n')
    return message


def search_thread(results_deque, thread_num, search_specifics):
    """
    Searches every post in thread thread_num on board board for the
    string provided. Returns a list of matching post numbers.
    """
    json_url = "https://a.4cdn.org/{0}/thread/{1}.json".format(search_specifics["board"], thread_num)
    thread_json = get_json_data(json_url)

    if thread_json is not None:
        re_search = None
        for post in thread_json["posts"]:
            user_text = "".join([post[s] for s in search_specifics["sections"] if s in post.keys()])
            re_search = re.search(search_specifics["string"], user_text, re.UNICODE + re.IGNORECASE)
            if re_search is not None:
                results_deque.append("{0}#p{1}".format(thread_num, post["no"]))


def search_page(results_deque, page, search_specifics):
    """Will be run by the threading module. Searches all the 
    4chan threads on a page and adds matching results to synchronised queue"""
    for thread in page['threads']:
        user_text = "".join([thread[s] for s in search_specifics["sections"] if s in thread.keys()])
        if re.search(search_specifics["string"], user_text, re.UNICODE + re.IGNORECASE) is not None:
            results_deque.append(thread["no"])


def process_results(board, string, results_deque):
    """Process the resulting data of a search and present it"""
    max_num_urls_displayed = 6
    max_num_urls_fetch = 20
    board = sanitise(board)
    message = ""
    urllist = []
    post_template = "https://boards.4chan.org/{0}/thread/{1}"
    if len(results_deque) <= 0:
        message = "No results for {0}".format(string)
    elif len(results_deque) > max_num_urls_fetch:
        #message = "Too many results for {0}".format(string)
        urls = [post_template.format(board, post_num) for post_num in results_deque]
        #message = " ".join(urllist[:max_num_urls_displayed])
        message = sprunge('\n'.join(urls))
    else:
        urls = [post_template.format(board, post_num) for post_num in results_deque]
        if len(urls) > max_num_urls_displayed:
            for url in urls:
                title =  get_title(url)
                urllist.append("{}".format(title).encode('ascii', 'ignore'))
            message = sprunge('\n\n'.join(urllist))
        else:
            for url in urls:
                title =  get_title(url)
                urllist.append("{}".format(title[:int(120)].encode('ascii', 'ignore')))
            message = " ".join(urllist[:max_num_urls_displayed])

    return message


@hook.command("4chan")
@hook.command   
def catalog(inp):
    "catalog <board> <regex> -- Search all OP posts on the catalog of a board, and return matching results"
    thread_join_timeout_seconds = 10
    results_deque = deque()

    inp = inp.split(" ")
    board = inp[0]
    string = (" ".join(inp[1:])).strip()

    json_url = "https://a.4cdn.org/{0}/catalog.json".format(board)
    sections = ["com", "name", "trip", "email", "sub", "filename"]
    catalog_json = get_json_data(json_url)
    search_specifics = {"sections" : sections, "board" : board, "string" : string}
    thread_pool = []

    for page in catalog_json:
        t = Thread(None, target=search_page, args=(results_deque, page, search_specifics))
        t.start()
        thread_pool.append(t)

    for _thread in thread_pool:
        if _thread.is_alive():
            _thread.join(float(thread_join_timeout_seconds))

    results = process_results(board, string, results_deque)
    return ("%s" % (results))


@hook.command   
def board(inp):
    "board <board> <regex> -- Search all the posts on a board and return matching results"
    thread_join_timeout_seconds = 10
    results_deque = deque()

    inp = inp.split(" ")
    board = inp[0]
    string = (" ".join(inp[1:]))

    json_url = "https://a.4cdn.org/{0}/threads.json".format(board)
    sections = ["com", "name", "trip", "email", "sub", "filename"]
    threads_json = get_json_data(json_url)
    search_specifics = {"sections" : sections, "board" : board, "string" : string}
    thread_pool = []

    for page in threads_json:
        for thread in page["threads"]:
            t = Thread(None, target=search_thread, args=(results_deque, thread["no"], search_specifics))
            t.start()
            thread_pool.append(t)
    
    for _thread in thread_pool:
        if _thread.is_alive():
            _thread.join(float(thread_join_timeout_seconds))

    results = process_results(board, string, results_deque)
    return ("%s" % (results))

@hook.command(autohelp=False)
def bs(inp, reply=None):
    "bs -- Returns current battlestation threads on /g/"
    return catalog("g battlestation")


@hook.command(autohelp=False)
def desktops(inp, reply=None):
    "desktop -- Returns current desktop threads on /g/"
    return catalog("g desktop thread")

@hook.command(autohelp=False)
def britbong(inp, reply=None):
    return catalog("pol britbong")
