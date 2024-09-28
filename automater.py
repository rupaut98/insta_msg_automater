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

# Initialize Instaloader
L = instaloader.Instaloader()
L.login(username, password)  # Login to Instagram

# Initialize Instagrapi Client for messaging
cl = Client()
cl.login(username, password)

# The hardcoded thread_id for the group chat
thread_id = os.getenv('THREAD_ID')  # Replace this with your actual thread ID if different

# Function to fetch URLs of 100 Instagram video posts from the feed
def fetch_video_urls_from_feed(limit=100):
    video_urls = []
    for post in L.get_feed_posts():
        if post.is_video:
            video_urls.append(f"https://www.instagram.com/p/{post.shortcode}/")
            if len(video_urls) >= limit:
                break
    return video_urls

# Function to send messages alternately from the list of fetched video URLs
def send_messages_instagrapi_group(video_urls, thread_id, total_messages=600, delay=3):
    # Prepare for sending messages
    messages_sent = 0
    url_index = 0
    total_urls = len(video_urls)

    while messages_sent < total_messages:
        current_url = video_urls[url_index % total_urls]  # Cycle through the video URLs
        try:
            # Send the video URL to the group chat
            cl.direct_send(current_url, thread_ids=[thread_id])
            print(f"Sent message {messages_sent + 1}: {current_url}")
            messages_sent += 1
            url_index += 1  # Move to the next URL
            time.sleep(delay)  # Wait to avoid spamming
        except Exception as e:
            print(f"An error occurred while sending message {messages_sent + 1}: {e}")
            break

# Main execution block
if __name__ == "__main__":
    # Fetch video URLs
    video_urls = fetch_video_urls_from_feed(limit=100)
    print(f"Fetched {len(video_urls)} video URLs.")

    if len(video_urls) == 0:
        print("No video URLs found. Exiting.")
        exit()

    print(f"Sending messages to group thread ID: {thread_id}")

    # Send messages to the group chat
    send_messages_instagrapi_group(video_urls, thread_id, total_messages=600, delay=10)
