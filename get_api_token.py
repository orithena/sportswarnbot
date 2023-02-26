#!/usr/bin/python3

import config
import getpass
from mastodon import Mastodon

email = input("Email Address used to register Bot: ")
pwd = getpass.getpass("Password: ") 

Mastodon.create_app(
    config.app_name,
    api_base_url = config.api_base_url,
    to_file = config.app_key_file
)

mastodon = Mastodon(client_id = config.app_key_file,)

mastodon.log_in(
    email,
    pwd,
    to_file = config.user_key_file
)
