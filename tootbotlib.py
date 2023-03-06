#!/usr/bin/python
# - coding: utf-8 -

from mastodon import Mastodon
import traceback
import time, datetime
import statefile

_CLIENT_CRED_FILE = ''
_OWNER = ''
_PRINT = True
_ERRTWEET = True

def setup(client_cred_file, owner, print_messages=True, toot_errors_to_owner=False):
    global _CLIENT_CRED_FILE, _OWNER, _PRINT, _ERRTWEET
    _CLIENT_CRED_FILE = client_cred_file
    _OWNER = owner
    _PRINT = print_messages
    _ERRTWEET = toot_errors_to_owner

def toot(msg, owner_mention=True):
    client = None
    try:
        client = Mastodon(
            access_token=_CLIENT_CRED_FILE
        )
        try:
            if not owner_mention:
                # mentioning owner with errors is disabled with this if
                s = "@%s %s" % (_OWNER, msg) if owner_mention else "%s" % msg
                client.toot(status = s[:498])
                if _PRINT: print("Status updated: %s" % s)
        except Exception as e:
            s = "@%s %s" % (_OWNER, e)
            if _ERRTWEET:
                client.toot(status = s[:300])
            if _PRINT:
                print("Exception status: %s" % s)
                print(traceback.format_exc())
    except Exception as e:
        if _PRINT: print("Exception while tooting: %s" % e)
        print(traceback.format_exc())

def once(toottext, next_event_datetime, statefilename="warnbot.state", hours_before=26):
    statefile.set(statefilename)
    event_delta = (datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=hours_before)) - next_event_datetime
    if not statefile.has(toottext):
        if event_delta > datetime.timedelta(0):
            statefile.save(toottext)
            toot(toottext, owner_mention=False)
        else:
            if _PRINT: print(
                "%dh warning not tooted. %s -- Next Match: %s" % (
                    hours_before,
                    "Due in %d hour(s)" % (1-int(event_delta.total_seconds() / (60*60))),
                    next_event_datetime.strftime("%a, %d.%m.%Y %H:%M")
                ))
    else:
        if _PRINT: print(
            "%dh warning not tooted. %s -- Next Match: %s" % (
                hours_before,
                "Already in statefile",
                next_event_datetime.strftime("%a, %d.%m.%Y %H:%M")
            ))

def toot_once(toottext, next_event_datetime, statefilename="warnbot.state", hours_before=(26, 4)):
    for hb in hours_before:
        once("%dh-%s" % (hb-1, toottext), next_event_datetime, statefilename=statefilename, hours_before=hb)

def toot_owner(msg):
    toot(msg)
