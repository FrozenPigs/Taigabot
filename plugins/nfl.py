import requests

NFL_REALTIME_API = 'http://static.nfl.com/liveupdate/scores/scores.json'


@hook.command(autohelp=False)
def nfl(inp):
    data = requests.get(
        "http://static.nfl.com/liveupdate/scores/scores.json")
    data = data.json()
    return str(data)
