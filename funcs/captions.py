import whisper

def format_time(seconds):
    hrs, rem = divmod(int(seconds), 3600)
    mins, secs = divmod(rem, 60)
    millis = int((seconds - int(seconds)) * 1000)
    return f"{hrs:02}:{mins:02}:{secs:02},{millis:03}"

srt_path = "upload_assets/captions.srt"
def transcribe(video_path):
    model = whisper.load_model("medium.en")
    result = model.transcribe(video_path, word_timestamps=True)

    count = 1
    with open(srt_path, "w", encoding="utf-8") as f:
        for segment in result["segments"]:
            for word in segment.get("words", []):
                start = word["start"]
                end = word["end"]
                text = word["word"].strip()

                f.write(f"{count}\n")
                f.write(f"{format_time(start)} --> {format_time(end)}\n")
                f.write(f"{text}\n\n")
                count += 1
    return "upload_assets/captions.srt"
