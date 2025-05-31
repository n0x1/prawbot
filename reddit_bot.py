import os
import praw
import requests
from dotenv import load_dotenv

load_dotenv() 

# Initialize Reddit client
reddit = praw.Reddit(
    client_id = os.getenv("REDDIT_CLIENT_ID"),
    client_secret = os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent = os.getenv("REDDIT_USER_AGENT")
)

SAVE_DIR = "downloaded_videos"
SUBREDDIT_NAME = "satisfying"


video_title_map = {}
os.makedirs(SAVE_DIR, exist_ok=True)
for submission in reddit.subreddit(SUBREDDIT_NAMEgi).hot(limit=10):
    if submission.is_video and submission.media and "reddit_video" in submission.media:
        video_url = submission.media["reddit_video"]["fallback_url"]
        response = requests.get(video_url, stream=True)
        if response.status_code == 200:
            filename = f"{submission.id}.mp4"
            filepath = os.path.join(SAVE_DIR, filename)
            with open(filepath, "wb") as f:
                for chunk in response.iter_content(chunk_size=1024):
                    f.write(chunk)
            video_title_map[filepath] = submission.title
            print(f"Downloaded: {filename}")
        else:
            print(f"Failed to download: {submission.id}")

print(video_title_map)
# `video_title_map` contains file paths mapped to their corresponding titles
