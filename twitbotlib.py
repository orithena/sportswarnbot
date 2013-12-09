#!/usr/bin/python
# - coding: utf-8 -

import twython
import traceback
import time, datetime
import statefile

_APP_KEY=''
_APP_SECRET=''
_OAUTH_TOKEN=''
_OAUTH_TOKEN_SECRET=''
_OWNER = ''
_PRINT = True
_ERRTWEET = True

def setup(app_key, app_secret, oauth_token, oauth_token_secret, owner, print_messages=True, tweet_errors_to_owner=True):
    global _APP_KEY, _APP_SECRET, _OAUTH_TOKEN, _OAUTH_TOKEN_SECRET, _OWNER, _PRINT, _ERRTWEET
    _APP_KEY = app_key
    _APP_SECRET = app_secret
    _OAUTH_TOKEN = oauth_token
    _OAUTH_TOKEN_SECRET = oauth_token_secret
    _OWNER = owner
    _PRINT = print_messages
    _ERRTWEET = tweet_errors_to_owner

def tweet(msg, mention_all_followers=False):
    client = None
    try:
        client = twython.Twython(
            app_key=_APP_KEY, 
            app_secret=_APP_SECRET, 
            oauth_token=_OAUTH_TOKEN, 
            oauth_token_secret=_OAUTH_TOKEN_SECRET
        )
        try:
            if mention_all_followers:
                for follower in client.get_followers_list()["users"]:
                    s = u"@%s %s" % (follower["screen_name"], msg)
                    #client.update_status(status = s[:138])
                    if _PRINT: print("Status updated: %s" % s)
                    time.sleep(1)
            else:
                s = u"@%s %s" % (_OWNER, msg)
                client.update_status(status = s[:138])
                if _PRINT: print("Status updated: %s" % s)
        except Exception as e:
            s = u"@%s %s" % (_OWNER, e)
            if _ERRTWEET: client.update_status(status = s[:138])
            if _PRINT: print(u"Exception status: %s" % s)
    except Exception as e:
        if _PRINT: print(u"Exception while tweeting: %s" % e)
        print(traceback.format_exc())

def tweet_owner(msg):
    tweet(msg, mention_all_followers=False)

def tweet_followers(msg):
    tweet(msg, mention_all_followers=True)

def tweet_followers_once(tweettext, next_event_datetime, statefilename="bvbwarnbot.state", hours_before=26):
    statefile.set(statefilename)
    if not statefile.has(tweettext):
        if datetime.datetime.now() + datetime.timedelta(hours=hours_before) > next_event_datetime:
            statefile.save(tweettext)
            tweet_followers(tweettext)
        else:
            if _PRINT: print(
                "Not tweeted. %s -- Next Match: %s" % ( 
                    "Not due yet", 
                    next_event_datetime.strftime("%a, %d.%m.%Y %H:%M")
                ))
    else:
        if _PRINT: print(
            "Not tweeted. %s -- Next Match: %s" % ( 
                "Already in statefile",
                next_event_datetime.strftime("%a, %d.%m.%Y %H:%M")
            ))
