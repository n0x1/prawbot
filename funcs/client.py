import os
import praw
from dotenv import load_dotenv


load_dotenv() 

# Initialize Reddit client
reddit = praw.Reddit(
    client_id = os.getenv("REDDIT_CLIENT_ID"),
    client_secret = os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent = os.getenv("REDDIT_USER_AGENT")
)
