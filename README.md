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

### Installation
Taigabot runs only on Python 2.7. See [install.md](install.md#instructions) for [ubuntu](install.md#ubuntu) or [alpine](install.md#alpine) instructions.

The biggest hurdle is `lxml` which needs a compiler and a bunch of libraries.

#### Other dependencies
Some commands require extra python packages, more information can be found on [install.md § specific dependencies](install.md#specific-dependencies).

Some commands also require API keys, 

The system packages `daemon` or `screen` are recomended for the launcher to run optimally.


### Run
Once you have installed the required dependencies, you need to create a config file:

    cp config.default config
    vim config
    python2 bot.py

There are two ways you can run the bot:

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
