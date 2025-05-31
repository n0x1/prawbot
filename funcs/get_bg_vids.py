from client import reddit
import requests
import os


## FIRST WE GET THE VIDS 
SAVE_DIR = "downloaded_videos"

video_title_map = {} # contains file paths mapped to their corresponding titles
os.makedirs(SAVE_DIR, exist_ok=True)

def get_vids(BGVID_SUB_NAME):
    for submission in reddit.subreddit(BGVID_SUB_NAME).hot(limit=5):
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

    return video_title_map


if __name__ == "__main__":
     get_vids("oddlysatisfying")