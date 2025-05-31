import torch
import torchaudio as ta
from chatterbox.tts import ChatterboxTTS

# Detect device (Mac with M1/M2/M3/M4)
device = "mps" if torch.backends.mps.is_available() else "cpu"
map_location = torch.device(device)

torch_load_original = torch.load
def patched_torch_load(*args, **kwargs):
    if 'map_location' not in kwargs:
        kwargs['map_location'] = map_location
    return torch_load_original(*args, **kwargs)

torch.load = patched_torch_load

model = ChatterboxTTS.from_pretrained(device=device)

# If you want to synthesize with a different voice, specify the audio prompt
AUDIO_PROMPT_PATH = "trump-sample.wav"

def gen_tts(text):
    wav = model.generate(
        text, 
        audio_prompt_path=AUDIO_PROMPT_PATH,
        exaggeration=1.2,
        cfg_weight=0.3
        )
    ta.save("upload_assets/tts.wav", wav, model.sr)
    return "upload_assets/tts.wav"



if __name__ == "__main__":
    gen_tts("Hello")

