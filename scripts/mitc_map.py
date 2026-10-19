"""Dark corporate map of Ayer Keroh from OpenStreetMap tiles, with the real toll -> hotel route.

usage: python3 scripts/mitc_map.py TILES_DIR ROUTE_JSON HF_DIR

TILES_DIR holds z15 OSM tiles named {z}_{x}_{y}.png plus range.txt ("z x0 x1 y0 y1");
ROUTE_JSON is an OSRM /route response (geometries=geojson) from the PLUS Air Keroh toll to the hotel.
Writes HF_DIR/assets/img/map-ayerkeroh.jpg (1500x820, the map panel size) and HF_DIR/assets/map.json
with every point in panel pixels.  Map data (c) OpenStreetMap contributors.
"""
import json
import math
import os
import subprocess
import sys

from PIL import Image

TILES, ROUTE, HF = sys.argv[1], sys.argv[2], sys.argv[3]
PW, PH = 1500, 820
POINTS = {                      # from Nominatim
    "toll": (2.30035, 102.31045),   # Plaza Toll PLUS Air Keroh
    "hotel": (2.27335, 102.28474),  # MITC Hotel Melaka
    "mitc": (2.27172, 102.28452),   # Pusat Perdagangan Antarabangsa Melaka (MITC)
}

z, x0, x1, y0, y1 = map(int, open(os.path.join(TILES, "range.txt")).read().split())


def px(lat, lon):
    n = 2 ** z * 256
    x = (lon + 180) / 360 * n
    y = (1 - math.log(math.tan(math.radians(lat)) + 1 / math.cos(math.radians(lat))) / math.pi) / 2 * n
    return x - x0 * 256, y - y0 * 256


mosaic = Image.new("RGB", ((x1 - x0) * 256, (y1 - y0) * 256))
for x in range(x0, x1):
    for y in range(y0, y1):
        mosaic.paste(Image.open(os.path.join(TILES, f"{z}_{x}_{y}.png")).convert("RGB"), ((x - x0) * 256, (y - y0) * 256))

# crop: toll and hotel inside with margins, panel aspect; hotel kept clear of the title (top-left)
(tx, ty), (hx, hy) = px(*POINTS["toll"]), px(*POINTS["hotel"])
cx, cy = (tx + hx) / 2, (ty + hy) / 2 + 20
ch = abs(hy - ty) + 300
cw = ch * PW / PH
box = (int(cx - cw / 2), int(cy - ch / 2), int(cx + cw / 2), int(cy + ch / 2))
crop = mosaic.crop(box).resize((PW, PH), Image.LANCZOS)
s = PW / (box[2] - box[0])

raw = os.path.join(HF, "assets", "img", "_map_raw.png")
out = os.path.join(HF, "assets", "img", "map-ayerkeroh.jpg")
crop.save(raw)
# navy "dark mode": grey -> negative -> map onto navy..periwinkle
subprocess.run(["convert", raw, "-colorspace", "Gray", "-negate", "-level", "12%,88%", "-gamma", "0.8",
                "-colorspace", "sRGB", "+level-colors", "#06112f,#b8c8f5", "-quality", "90", out], check=True)
os.remove(raw)


def panel(lat, lon):
    x, y = px(lat, lon)
    return round((x - box[0]) * s, 1), round((y - box[1]) * s, 1)


route = json.load(open(ROUTE))["routes"][0]
pts = [panel(lat, lon) for lon, lat in route["geometry"]["coordinates"]]
length = sum(math.dist(a, b) for a, b in zip(pts, pts[1:]))
mid = pts[len(pts) // 2]
data = {"toll": panel(*POINTS["toll"]), "hotel": panel(*POINTS["hotel"]), "mitc": panel(*POINTS["mitc"]),
        "route": pts, "route_len": round(length + 4), "route_mid": mid,
        "km": round(route["distance"] / 1000, 1), "box": box, "scale": s}
json.dump(data, open(os.path.join(HF, "assets", "map.json"), "w"))
print("crop", box, "scale", round(s, 3), "toll", data["toll"], "hotel", data["hotel"], "mitc", data["mitc"], "km", data["km"])
