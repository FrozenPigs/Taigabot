# taigabot dependencies
taigabot is ancient software that runs on an unmantained python version. the existing uguubot instructions no longer work.

the main piece of software, the irc bot, is more than 12 years old and some dependencies can't be found on repositories (ubuntu, pip or even github), so they've been bundled with the bot in this repository.

taiga runs only on python 2.7.

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
you __need__ these to run the bot.

    pip install -r requirements.txt

- virtualenv
  - helps keep the trash contained. please use this.
- lxml
  - works on 3.3.6
  - used to parse html and xml
  - https://pypi.org/project/lxml/3.3.6/
  - __required__
- requests
  - 2.23.0 works fine
  - __required__
- beautifulsoup4
  - 4.9.0 works fine
  - __required__

with the aforementioned requirements, taigabot is guaranteed to run and these core plugins will work:
- core_admin_channel.py
- core_admin_global.py
- core_ctcp.py
- core_misc.py
- core_sieve.py
- core_user.py
- log.py
- all internal `util` plugins

## plugins
plugins need some dependencies. they're "optional" but the bot is __useless without plugins__.

    pip2 install -r requirements_extra.txt

you can find details below.

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
    pip2 install -r requirements_extra.txt

make your own configuration:

    cp config.default config
    vi config

run the bot, finally:

    python2 bot.py


## details
if `bs4` and `requests` are installed, these plugins will work:
- amazon
- bash
- debt
- dictionary
- distro
- drama
- fmylife
- religion
- validate
- wordoftheday

if `requests` is installed, these plugins will work:
- furry
- translate
- kernel
- urbandict
- vimeo

to get these plugins working, you need to install these specific dependencies:
- weather
  - urllib
  - requests
  - pytz
  - geopy

### plugins with no external dependencies
- choose
- coin
- countdown
- dice
- heartbleed
- potato
- smileys
- wolframalpha

### api keys
these plugins need an api key on the `config` file
| plugin       | key name           | where to find |
|--------------|--------------------|---------------|
| religion     | `"english_bible"`  | [here](https://api.esv.org/docs/) |
| weather      | `"darksky"`        | not possible to get anymore |
| wolframalpha | `"wolframalpha"`   | [here](https://products.wolframalpha.com/api/) |
| google       | `"google"`         | - |
| google       | `"google2"`        | - |
| google       | `"googleimage"`    | - |
