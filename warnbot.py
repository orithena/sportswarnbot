#!/usr/bin/python3
# - coding: utf-8 -

import twitbotlib
import config
import importlib
import locale
import traceback
from datetime import datetime
fetch_module = importlib.import_module(config.data_fetcher)


locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8')
twitbotlib.setup(config.app_key, config.app_secret, config.oauth_token, config.oauth_token_secret, config.owner)

with open("/tmp/sportswarnbot.log", "a") as log:
    log.write("="*5 + "bvbwarnbot" + "="*5 + datetime.isoformat(datetime.now())+ "\n")

try:
    tweettext, nextmatchtime = fetch_module.fetch_data()
    with open("/tmp/sportswarnbot.log", "a") as log:
        log.write("Got parsed data at " + datetime.isoformat(datetime.now())+ "\n")
    twitbotlib.tweet_once(tweettext, nextmatchtime, hours_before=(27,5))
    with open("/tmp/sportswarnbot.log", "a") as log:
        log.write("Done at " + datetime.isoformat(datetime.now())+ "\n")
except Exception as e:
    twitbotlib.tweet_owner(e)
    print(e)
    with open("/tmp/sportswarnbot.log", "a") as log:
        traceback.print_exc(file=log)
