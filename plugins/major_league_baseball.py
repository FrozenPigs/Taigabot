#!/usr/bin/env python2
# Copyright (C) 2020  Anthony DeDominic <adedomin@gmail.com>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from util import hook
from utilities.request import get_json
from time import strftime

MLB_DEPRECATED_API = 'http://gd2.mlb.com/components/game/mlb'
API_DATEFMT = "year_%Y/month_%m/day_%d"
OUTGAME_STRING = '\x02{}\x02 {} ({}{}) \x02{}\x02 {}'


@hook.command('mlb', autohelp=False)
def mlb(inp):
    api_base = '{}/{}'.format(MLB_DEPRECATED_API,
                              strftime(API_DATEFMT))
    api_string = '{}/grid.json'.format(api_base)

    try:
        games_today = get_json(api_string)
    except Exception:
        return 'Failed to get games today (Note: gd2 API *is* deprecated).'

    if not isinstance(games_today, dict):
        return 'Failed to get games today: grid.json is not an object.'
    
    try:
        games = games_today['data']['games']['game']
    except KeyError:
        return 'No Games Today.'

    if not isinstance(games, list):
        games = [games]

    output = []
    for game in games:
        away_team = game.get('away_name_abbrev', '')
        away_score = game.get('away_score', '0')
        if away_score == '':
            away_score = 0

        home_team = game.get('home_name_abbrev', '')
        home_score = game.get('home_score', '0')
        if home_score == '':
            home_score = 0
        
        inning = game.get('top_inning', '-')
        if inning == 'Y':
            inning = '\x0303^\x03'
        elif inning == 'N':
            inning = '\x0302v\x03'
        else:
            inning = '-'
        
        game_status = game.get('status', '')
        if 'Pre' == game_status[0:3]:
            game_status = game.get('event_time', 'P')
            inning = ''
        elif 'Final' == game_status:
            game_status = 'F'
            inning = ''
        else:
            game_status = game.get('inning', '0')

        outstring = OUTGAME_STRING.format(away_team, away_score,
                                          game_status, inning,
                                          home_team, home_score)

        if inp.lower() == away_team.lower() or inp.lower() == home_team.lower():
            if inning != '':
                details = get_more_detail(api_base, game.get('id', 'null'))
                outstring += ' Count: {}-{}'.format(details['balls'],
                                                    details['strikes'])
                outstring += ' Outs: {}'.format(details['outs'])
                outstring += ' OnBase: {}'.format(details['onbase'])
                outstring += ' Pitcher: {}'.format(details['pitcher'])
                outstring += ' Batter: {}'.format(details['batter'])
            return outstring
        else:
            output.append(outstring)

    if len(output) == 0:
        return 'No Games Today.'
    else:
        return 'Times in EST - ' + ' :: '.join(output)


def get_more_detail(api_path, gid):
    api_gid = gid.replace('/', '_').replace('-', '_')
    detail_api_base = '{}/{}'.format(api_path, api_gid)
    detail_linescore = '{}/linescore.json'.format(detail_api_base)

    try:
        linescore = get_json(detail_linescore)
    except Exception:
        return {'balls':'unkn',
                'strikes':'unkn',
                'outs':'unkn',
                'onbase':'unkn',
                'pitcher':'unkn',
                'batter':'unkn'}

    # count
    balls = linescore.get('balls', 'unkn')
    strikes = linescore.get('strikes', 'unkn')
    outs = linescore.get('outs', 'unkn')

    runners_onbase = linescore.get('runner_on_base_status', 'unkn')

    pitcher = linescore.get('current_pitcher', dict()).get('last_name', 'unkn')
    batter = linescore.get('current_batter', dict()).get('last_name', 'unkn')

    # TODO: events (requires XML parser

    return {'balls':balls,
            'strikes':strikes,
            'outs':outs,
            'onbase':runners_onbase,
            'pitcher':pitcher,
            'batter':batter}
