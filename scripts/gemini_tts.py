"""Gemini TTS -> wav. Key is read from the file named in $GEMINI_KEY_FILE (never stored in the repo); without it,
a placeholder is sent and the environment's network secret for generativelanguage.googleapis.com supplies the key.
usage: gemini_tts.py lines.json outdir [model] [voice]
lines.json: [{"id":..., "text":..., "style": optional override}]"""
import base64, json, os, sys, time, urllib.request, wave

KEY = open(os.environ["GEMINI_KEY_FILE"]).read().strip() if os.environ.get("GEMINI_KEY_FILE") else "proxy-injected"
STYLE = ("You are a Malaysian Malay voice-over artist. Read the user's text aloud exactly as written, "
         "in natural Malaysian Malay, as a confident, warm documentary narrator for a state-level "
         "innovation competition video. Do not add or read any other words.")


def tts(text, model, voice, style=STYLE):
    body = {
        "contents": [{"parts": [{"text": text}]}],
        "generationConfig": {
            "responseModalities": ["AUDIO"],
            "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": voice}}},
        },
    }
    req = urllib.request.Request(
        # key as a query parameter: a proxy-injected x-goog-api-key header would override a header key
        f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={KEY}",
        data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=600) as r:
                d = json.load(r)
            part = d["candidates"][0]["content"]["parts"][0]["inlineData"]
            return base64.b64decode(part["data"]), part.get("mimeType", "")
        except urllib.error.HTTPError as e:
            msg = e.read().decode()[:300]
            print("HTTP", e.code, msg, file=sys.stderr)
            if e.code in (429, 500, 502, 503, 504):
                time.sleep(8 * (attempt + 1)); continue
            raise
    raise RuntimeError("tts failed")


def save_wav(pcm, path, rate=24000):
    with wave.open(path, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(rate); w.writeframes(pcm)


if __name__ == "__main__":
    lines = json.load(open(sys.argv[1]))
    out = sys.argv[2]; os.makedirs(out, exist_ok=True)
    model = sys.argv[3] if len(sys.argv) > 3 else "gemini-3.8-flash-tts"
    voice = sys.argv[4] if len(sys.argv) > 4 else "Charon"
    for l in lines:
        pcm, mime = tts(l["text"], model, l.get("voice", voice), l.get("style", STYLE))
        if pcm[:4] == b"RIFF":  # already a wav container
            open(f"{out}/{l['id']}.wav", "wb").write(pcm)
        else:
            rate = int(mime.split("rate=")[1].split(";")[0]) if "rate=" in mime else 24000
            save_wav(pcm, f"{out}/{l['id']}.wav", rate)
        print("ok", l["id"], mime)
