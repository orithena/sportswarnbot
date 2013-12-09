sportswarnbot
=============

This is a Twitter Bot for Non-Sport-Fans that warns its followers about upcoming 
matches of sports teams -- and the onslaught of the associated fan base.

Currently, it only supports upcoming matches of Borussia Dortmund by scraping bvb.de.
It is planned to use openligadb.de as a data source to make it easier to fork your
own bot.

  * Für BVB-Warnungen folge @bvbwarnbot: https://twitter.com/bvbwarnbot



Dependencies
------------

  * Python 2.7 (although 3.x might just work)
  * Python modules:
    * BeautifulSoup
    * tidylib
    * twython
  * Cron
  * internet connection
  * running on a linux box that runs 24/7



Install
-------

```bash
$ git clone https://github.com/orithena/sportswarnbot.git
```


Configure/Develop
-----------------

Copy bvbwarner.py to another file, maybe myhsvwarnbot.py, then edit it according to 
your needs. The main point is the Twitter API key and OAuth secret -- here's 
how to obtain one:

  * Create a new account on Twitter, maybe "hsvwarnbot".
  * Do not forget to confirm the email address.
  * Go to https://dev.twitter.com/
  * Sign in as the newly created account.
  * In the top right user menu, click on "My Applications".
  * Click on "Create a new application" and register an application.
  * When you're done with this, choose the "Settings" tab on the application's page.
  * Set the "Application type" to "Read and Write" (and optional "direct messages")
  * Save setting by clicking "Update this Twitter application's settings"
  * Go to the "Details" tab of the application
  * Click "Create access token" and wait a while (some minutes or so).
  * Reload the "Details" tab
  * Copy and paste the access key data into the correct variables in your python file:
    * Consumer key        -> app_key
    * Consumer secret     -> app_secret
    * Access token        -> oauth_token
    * Access token secret -> oauth_token_secret
    * Your own twitter screen name -> owner (lose the @)
  * Re-check the key's access level below the token secret.
  * If it's not at least "Read and Write", you confused the order of the steps above.

Apart from that, you need to rewrite the data fetching function fetch_bvb() to match
the website of the sports club in your vicinity. Luckily, there's soupselect included
which gives you almost jQuery-like powers when it comes to selecting elements from a
HTML DOM.

As soon as your bot has got some followers, you may want to comment out the 
```python
client.update_status(...)
```
line (l.40) in twitbotlib.py when you're testing around with the bot. No need to spam
all your followers with your botched attempts to get it right ;-)

When you're done, put the program into your crontab:
```bash
$ crontab -e
55 * * * * /path/to/sportswarnbot/myhsvwarnbot.py | logger -t hsvwarnbot
```
  
This will call the bot every hour at xx:55 and log all output into /var/log/syslog.
The way it's set up currently, it would try to tweet the configured owner if there 
is an error. If that fails, there's always the output in the syslog.

If you re-publish the bot to github, MAKE SURE YOU NEVER PUBLISH THE TWITTER API KEY DATA!
This line of bash may help:
```bash
cat myhsvwarnbot.py | sed 's/^\([a-zA-Z_]\+="\).*"/\1"/' > hsvwarnbot.py
```
Then simply do not execute "git add myhsvwarnbot.py".
