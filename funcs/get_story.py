from client import reddit


def get_story(STORY_SUB_NAME):
    for submission in reddit.subreddit(STORY_SUB_NAME).hot(limit=3): # First 2 posts will be ignored bc pinned
        if submission.stickied:
            continue
        title = submission.title
        body = submission.selftext
        story = f"{title} || {body}"

    return story

