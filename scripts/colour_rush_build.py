"""Colour Rush tee ad: write the music beat grid into hf/index.html and derive the 9:16
project (hf-916/) from the same composition. The composition reads its layout from the
root's data-width/data-height (class "v" switches the CSS to the vertical layout).
usage: colour_rush_build.py edits/colour-rush-ad"""
import json
import os
import re
import shutil
import sys

base = sys.argv[1]
hf = os.path.join(base, "hf")
v = os.path.join(base, "hf-916")
src_path = os.path.join(hf, "index.html")
grid = json.load(open(os.path.join(hf, "assets/bgm/beats.json")))

src = open(src_path).read()
src = re.sub(r"const BEATS = \[[^\]]*\];", f"const BEATS = {json.dumps(grid['beats'])};", src)
src = re.sub(r"const DOWNBEATS = \[[^\]]*\];", f"const DOWNBEATS = {json.dumps(grid['downbeats'])};", src)
open(src_path, "w").write(src)

vert = src
for a, b in [
    ('content="width=1920, height=1080"', 'content="width=1080, height=1920"'),
    ('data-width="1920" data-height="1080"', 'data-width="1080" data-height="1920"'),
    ('<div id="root" data-composition-id', '<div id="root" class="v" data-composition-id'),
]:
    assert vert.count(a) == 1, a
    vert = vert.replace(a, b)
# html/body and #root boxes
n = len(re.findall(r"width: 1920px;\n(\s+)height: 1080px;", vert))
assert n == 3, n  # html/body, #root, #cam
vert = re.sub(r"width: 1920px;\n(\s+)height: 1080px;", r"width: 1080px;\n\1height: 1920px;", vert)

os.makedirs(v, exist_ok=True)
open(os.path.join(v, "index.html"), "w").write(vert)
for f in ("package.json", "hyperframes.json", "CLAUDE.md", "AGENTS.md"):
    shutil.copy(os.path.join(hf, f), os.path.join(v, f))
meta = json.load(open(os.path.join(hf, "meta.json")))
meta.update(id=meta["id"] + "-916", name=meta["name"] + " (9:16)")
json.dump(meta, open(os.path.join(v, "meta.json"), "w"), indent=2)
for d in ("assets", "vendor"):  # share the 16:9 project's assets
    link = os.path.join(v, d)
    if not os.path.lexists(link):
        os.symlink(os.path.join("..", "hf", d), link)
print("wrote", v)
