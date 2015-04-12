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

### Requirements

Linux packages needed for install: python, python-dev, libenchant-dev, libenchant1c2a, libxslt-dev, libxml2-dev.

UguuBot runs on **Python** *2.7.x*. It is developed on **Ubuntu** *12.04* with **Python** *2.7.3*.

It **requires the Python module** `lXML`, and `Enchant` is needed for the spellcheck plugin.

The programs `daemon` or `screen` are recomended for the launcher to run optimally.

**Windows** users: Windows compatibility with the launcher and some plugins is **broken** (such as ping), but we do intend to add it.³

### Install required Linux packages 
    
    Install python, python-dev, libenchant-dev, libenchant1c2a, libxslt-dev, libxml2-dev
    
Before you can run the bot, you need to install a few Python dependencies. These can be installed with `pip` (The Python package manager):

    [sudo] pip install -r requirements.txt

#### How to install `pip`

    curl -O http://python-distribute.org/distribute_setup.py # or download with your browser on windows
    python distribute_setup.py
    easy_install pip

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

On Windows you can usually just double-click the `bot.py` file to start the bot, as long as you have Python installed correctly.

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

## Notes

³ eventually
