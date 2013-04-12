import inspect
import json
import os
from configobj import ConfigObj

def save(conf):
    json.dump(conf, open('config', 'w'), sort_keys=True, indent=2)

if not os.path.exists('config'):
    open('config', 'w').write(inspect.cleandoc(
        r'''
        {
          "connections":
          {
            "Rizon":
            {
              "server": "irc.rizon.net",
              "nick": "NewBot",
              "user": "user",
              "realname": "newbot",
              "nickserv_password": "",
              "channels": ["#devbot"],
              "invite_join": true,
              "auto_rejoin": false,
              "command_prefix": "."
            }
          },
          "disabled_plugins": [],
          "disabled_commands": [],
          "acls": {},
          "api_keys":
          {
            "geoip": "INSERT API KEY FROM ipinfodb.com HERE",
            "tvdb": "INSERT API KEY FROM thetvdb.com HERE",
            "bitly_user": "INSERT USERNAME FROM bitly.com HERE",
            "bitly_api": "INSERT API KEY FROM bitly.com HERE",
            "wolframalpha": "INSERT API KEY FROM wolframalpha.com HERE",
            "lastfm": "INSERT API KEY FROM lastfm HERE",
            "rottentomatoes": "INSERT API KEY FROM rottentomatoes HERE",
            "mc_user": "INSERT minecraft USERNAME HERE",
            "mc_pass": "INSERT minecraft PASSWORD HERE"
          },
          "plugins":
          {
            "factoids":
            {
              "prefix": false
            },
            "ignore":
            {
              "ignored": []
            }
          },
          "censored_strings":
          [
            "mypass",
            "mysecret"
          ],
          "admins": ["myname@myhost","myname@*some.host","mynick"]
        }''') + '\n')
    print "Config generated!"
    print "Please edit the config now!"
    print "Dont forget to pip -r requirements.txt!"
    sys.exit()

if not os.path.exists('channelconfig'): 
    ConfigObj('channelconfig',indent_type='\t', write_empty_values=False,create_empty=True)
    print "channelconfig generated!"

def config():
    # reload config from file if file has changed
    config_mtime = os.stat('config').st_mtime
    if bot._config_mtime != config_mtime:
        try:
            bot.config = json.load(open('config'))
            bot._config_mtime = config_mtime
        except ValueError, e:
            print 'error: malformed config', e

def channelconfig():
    # reload channelconfig from file if file has changed
    channelconfig_mtime = os.stat('channelconfig').st_mtime
    if bot._channelconfig_mtime != channelconfig_mtime:
        try:
            bot.channelconfig = ConfigObj('channelconfig',indent_type='\t', write_empty_values=False,create_empty=True)
            bot._channelconfig_mtime = channelconfig_mtime
        except ValueError, e:
            print 'error: malformed channelconfig', e

bot._config_mtime = 0
bot._channelconfig_mtime = 0


