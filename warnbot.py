#!/usr/bin/python
# - coding: utf-8 -

import twitbotlib
import config
import importlib
import locale
from datetime import datetime
fetch_module = importlib.import_module(config.data_fetcher)


locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8')
twitbotlib.setup(config.app_key, config.app_secret, config.oauth_token, config.oauth_token_secret, config.owner)

try:
    tweettext, nextmatchtime = fetch_module.fetch_data()
    twitbotlib.tweet_once(tweettext, nextmatchtime, hours_before=(27,5))
except Exception as e:
    twitbotlib.tweet_owner(e)
    print(e)
    with open("/tmp/sportswarnbot.log", "a") as log:
        log.write("="*10 + datetime.isoformat(datetime.now()))
        traceback.print_exc(file=log)
