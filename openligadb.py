#!/usr/bin/python
# - coding: utf-8 -

import datetime
import locale
import sys

import httpx

# Most teams can be found at https://www.openligadb.de/api/getavailableteams/bl1/2019 and https://www.openligadb.de/api/getavailableteams/bl2/2019


def fetch_data(
    team_name: str,
    team_city: str,
    week_count_future: int = 1,
    avoid_home_message: str = "",
):
    locale.setlocale(locale.LC_ALL, "de_DE.UTF-8")
    if avoid_home_message == "":
        avoid_home_message = f"Meide typische Fußball-Orte in {team_city}"
    # Get the next game from openligadb.de
    # This is a JSON API, so we use httpx
    games = []
    try:
        r = httpx.get(
            f"https://api.openligadb.de/getmatchesbyteam/{team_name}/0/{week_count_future}"
        )
        r.raise_for_status()
        games = r.json()
    except Exception as e:
        raise Exception(f"Error fetching/parsing website: {e}")

    out = ""
    matchtime = datetime.datetime.now() + datetime.timedelta(hours=25)
    timestr = ""
    try:
        home = games[0]["team1"]["teamName"]
        guest = games[0]["team2"]["teamName"]
        league = games[0]["leagueName"]
        matchtime = datetime.datetime.strptime(
            games[0]["matchDateTimeUTC"], "%Y-%m-%dT%H:%M:%S%z"
        )
        timestr = matchtime.strftime("%A, %d.%m.%Y %H:%M")
        dontgo = (
            avoid_home_message
            if team_name == home
            else f"Meide Kneipen mit TV in {team_city}"
        )
        location = "Heim" if team_name == home else "Auswärts"
        out = (
            f"WARNUNG! {timestr}: {home} vs {guest} ({league} — {location}). {dontgo}."
        )
    except IndexError:
        # This means: No next game on the webpage.
        sys.exit(1)
    except Exception as e:
        raise Exception(f"Error: {e}")
    return out, matchtime
