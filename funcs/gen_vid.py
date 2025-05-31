from moviepy.editor import VideoFileClip, AudioFileClip, CompositeVideoClip, concatenate_videoclips
from moviepy.video.tools.subtitles import SubtitlesClip
from moviepy.video.fx.all import resize
from moviepy.video.VideoClip import TextClip
import os
import random
import glob

os.environ["IMAGEMAGICK_BINARY"] = "/usr/local/bin/convert"

def generate_final_video(video_folder, srt_filename, voiceover_filename=None, output_path="final_output.mp4"):
    base_dir = os.path.expanduser("~/Developer/socialbots/vidgen-bot/")
    
    video_folder_path = os.path.join(base_dir, video_folder)
    srt_path = os.path.join(base_dir, srt_filename)
    if voiceover_filename:
        voiceover_path = os.path.join(base_dir, voiceover_filename)
    else:
        voiceover_path = None
    
    print(f"Video folder: {video_folder_path}")
    print(f"SRT path: {srt_path}")
    print(f"Folder exists: {os.path.exists(video_folder_path)}")
    print(f"SRT exists: {os.path.exists(srt_path)}")
    
    # Get all video files from the folder
    video_extensions = ['*.mp4', '*.avi', '*.mov', '*.mkv', '*.wmv', '*.flv']
    video_files = []
    for ext in video_extensions:
        video_files.extend(glob.glob(os.path.join(video_folder_path, ext)))
        video_files.extend(glob.glob(os.path.join(video_folder_path, ext.upper())))
    
    if not video_files:
        raise ValueError(f"No video files found in {video_folder_path}")
    
    print(f"Found {len(video_files)} video files")
    
    # Load audio to get target duration
    if voiceover_path:
        audio = AudioFileClip(voiceover_path)
        target_duration = audio.duration
    else:
        # Get duration from SRT file
        with open(srt_path, 'r', encoding='utf-8') as f:
            content = f.read()
        # Find the last timestamp in SRT
        lines = content.strip().split('\n')
        for line in reversed(lines):
            if '-->' in line:
                end_time = line.split('-->')[1].strip()
                # Parse timestamp (HH:MM:SS,mmm)
                time_parts = end_time.replace(',', ':').split(':')
                target_duration = int(time_parts[0]) * 3600 + int(time_parts[1]) * 60 + int(time_parts[2]) + float(time_parts[3]) / 1000
                break
    
    print(f"Target duration: {target_duration} seconds")
    
    # Create looped video to match target duration
    looped_video = create_looped_video(video_files, target_duration)
    
    def subtitle_generator(txt):
        return TextClip(txt,
                       font='upload_assets/Belissio.ttf',
                       fontsize=92,
                       color='white',
                       stroke_color='black',
                       stroke_width=4,
                       size=(looped_video.w - 40, None),
                       method='caption')
    
    subs = SubtitlesClip(srt_path, subtitle_generator)
    video_with_subs = CompositeVideoClip([
        looped_video,
        subs.set_position(('center', 'center'), relative=True)
    ])
    
    if voiceover_path:
        final = video_with_subs.set_audio(audio)
    else:
        final = video_with_subs
    
    final.write_videofile(output_path, fps=24)
    
    # Cleanup
    looped_video.close()
    subs.close()
    video_with_subs.close()
    if voiceover_path:
        audio.close()

def create_looped_video(video_files, target_duration):
    """Create a looped video from random clips until target duration is reached"""
    clips = []
    current_duration = 0
    
    while current_duration < target_duration:
        # Pick a random video file
        random_video_path = random.choice(video_files)
        print(f"Adding video: {os.path.basename(random_video_path)}")
        
        try:
            clip = VideoFileClip(random_video_path)
            clip = resize(clip, width=720)
            clip = clip.fx(lambda c: c.speedx(2))  # 2x speed
            
            # Calculate how much more duration we need
            remaining_duration = target_duration - current_duration
            
            if clip.duration <= remaining_duration:
                # Use the whole clip
                clips.append(clip)
                current_duration += clip.duration
            else:
                # Trim the clip to fit exactly
                trimmed_clip = clip.subclip(0, remaining_duration)
                clips.append(trimmed_clip)
                current_duration += remaining_duration
                clip.close()  # Close the original since we're using trimmed version
                
        except Exception as e:
            print(f"Error loading {random_video_path}: {e}")
            continue
    
    print(f"Created video loop with {len(clips)} clips, total duration: {current_duration}")
    
    # Concatenate all clips
    if len(clips) == 1:
        return clips[0]
    else:
        return concatenate_videoclips(clips)

# Alternative version that takes a single video and loops it
def generate_final_video_single_loop(video_filename, srt_filename, voiceover_filename=None, output_path="final_output.mp4"):
    """Version that loops a single video file"""
    base_dir = os.path.expanduser("~/Developer/socialbots/vidgen-bot/")
    
    video_path = os.path.join(base_dir, video_filename)
    srt_path = os.path.join(base_dir, srt_filename)
    if voiceover_filename:
        voiceover_path = os.path.join(base_dir, voiceover_filename)
        audio = AudioFileClip(voiceover_path)
        target_duration = audio.duration
    else:
        voiceover_path = None
        # Get duration from SRT (same logic as above)
        with open(srt_path, 'r', encoding='utf-8') as f:
            content = f.read()
        lines = content.strip().split('\n')
        for line in reversed(lines):
            if '-->' in line:
                end_time = line.split('-->')[1].strip()
                time_parts = end_time.replace(',', ':').split(':')
                target_duration = int(time_parts[0]) * 3600 + int(time_parts[1]) * 60 + int(time_parts[2]) + float(time_parts[3]) / 1000
                break
    
    # Load and loop single video
    video = VideoFileClip(video_path)
    video = resize(video, width=720)
    video = video.fx(lambda c: c.speedx(2))  # 2x speed
    
    # Calculate how many loops we need
    loops_needed = int(target_duration / video.duration) + 1
    video_clips = [video] * loops_needed
    looped_video = concatenate_videoclips(video_clips).subclip(0, target_duration)
    
    def subtitle_generator(txt):
        return TextClip(txt,
                       font='Futura-CondensedExtraBold',
                       fontsize=48,
                       color='white',
                       stroke_color='black',
                       stroke_width=0.5,
                       size=(looped_video.w - 40, None),
                       method='caption')
    
    subs = SubtitlesClip(srt_path, subtitle_generator)
    video_with_subs = CompositeVideoClip([
        looped_video,
        subs.set_position(('center', 0.65), relative=True)
    ])
    
    if voiceover_path:
        final = video_with_subs.set_audio(audio)
    else:
        final = video_with_subs
    
    final.write_videofile(output_path, fps=24)
    
    # Cleanup
    video.close()
    looped_video.close()
    subs.close()
    video_with_subs.close()
    if voiceover_path:
        audio.close()

# Usage examples:
# generate_final_video("background_videos", "story.srt", "voiceover.mp3")  # Random videos from folder
# generate_final_video_single_loop("background.mp4", "story.srt", "voiceover.mp3")  # Single video looped