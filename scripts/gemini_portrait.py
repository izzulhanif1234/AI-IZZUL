"""Corporate studio portraits from a passport-style photo with a Gemini image model.
Key is read from the file named in $GEMINI_KEY_FILE (never stored in the repo).
usage: gemini_portrait.py src.jpg out_prefix pose [model]
pose: duduk | berdiri | separuh"""
import base64, json, os, sys, time, urllib.request

KEY = open(os.environ["GEMINI_KEY_FILE"]).read().strip()

BASE = (
    "Using the attached photo as the identity reference, create a high-end corporate studio portrait "
    "of the SAME woman. Keep her face, facial features, skin tone, expression, glasses (if any), "
    "hijab colour and style, blazer and inner clothing exactly as in the reference, including the "
    "name tag on the blazer if there is one. Do not beautify or change her face shape. "
    "Setting: professional photo studio with a seamless charcoal-grey backdrop and a soft gradient "
    "glow behind her, large softbox key light from the front-left, gentle rim light, clean and "
    "elegant corporate look like an executive company profile photo. Shot on a full-frame camera, "
    "85mm lens, shallow depth of field, sharp focus on the eyes, natural skin texture, photorealistic. "
    "No text, no watermark, no logos added. "
)
POSES = {
    "duduk": "Pose: she is seated on a modern dark leather studio chair, body angled slightly to the side, "
             "turned to face the camera, hands resting neatly on her lap, confident and friendly smile. "
             "Frame from head to just below the knees.",
    "berdiri": "Pose: she is standing upright, body turned about 30 degrees, arms crossed confidently "
               "in front of her chest, looking at the camera with a confident, warm smile. "
               "Frame as a three-quarter length shot from head to mid-thigh.",
    "separuh": "Pose: standing, shoulders slightly angled, hands lightly clasped in front at waist level, "
               "looking at the camera. Frame from head to waist.",
}


def generate(src, pose, model):
    img = base64.b64encode(open(src, "rb").read()).decode()
    body = {
        "contents": [{"parts": [
            {"inlineData": {"mimeType": "image/jpeg", "data": img}},
            {"text": BASE + POSES[pose]},
        ]}],
        "generationConfig": {
            "responseModalities": ["IMAGE"],
            "imageConfig": {"aspectRatio": "4:5", "imageSize": "2K"},
        },
    }
    req = urllib.request.Request(
        f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json", "x-goog-api-key": KEY})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=300) as r:
                d = json.load(r)
            for p in d["candidates"][0]["content"]["parts"]:
                if "inlineData" in p:
                    return base64.b64decode(p["inlineData"]["data"]), p["inlineData"].get("mimeType", "")
            raise RuntimeError("no image in response: " + json.dumps(d)[:400])
        except urllib.error.HTTPError as e:
            print("HTTP", e.code, e.read().decode()[:300], file=sys.stderr)
            if e.code in (429, 500, 503):
                time.sleep(10 * (attempt + 1)); continue
            raise
    raise RuntimeError("generation failed")


if __name__ == "__main__":
    src, prefix, pose = sys.argv[1:4]
    model = sys.argv[4] if len(sys.argv) > 4 else "gemini-3-pro-image"
    data, mime = generate(src, pose, model)
    ext = "png" if "png" in mime else "jpg"
    path = f"{prefix}-{pose}.{ext}"
    open(path, "wb").write(data)
    print("ok", path, mime)
