#!/usr/bin/python
# - coding: utf-8 -

from bs4 import BeautifulSoup as Soup
from tidylib import tidy_document
from soupselect import select
import traceback
import urllib.request, urllib.error, urllib.parse, datetime, time, locale, sys

tidyoptions = { "output-xhtml": 1, "tidy-mark": 0, "force-output": 1, "char-encoding": "utf8", }

def fetch_data():
    def bvbreplace(s):
        return "BVB" if "Dortmund" in s else s

    doc = None
    try:
        doc, errs = tidy_document(urllib.request.urlopen('http://www.bvb.de/').read(), tidyoptions)
        soup = Soup(doc, "lxml")
    except Exception as e:
        print((traceback.format_exc()))
        raise Exception("Error fetching/parsing website: %s" % e.message)

    out = ''
    matchtime = datetime.datetime.now() + datetime.timedelta(hours=25)
    timestr = ''
    try:
        home = bvbreplace(select(soup, "div.next-match p span")[0].contents[0].strip())
        guest = bvbreplace(select(soup, "div.next-match p span")[1].contents[0].strip())
        league = ''
        try:
            league = select(soup, "div.next-match p span.tournament")[0].contents[0].strip()
        except:
            league = select(soup, "div.next-match p span")[2].contents[0].strip()            
        if "Test" in league:
            sys.exit(1)
        matchtime = datetime.datetime.strptime(select(soup, "div.next-match p")[1].contents[-1].strip(), "%d.%m.%Y %H:%M")
        timestr = matchtime.strftime("%a, %d.%m.%Y %H:%M")
        dontgo = "Meide U42/U46/Kreuzviertel/Borsigplatz/Uni-Parkplatz" if "BVB" == home else "Meide Kneipen mit TV in Dortmund"
        #dontgo = u"Hat jemand die Fans seit Start der Bundesliga beobachtet und kann Hinweise zu deren tatsächlichem Verhalten geben?"
        location = "Heim" if "BVB" == home else "Auswaerts"
        out = "WARNUNG! %s: %s vs %s (%s/%s). %s." % (timestr, home, guest, location, league, dontgo)
    except IndexError:
        # This means: No next game on the webpage.
        sys.exit(1)
    except Exception as e:
        print((traceback.format_exc()))
        raise Exception("ERRBVB while parsing bvb.de: %s" % e)
    return out, matchtime
