from util import formatting, hook, http, web
import requests

NFL_REALTIME_API = 'http://static.nfl.com/liveupdate/scores/scores.json'
HOME = 'home'
AWAY = 'away'
ABBR = 'abbr'   # e.g. NE, DAL
SCORE = 'score'
T = 'T'         # Current score


def get_match_info(home, away):
    """ Returns teams and scores for a given match
    """

    home_abbr = home[ABBR]
    # If None type, turn it to 0
    home_score = home[SCORE][T] or 0
    away_abbr = away[ABBR]
    away_score = away[SCORE][T] or 0
    return "{} {} {} {}".format(home_abbr, home_score, away_abbr, away_score)


@hook.command(autohelp=False)
def nfl(inp):
    """nfl | nfl <team abbreviation> -- Returns all matchups for current week, or only for a specified team's matchup
    """

    # Get real time data
    data = requests.get(NFL_REALTIME_API).json()

    # Convert input to uppercase; NFL team abbreviations are in uppercase
    team_abbr = inp.upper()

    if team_abbr:
        # If user has specified a team, return the match with that team
        for game_id in data:
            match = data[game_id]
            home = data[game_id][HOME]
            away = data[game_id][AWAY]
            if team_abbr in [home[ABBR], away[ABBR]]:
                return get_match_info(home, away)

        # Non-existent football team or team is not playing this week
        return "{} not found".format(inp)

    # Build entire schedule
    schedule = []
    for game_id in data:
        match = data[game_id]
        home = match[HOME]
        away = match[AWAY]

        # Add all matches
        match_info = get_match_info(home, away)
        schedule.append(match_info)

    # Return all matches occurring in current week
    return ', '.join(schedule)
