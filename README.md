# UguuBot

* Easy to use wrapper
* Intuitive configuration
* Fully controlled from IRC
* Fully compatable with existing skybot plugins
* Easily extendable
  * Thorough documentation
  * Cross-platform
* Muti-threaded, efficient
  * Automatic reloading
  * Little boilerplate

### Dependencies
Taigabot requires Python 2.7 and its developed on Ubuntu 18.04.

You can read more about the dependencies in [dependencies.md](dependencies.md)

The following system dependencies are needed (`apt install`):

    python2.7 python-pip git python2.7-dev build-essential libxml2-dev libxslt1-dev

and these python dependencies are required (__already in requirements.txt__: `pip2 install -r requirements.txt`):

    httplib2==0.7.5 BeautifulSoup4==4.1.3 lxml==3.3.6 requests

you can install the additional dependencies for more plugins:

    pip2 install -r requirements_extra.txt

It is strongly recommended to install dependencies in a virtual environment.

With all of these, the bot will run and almost all plugins will work.

#### Other dependencies

Some plugins require other python packages, more information can be found on [dependencies.md § details](dependencies.md#details).

The system packages `daemon` or `screen` are recomended for the launcher to run optimally.

### Installation
On Ubuntu:

    sudo apt-get install python2.7 python-pip git
    sudo apt-get install python2.7-dev build-essential libxml2-dev libxslt1-dev
    git clone https://github.com/inexist3nce/Taigabot.git
    cd Taigabot
    pip2 install virtualenv
    python2 -m virtualenv venv
    source venv/bin/activate
    pip2 install -r requirements.txt
    pip2 install -r requirements_extra.txt
    cp config.default config
    vim config
    python2 bot.py

### Run

Once you have installed the required dependencies, there are two ways you can run the bot:

#### Launcher

**Note:** Due to some issues with the launcher we recommend you run the bot manually as detailed below.

**Note:** If migrating from an older version please look in the modules/Admin.py at the migrate_old_db command. MAKE SURE TO USE A COPY OF THE ORIGINAL DB.

The launcher will start the bot as a background process, and allow the bot to close and restart itself. This is only supported on unix-like machines (not Windows).

For the launcher to work properly, install `screen`, or `daemon` (daemon is recommended):

`apt-get install screen`

`apt-get install daemon`

Once you have installed either `screen` or `daemon`, run the start command:

`./uguubot start`

It will generate a default config for you.  Once you have edited the config, run it again with the same command:

`./uguubot start`

This will start up your bot as a background process. To stop it, use `./uguubot stop`.)

#### Manually

To manually run the bot and get console output, run it with:

`python bot.py`

(note: running the bot without the launcher breaks the start and restart commands)

## License

UguuBot is **licensed** under the **GPL v3** license. The terms are as follows.

    UguuBot/DEV
    Copyright © 2013-2013 Infinity - <https://github.com/infinitylabs/UguuBot>
    Copyright © 2011-2012 Luke Rogers / ClouDev - <[cloudev.github.com](http://cloudev.github.com)>

    UguuBot is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    UguuBot is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with UguuBot.  If not, see <http://www.gnu.org/licenses/>.

## Contact

Need to contact someone? Head on over to #uguubot at irc.rizon.net for assistance or any other needs.
