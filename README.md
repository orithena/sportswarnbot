sportswarnbot
=============

This is a Mastodon Bot for Non-Sport-Fans that warns its followers about upcoming 
matches of sports teams -- and the onslaught of the associated fan base.

Currently, it only supports upcoming matches of Borussia Dortmund by scraping bvb.de.
It is planned to use openligadb.de as a data source to make it easier to fork your
own bot.

  * Für BVB-Warnungen folge @bvbwarnbot@botsin.space: https://botsin.space/@bvbwarnbot



Dependencies
------------

  * Python 3.5 or higher
  * Python modules:
    * BeautifulSoup4
    * tidylib
    * Mastodon
  * Cron
  * internet connection
  * running on a linux box that runs 24/7



Install
-------

```bash
$ git clone https://github.com/orithena/sportswarnbot.git
```


Configure
---------

```bash
$ cp config_clean.py config.py
$ $EDITOR config.py
```

The main point is the Mastodon API key and OAuth secret -- here's 
how to obtain one:

  * Create a new account on botsin.space, maybe "hsvwarnbot".
  * Do not forget to confirm the email address.
  * Run get_api_token.py, enter email address and password.
  * Tokens are now stored in the files configured in config.py


Develop
-------

Copy bvb.py to another file, maybe hsv.py, then edit it according to your
needs. You need to rewrite the data fetching function fetch_data() to match
the website of the sports club in your vicinity. Luckily, there's
soupselect included which gives you almost jQuery-like powers when it comes
to selecting elements from a HTML DOM.

As soon as your bot has got some followers, you may want to comment out the 
```python
client.toot(...)
```
line (l.40) in tootbotlib.py when you're testing around with the bot. No need to spam
all your followers with your botched attempts to get it right ;-)

When you're done, put the program into your crontab:
```bash
$ crontab -e
55 * * * * /path/to/sportswarnbot/warnbot.py | logger -t hsvwarnbot
```
  
This will call the bot every hour at xx:55 and log all output into /var/log/syslog.
The way it's set up currently, it would try to tweet the configured owner if there 
is an error. If that fails, there's always the output in the syslog.

If you re-publish the bot to github, 
MAKE SURE YOU NEVER PUBLISH THE MASTODON API KEY DATA!
Simply never execute "git add config.py".
