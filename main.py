import os
import praw
import requests
from funcs.tts import gen_tts
from funcs.captions import transcribe
from funcs.get_bg_vids import get_vids
from funcs.get_story import get_story
from funcs.gen_vid import generate_final_video


needvids = False
needstory = True
VID_SUB_NAME = "satisfying"
STORY_SUB_NAME = "NuclearRevenge" # Get the stories from here

if needvids:
    get_vids(VID_SUB_NAME)
    
if needstory:
    story = get_story(STORY_SUB_NAME)

audio = gen_tts(story)
captions = transcribe(audio)  
bg_vid_folder = "downloaded_videos"
generate_final_video(bg_vid_folder, "upload_assets/captions.srt", audio)