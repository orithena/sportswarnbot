
# the screenname of the owner (for error messages etc)
owner=""

# the module containing the fetch_data() function
data_fetcher='bvb'

# toot how many hours before the event? (tuple of integers)
hours_before=(27,5)

# app_name of the bot (shows up in your authorized applications)
app_name="bvbwarnbot"

# base url of the Mastodon server you're using
api_base_url="https://botsin.space/"

# where to store app tokens? Set a path, then run get_api_token.py to fetch and store credentials
app_key_file="bvbwarnbot.client.secret"
user_key_file="bvbwarnbot.user.secret"

# where to log the error messages?
log_file="/tmp/sportswarnbot-mastodon.log"

# where to store the app state?
state_file="/tmp/sportswarnbot-mastodon.state"
