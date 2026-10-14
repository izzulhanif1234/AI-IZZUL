"""Malay TTS (edge-tts ms-MY-OsmanNeural) with word timings.
usage: tts.py lines.json outdir   (lines.json: [{"id":..,"text":..,"rate":"+0%"}])"""
import asyncio, json, os, sys
import edge_tts

VOICE = "ms-MY-OsmanNeural"


async def one(line, outdir):
    c = edge_tts.Communicate(line["text"], VOICE, rate=line.get("rate", "+0%"), pitch=line.get("pitch", "+0Hz"),
                             boundary="WordBoundary", proxy=os.environ.get("HTTPS_PROXY"))
    words = []
    with open(f"{outdir}/{line['id']}.mp3", "wb") as f:
        async for ch in c.stream():
            if ch["type"] == "audio":
                f.write(ch["data"])
            elif ch["type"] == "WordBoundary":
                words.append({"start": round(ch["offset"] / 1e7, 3), "end": round((ch["offset"] + ch["duration"]) / 1e7, 3), "word": ch["text"]})
    json.dump(words, open(f"{outdir}/{line['id']}.json", "w"), ensure_ascii=False)


async def main():
    lines = json.load(open(sys.argv[1]))
    os.makedirs(sys.argv[2], exist_ok=True)
    for l in lines:
        await one(l, sys.argv[2])
        print("ok", l["id"])

asyncio.run(main())
