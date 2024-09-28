import instaloader
import os
from instagrapi import Client
from dotenv import load_dotenv
import time

# Load environment variables from the .env file
load_dotenv()

# Fetch Instagram credentials from environment variables
username = os.getenv('INSTAGRAM_USER')
password = os.getenv('INSTAGRAM_PW')

if username is None or password is None:
    raise Exception("Please set your environment variables 'INSTAGRAM_USER' and 'INSTAGRAM_PW'.")

# Initialize Instagrapi Client for messaging and media fetching
cl = Client()
cl.login(username, password)

# Fetch user_id from the username
user_id = cl.user_id_from_username(username)


clips = cl.user_clips(user_id=user_id, amount=5)
print(clips)