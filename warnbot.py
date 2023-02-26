#!/usr/bin/python3
# - coding: utf-8 -

import tootbotlib
import config
import importlib
import locale
import traceback
from datetime import datetime
fetch_module = importlib.import_module(config.data_fetcher)


locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8')
tootbotlib.setup(config.user_key_file, config.owner)

with open(config.log_file, "a") as log:
    log.write("="*5 + config.app_name + "="*5 + datetime.isoformat(datetime.now())+ "\n")

try:
    toottext, nextmatchtime = fetch_module.fetch_data()
    with open(config.log_file, "a") as log:
        log.write("Got parsed data at " + datetime.isoformat(datetime.now())+ "\n")
    tootbotlib.toot_once(toottext, nextmatchtime, hours_before=(27,5), statefilename=config.state_file)
    with open(config.log_file, "a") as log:
        log.write("Done at " + datetime.isoformat(datetime.now())+ "\n")
except Exception as e:
    tootbotlib.toot_owner(e)
    print(e)
    with open(config.log_file, "a") as log:
        traceback.print_exc(file=log)
