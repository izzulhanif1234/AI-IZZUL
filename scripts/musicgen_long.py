"""MusicGen-small with audio continuation to get a bed longer than 30 s.

usage: musicgen_long.py OUT SECONDS "prompt" [seed]
Generates 30 s, then repeatedly feeds the last 10 s back as an audio prompt and
keeps the 20 s of new material, until SECONDS is reached.
"""
import sys
import numpy as np
import soundfile as sf
import torch
from transformers import AutoProcessor, MusicgenForConditionalGeneration

out, total, prompt = sys.argv[1], float(sys.argv[2]), sys.argv[3]
torch.manual_seed(int(sys.argv[4]) if len(sys.argv) > 4 else 11)
proc = AutoProcessor.from_pretrained("facebook/musicgen-small")
model = MusicgenForConditionalGeneration.from_pretrained("facebook/musicgen-small")
sr = model.config.audio_encoder.sampling_rate
inputs = proc(text=[prompt], padding=True, return_tensors="pt")
song = model.generate(**inputs, do_sample=True, guidance_scale=3.0, max_new_tokens=1500)[0, 0].numpy()
print("seg0", len(song) / sr, flush=True)
while len(song) / sr < total:
    ctx = song[-10 * sr:]
    inputs = proc(audio=ctx, sampling_rate=sr, text=[prompt], padding=True, return_tensors="pt")
    gen = model.generate(**inputs, do_sample=True, guidance_scale=3.0, max_new_tokens=1500)[0, 0].numpy()
    new = gen[len(ctx):]
    song = np.concatenate([song, new])
    print("len", len(song) / sr, flush=True)
sf.write(out, song.astype(np.float32), sr)
print("done", out)
