"""Single source of truth for the MCORP EstiMATE film timeline: VO placement, dialogue cuts,
and caption cues (root seconds). Writes assets/captions.json."""
import json, os, re

ROOT = os.path.dirname(os.path.abspath(__file__))
HF = "/home/user/AI-IZZUL/edits/mcorp-estimate/hf"
TR = "/home/user/AI-IZZUL/media/sistem-full/transcripts"

VO = {  # line id -> audio data-start (root s)
    "v01": 0.30, "v02": 5.90, "v03": 12.55, "v03b": 16.55, "v04": 27.95, "v05": 36.05,
    "v06": 47.85, "v07": 53.55, "v08": 66.55, "v09": 72.05, "v10": 81.05, "v11": 105.95,
}
# dialogue cuts: (clip, root_start, src_start, duration)
DIALOGUE = [
    ("intro2", 21.60, 1.70, 6.25),
    ("rahimah3", 82.60, 16.98, 9.92),
    ("helmy3", 92.60, 2.96, 6.34),
    ("helmy3", 98.94, 19.25, 6.70),
]
# hand-punctuated captions for each dialogue cut (same words as spoken, token count must match)
DIALOGUE_TEXT = [
    "Sekarang dah senang. Masukkan je BQ, skop kerja. Kirakan kos.",
    "Ia sangat membantulah bagi kerja-kerja yang di bawah projek RM500,000. So sangat membantu untuk jabatan kami yang tiada teknikal ni lah.",
    "Dekat bila kita nak terangkan kepada orang awam, penduduk, rakyat. Sebab apa rakyat selalu pertikai, kan? Takkan RM50,000 dapat panjang ni?",
    "Dia bila ada ni, kita boleh tunjukkan kepada dekat mana isu itu sebenar. Jadi dia boleh tengok pecahan-pecahan ni, kat sini yang mahal, kat sini yang murah.",
]
FIX = {"Bintik": "binti", "petikai": "pertikai", "Kos": "kos", "-s": "s", "membantulah": "membantulah"}


SCRIPT = {l["id"]: l["text"] for f in ("script.json", "team.json", "close.json")
          for l in json.load(open(f"/home/user/AI-IZZUL/media/sistem-full/vo/{f}"))}


def vo_words():
    """TTS word timings, re-labelled with the script's own tokens so captions keep punctuation."""
    out = []
    for lid, at in VO.items():
        ws = json.load(open(f"{HF}/assets/vo/{lid}.json"))
        toks = SCRIPT[lid].split()
        use = len(toks) == len(ws)
        for i, w in enumerate(ws):
            # the script spells "M-Corp" so the voice says it right; captions show the brand as written
            word = (toks[i] if use else w["word"]).replace("M-Corp", "MCORP")
            out.append({"s": round(at + w["start"], 3), "e": round(at + w["end"], 3), "w": word, "src": lid})
    return out


def dialogue_words():
    out = []
    for i, (clip, rs, ss, dur) in enumerate(DIALOGUE):
        cut = []
        d = json.load(open(f"{TR}/{clip}.json"))
        for seg in d["segments"]:
            for w in seg["words"]:
                if ss - 0.05 <= w["start"] and w["end"] <= ss + dur + 0.05:
                    word = FIX.get(w["word"], w["word"])
                    cut.append({"s": round(rs + w["start"] - ss, 3), "e": round(rs + w["end"] - ss, 3), "w": word, "src": f"{clip}#{i}"})
        cut = merge_tokens(cut)
        toks = DIALOGUE_TEXT[i].split()
        if len(toks) == len(cut):
            for w, t in zip(cut, toks):
                w["w"] = t
        else:
            print("WARN token mismatch", clip, len(toks), len(cut), [w["w"] for w in cut])
        out += cut
    return out


def merge_tokens(words):
    """Glue whisper sub-tokens ("RM500" ",000" / "kerja" "-kerja" / "GPT" "s") onto the previous word."""
    out = []
    for w in words:
        t = w["w"]
        if out and (t.startswith(",") or t.startswith("-") or t in ("s",)) and w["src"] == out[-1]["src"]:
            out[-1]["w"] += t
            out[-1]["e"] = w["e"]
        else:
            out.append(dict(w))
    return out


def cues(words, max_words=6, max_gap=0.6):
    """Split into phrases (sentence end, comma after 3+ words, long gap, speaker change), then
    split long phrases into even chunks so no cue is a lonely word."""
    phrases, cur = [], []
    for w in words:
        if cur and (w["s"] - cur[-1]["e"] > max_gap or w["src"] != cur[-1]["src"]
                    or re.search(r"[.?!]$", cur[-1]["w"])
                    or (cur[-1]["w"].endswith(",") and len(cur) >= 3)):
            phrases.append(cur); cur = []
        cur.append(w)
    if cur:
        phrases.append(cur)
    # fold a one-word phrase back into its neighbour ("kan?")
    merged = []
    for ph in phrases:
        if merged and len(ph) == 1 and ph[0]["src"] == merged[-1][-1]["src"] and len(merged[-1]) <= 6:
            merged[-1] = merged[-1] + ph
        else:
            merged.append(ph)
    phrases = merged
    res = []
    for ph in phrases:
        n = -(-len(ph) // max_words)
        size = -(-len(ph) // n)
        res += [ph[i:i + size] for i in range(0, len(ph), size)]
    return [{"s": c[0]["s"], "e": round(c[-1]["e"] + 0.15, 3), "words": [{"w": x["w"], "s": x["s"]} for x in c]} for c in res]


if __name__ == "__main__":
    words = sorted(vo_words() + dialogue_words(), key=lambda w: w["s"])
    cs = cues(words)
    # never let a cue overlap the next one
    for a, b in zip(cs, cs[1:]):
        a["e"] = min(a["e"], b["s"] - 0.02)
    json.dump(cs, open(f"{HF}/assets/captions.json", "w"), ensure_ascii=False, indent=0)
    for c in cs:
        print(f'{c["s"]:7.2f}-{c["e"]:7.2f}  ' + " ".join(f'{x["w"]}' for x in c["words"]))
    print(len(cs), "cues")
