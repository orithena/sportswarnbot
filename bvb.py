#!/usr/bin/python
# - coding: utf-8 -

from BeautifulSoup import BeautifulSoup as Soup
from tidylib import tidy_document
from soupselect import select
import urllib2, datetime, time, locale

tidyoptions = { "output-xhtml": 1, "tidy-mark": 0, "force-output": 1, }

def fetch_data():
    def bvbreplace(s):
        return "BVB" if "Dortmund" in s else s

    doc = None
    try:
        doc, errs = tidy_document(urllib2.urlopen('http://www.bvb.de/').read(), tidyoptions)
        soup = Soup(doc)
    except Exception as e:
        raise Exception("Error fetching/parsing website: %s" % e)

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
        matchtime = datetime.datetime.strptime(select(soup, "div.next-match p")[1].contents[-1].strip(), "%d.%m.%Y %H:%M")
        timestr = matchtime.strftime("%a, %d.%m.%Y %H:%M")
        dontgo = "U42/U46/Kreuzviertel/Borsigplatz/Uni-Parkplatz" if "BVB" == home else "Kneipen mit TV in Dortmund"
        location = "Heim" if "BVB" == home else "Auswaerts"
        out = "WARNUNG! %s: %s vs %s (%s/%s). Meide %s." % (timestr, home, guest, location, league, dontgo)
    except Exception as e:
        #print(traceback.format_exc())
        raise Exception("ERRBVB: %s" % e)
    return out, matchtime