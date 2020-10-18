from util import formatting, hook, http, web
import requests

NFL_REALTIME_API = 'http://static.nfl.com/liveupdate/scores/scores.json'
HOME = 'home'
AWAY = 'away'
ABBR = 'abbr'   # e.g. NE, DAL
SCORE = 'score'
T = 'T'         # Current score
QTR = 'qtr'
YL = 'yl'
DOWN = 'down'
TOGO = 'togo'
CLOCK = 'clock'
POSTEAM = 'posteam'  # Possessing team


def ordinaltg(n):
    """ Add an ordinal (-st, -nd, -rd) to a number
    """
    return str(n) + {1: 'st', 2: 'nd', 3: 'rd'}.get(4 if 10 <=
                                                    n % 100 < 20 else n % 10, "th")


def get_match_info(home, away, match=None):
    """ Returns teams and scores for a given match
    """

    home_abbr = home[ABBR]
    # If None type, turn it to 0
    home_score = home[SCORE][T] or 0
    away_abbr = away[ABBR]
    away_score = away[SCORE][T] or 0

    # Returning brief info for given match; used in getting all NFL games for
    # current week
    if not match:
        return "{} {} {} {}".format(
            home_abbr, home_score, away_abbr, away_score)

    # Get detailed game stats for a specific match

    # Game has not started or has ended
    quarter = match[QTR]
    if not quarter or quarter.lower() in ["final", "pregame"]:
        return "{} {} {} {} - {}".format(home_abbr,
                                         home_score,
                                         away_abbr,
                                         away_score,
                                         quarter)

    # Game is ongoing, fetch and return detailed info
    yard_line = match[YL]
    down = ordinaltg(match[DOWN])
    to_go = match[TOGO]
    clock = match[CLOCK]
    pos_team = match[POSTEAM]
    # Example: TB 14 GB 10 - 2Q 11:02 - [GB] 1st & 10 @ GB 25
    return "{} {} {} {} - {}Q {} - [{}] {} & {} @ {}".format(
        home_abbr,
        home_score,
        away_abbr,
        away_score,
        quarter,
        clock,
        pos_team,
        down,
        to_go,
        yard_line)


@hook.command(autohelp=False)
def nfl(inp):
    """nfl | nfl <team abbreviation> -- Returns all matchups for current week, or only for a specified team's matchup
    """

    # Get real time data
    try:
        data = requests.get(NFL_REALTIME_API).json()
    except Exception as e:
        return "Could not get NFL data"

    # Convert input to uppercase; NFL team abbreviations are in uppercase
    team_abbr = inp.upper()

    if team_abbr:
        # If user has specified a team, return the match with that team
        for game_id in data:
            match = data[game_id]
            home = data[game_id][HOME]
            away = data[game_id][AWAY]
            if team_abbr in [home[ABBR], away[ABBR]]:
                return get_match_info(home, away, match)

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
