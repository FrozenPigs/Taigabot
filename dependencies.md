# taigabot dependencies
taigabot is ancient software that runs on an unmantained python version. the existing uguubot instructions no longer work.

the main piece of software, the uguu irc bot, is more than 10 years old and some dependencies can't be found on repositories (ubuntu, pip or even github), so they've been bundled with the bot in this repository.

taiga runs only on python 2. its unmantained, but its too much work to port everything to python 3.

this is an attempt to get taiga properly documented for running on ubuntu 18.04, and eventually other distros.

## system dependencies (ubuntu)
- python2.7
- python-pip
- build-essential
  - everything needed to compile lxml
- python2.7-dev libxml2-dev libxslt1-dev
  - headers/libraries needed to compile lxml

optionally `git` to clone this repo, but you can download it however you want.

## python dependencies
you __need__ these to run the bot

- virtualenv
  - helps keep the trash contained. please use this.
- lxml
  - works on 3.3.6 (originally used 3.1beta1, doesnt work anymore)
  - used to parse html
  - as of 2020-05, versions older than 3.2 don't compile because of some long error i didnt feel like reading.
  - https://pypi.org/project/lxml/3.3.6/
  - __required__ to work
- requests
  - 2.23.0 works fine
  - __required__ to work

with the aforementioned requirements, taigabot is guaranteed to run and these core plugins will work:
- core_admin_channel.py
- core_admin_global.py
- core_ctcp.py
- core_misc.py
- core_sieve.py
- core_user.py
- log.py
- all internal `util` plugins

## python dependencies for plugins
plugins need these. they're "optional" but the bot is __useless without plugins__.

- beautifulsoap
  - needs 3.2.1 and 4.1.3, works with 4.9.0
  - used for scraping websites.
  - taiga uses both bs3 and bs4. install 3.2.1 and 4.9.0
  - https://pypi.org/project/BeautifulSoup/3.2.1/
  - https://pypi.org/project/beautifulsoup4/4.9.0/
- yql
  - needs custom version (0.7.5?)
  - some helper for yahoo query language by stuart colville.
  - this version isnt the same as the one on pip, so it's been bundled with the bot in the "lib/" folder.
  - depends on httplib2 and a specific oauth (read below)
- httplib2
  - needs 0.7.5
  - dependency of yql
  - https://pypi.org/project/httplib2/0.7.5/
- oauth
  - needs custom version (a modified 1.5.211?)
  - dependency of yql
  - this is an unknown version, its not "oauth", "oauth2" or "oauth2.3" (from pip).
  - it's been bundled with the bot, in the "lib/" folder
- tweepy
  - needs 3.5.0
  - *optional*: not used by a lot of plugins
  - https://pypi.org/project/tweepy/3.5.0/
- simplejson
  - needs 2.0.7
  - *optional*: not used by a lot of plugins
  - https://pypi.org/project/simplejson/2.0.7/

## instructions
basic system requirements:

    apt-get install python2.7 python-pip git

for compiling:

    apt-get install python2.7-dev build-essential libxml2-dev libxslt1-dev

get the bot and make a virtual env

    git clone https://github.com/inexist3nce/Taigabot.git
    cd Taigabot
    pip2 install virtualenv
    python2 -m virtualenv venv
    source venv/bin/activate

install dependencies:

    pip2 install -r requirements.txt

make your own configuration:

    cp config.default config
    vi config

run the bot, finally:

    python2 bot.py


## details
to get the plugin working, the listed python dependencies are needed

- amazon, bash, debt, dictionary, drama, fmylife
  - bs4
  - requests (in util.request)
- wolframalpha
  - urllib2
  - simplejson
  - [!] util.http
- furry, translate
  - requests (in util.request)

### plugins with no external dependencies
- choose
- coin
- countdown
- dice
- heartbleed
- potato
- smileys
