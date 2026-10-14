"""Transcribe audio with word-level timestamps (faster-whisper) -> JSON."""
import json
import sys
import wave

import numpy as np
from faster_whisper import WhisperModel

audio, out = sys.argv[1], sys.argv[2]
model_name = sys.argv[3] if len(sys.argv) > 3 else "large-v3"

# Load 16kHz mono WAV directly (avoids PyAV version issues)
with wave.open(audio) as w:
    pcm = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768.0

model = WhisperModel(model_name, device="cpu", compute_type="int8")
segments, info = model.transcribe(pcm, word_timestamps=True, vad_filter=False, beam_size=5)

result = {"language": info.language, "language_probability": info.language_probability, "segments": []}
for s in segments:
    result["segments"].append({
        "start": round(s.start, 2), "end": round(s.end, 2), "text": s.text.strip(),
        "words": [{"start": round(w.start, 2), "end": round(w.end, 2), "word": w.word.strip(), "p": round(w.probability, 2)} for w in s.words],
    })
    print(f"[{s.start:6.2f} -> {s.end:6.2f}] {s.text.strip()}", flush=True)

with open(out, "w") as f:
    json.dump(result, f, ensure_ascii=False, indent=1)
print("language:", info.language, round(info.language_probability, 2))
