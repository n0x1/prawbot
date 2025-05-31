import praw
import requests
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT"),
)


for submission in reddit.subreddit("interestingasfuck").hot(limit=1):
    title = submission.title
    # body = submission.selftext
    urls = submission.url
    link = requests.get(urls).url

    # c1 = submission.comments[0].body
    # c2 = submission.comments[1].body
    print(link)
    

# gen_tts(title)
