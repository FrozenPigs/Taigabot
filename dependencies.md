## about this fork
taigabot is ancient software that runs on an unmantained python version. the existing uguubot instructions no longer work.

the main piece of software, the uguu irc bot, is more than 10 years old and some dependencies can't be found on repositories (ubuntu, pip or even github), so they've been bundled with the bot in this repository.

taiga runs only on python 2. its unmantained, but its too much work to port everything to python 3.

this is an attempt to get taiga properly documented for running on ubuntu 18.04, and eventually other distros.

the bare minimum is listed below.

## system dependencies (ubuntu)
- python2.7
  - its python.
- python-pip
  - package manager, particularly useful for installing very old versions
- git
  - allows for cloning/updating the bot
  - alternative  - wget github's auto-generated .zip
- build-essential python2.7-dev
  - everything needed to compile, plus python headers
- libxml2-dev libxslt1-dev
  - libraries that need to be installed to compile lxml

## python dependencies
- virtualenv
  - helps keep the trash contained in a single place
- lxml
  - works on 3.3.6
  - not sure what this library does, but its used to parse html
  - taiga needs 3.1beta1, but it doesn't compile anymore, so you can install 3.3.6.
  - as of 2020-05, versions older than 3.2 don't compile because of some long error i didnt feel like reading.
  - https://pypi.org/project/lxml/3.3.6/
- beautifulsoap
  - needs 3.2.x and 4.1.3
  - used for scraping websites.
  - taiga uses both bs3 and bs4. install 3.2.2 and 4.1.3.
  - https://pypi.org/project/BeautifulSoup/3.2.2/
  - https://pypi.org/project/beautifulsoup4/4.1.3/
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

    pip2 install lxml==3.3.6
    pip2 install BeautifulSoup==3.2.2 beautifulsoup4==4.1.3
    pip2 install httplib2==0.7.5

make your own configuration:

    cp config.default config
    vi config

run the bot, finally:

    python2 bot.py
