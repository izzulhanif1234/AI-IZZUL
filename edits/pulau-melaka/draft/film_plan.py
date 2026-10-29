"""Build the draft-3 film plan (v2: drone-montage hook, no quiz, overlapping transitions).

Writes draft/film-plan.js (scene schedule, island copy, clip windows, SFX cues) and extracts the
frames each clip window needs from the source videos into draft/clips/<island>_<slot>/NNNNN.jpg,
sampled at the preview frame rate with the clip's speed-up already applied.

usage: python3 film_plan.py [--no-extract | --only key,key]
"""
import glob
import json
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, '..', '..', '..', 'media', 'pulau', 'src', 'GUGUSAN PULAU-PULAU MELAKA')
FPS = 30   # matches the sources (30 fps, or 60 fps that halves cleanly); 25 fps caused uneven cadence

CUTS = json.load(open(os.path.join(HERE, '..', 'cuts.json')))

# island copy (concise, from the source document) and per-island treatment
ISL = {
    'masjid':   dict(n='MASJID', z='u', t='Pulau paling utara, bersempadan Negeri Sembilan.', f=['Mukim Kuala Linggi, Alor Gajah', '0.61 ekar · barat Tanjung Tuan']),
    'keramat':  dict(n='KERAMAT', z='u', t='Boleh berjalan kaki ke pulau ketika air surut.', f=['±50 m dari Pulau Konet', '5 kubur lama pedagang Arab / ulama Aceh']),
    'konet':    dict(n='KONET', z='u', t='Beting pasir muncul ketika air surut.', f=['Nama asal: Pulau Kenit', 'Laluan pasir dari tanah besar'],
                     dyk=['Legenda orang bunian', 'Penduduk kampung dikatakan meminjam pinggan mangkuk bunian untuk kenduri.']),
    'upeh':     dict(n='UPEH', z='t', t='Rumah penyu karah di Melaka.', f=[],
                     dyk=['Penyu karah bertelur di sini', 'Antara tapak sarang utama penyu karah, spesies yang jarang ditemui.']),
    'melaka':   dict(n='MELAKA', z='t', t='Batu lateritnya membina A’Famosa.', f=['Portugis: “Ilha das Pedras”', 'Ditambak sejak 2013'], chain=True),
    'panjang':  dict(n='PANJANG', z='t', t='Dinamakan sempena bentuknya yang memanjang.', f=['2.17 hektar', 'Boya panduan untuk nelayan']),
    'menatang': dict(n='MENATANG', z='t', t='Air pasang: dua pulau. Air surut: satu pulau.', f=['Berhampiran Teluk Mas', 'Kutip kerang & siput ketika surut']),
    'burung':   dict(n='BURUNG', z='t', t='Satu pulau yang “terbelah dua” oleh pasang surut.', f=['Pulau Burung Ibu & Anak Burung', 'Portugis: “Pulo Buron”'],
                     dyk=['Batu laterit berpahat', 'Dipahat penduduk untuk batu nisan & alas tiang masjid.']),
    'peringgi': dict(n='PERINGGI', z='t', t='“Peringgi”: gelaran nelayan untuk orang Portugis.', f=['Pulau kecil dikelilingi batu', 'Berhampiran Pulau Burung']),
    'besar':    dict(n='BESAR', z='s', t='Antara pusat terawal penyebaran Islam di Nusantara.', f=[], here=True),
    'serimbun': dict(n='SERIMBUN', z='s', t='', f=[]),
    'hanyut':   dict(n='HANYUT', z='s', t='Dari jauh, seperti daratan yang hanyut.', f=['1.8 hektar', '4.5 km dari Pulau Undan']),
    'lalang':   dict(n='LALANG', z='s', t='Pasir putih, pohon nyiur & pokok ±3,000 tahun.', f=['Portugis: “Alan-Alan”']),
    'dodol':    dict(n='DODOL', z='s', t='Bentuknya seakan-akan kuih dodol.', f=[]),
    'nangka':   dict(n='NANGKA', z='s', t='Berbentuk buah nangka, pokok berusia 400 tahun.', f=['11.76 hektar', 'Bukit setinggi 50 m'],
                     dyk=['Pokok tertua di pulau', 'Sebesar lapan depa dan dianggarkan berusia 400 tahun.']),
    'undan':    dict(n='UNDAN', z='s', t='', f=['Rumah api zaman British', 'Nama sempena burung undan'],
                     dyk=['3 penjaga rumah api', 'Bergilir-gilir setiap 3 minggu, memantau kapal di Selat Melaka.']),
}
# pin centres on the HD poster (2394 x 3263)
PIN = {'masjid': (89, 624), 'keramat': (454, 755), 'konet': (606, 989), 'upeh': (850, 1330), 'melaka': (1229, 1532),
       'panjang': (1352, 1718), 'menatang': (1683, 1824), 'serimbun': (1207, 2049), 'lalang': (1684, 2099),
       'peringgi': (1980, 2210), 'hanyut': (774, 2292), 'burung': (1979, 2360), 'besar': (1440, 2365),
       'dodol': (1515, 2521), 'nangka': (1406, 2710), 'undan': (1227, 2838)}

# AR callouts pinned to features in the footage: island -> (slot, [(label, x, y) on the clip's first frame, in 960x540 units])
# tracks are stored in 1920x1080 units
# the callout clip plays second in the island's segment so it gets the clean middle of the scene
CALL = {
    'masjid': ('A', [('Bot nelayan', 850, 450)]),
    'keramat': ('C', [('Tebing berbatu', 560, 200)]),
    'konet': ('B', [('Beting pasir ketika air surut', 280, 390)]),
    'upeh': ('A', [('Jeti Pulau Upeh', 800, 170)]),
    'melaka': ('A', [('Masjid Selat Melaka', 504, 240)]),
    'panjang': ('A', [('Pulau Panjang', 360, 234)]),
    'menatang': ('B', [('Batu separa tenggelam', 520, 300)]),
    'burung': ('A', [('Pantai berpasir', 600, 400)]),
    'peringgi': ('A', [('Pulau kecil dikelilingi batu', 480, 205)]),
    'besar': ('A', [('Pantai pasir putih', 320, 400)]),
    'serimbun': ('A', [('Bot nelayan', 510, 380)]),
    'hanyut': ('B', [('Batuan & air jernih', 560, 330)]),
    'lalang': ('C', [('Pasir putih', 460, 410)]),
    'dodol': ('A', [('Bentuk seakan-akan kuih dodol', 460, 300)]),
    'nangka': ('A', [('Pantai berpasir', 520, 130)]),
    'undan': ('A', [('Rumah api zaman British', 360, 120),
                    ('Beting pasir 70 m yang menghubungkan pulau utama dengan pulau kecil. Bentuknya berubah ikut arus laut.', 480, 405, 'TOMBOLO')]),
}


def seq(key):
    slots = ['A', 'B', 'C', 'D'] if 'D' in CUTS[key] else ['A', 'B', 'C']
    c = CALL[key][0]
    rest = [x for x in slots if x != c]
    return [rest[0], c] + rest[1:]


# film order: (scene, seconds[, island, transition-in])
# islands run ~4 s per cut so every caption stays up long enough to read (boss review)
# every scene overlaps the next by OV seconds so transitions can mix two live videos
OV = 0.6
ORDER = [
    ('hook', 14), ('map', 9), ('zones', 6),
    ('zone', 2.4, 'u'), ('island', 12, 'masjid', 'zoom'), ('island', 12, 'keramat', 'topo'), ('island', 12, 'konet', 'pin'),
    ('zone', 2.4, 't'), ('island', 12, 'upeh', 'zoom'), ('island', 13.5, 'melaka', 'mask'), ('island', 12, 'panjang', 'slats'),
    ('island', 12, 'menatang', 'whip'), ('island', 12, 'burung', 'cube'), ('island', 12, 'peringgi', 'wave'),
    ('zone', 2.4, 's'), ('island', 16, 'besar', 'zoom'), ('island', 12, 'serimbun', 'split'), ('island', 12, 'hanyut', 'lens'),
    ('island', 12, 'lalang', 'topo'), ('island', 12, 'dodol', 'slats'), ('island', 12, 'nangka', 'whip'), ('island', 13.5, 'undan', 'cube'),
    ('close', 8),
]
# hook montage: whole-island drone shots, (island, slot, offset into the cut)
HOOK = [('masjid', 'B', 2), ('keramat', 'A', 2), ('konet', 'A', 1), ('upeh', 'A', 2), ('melaka', 'A', 2), ('panjang', 'B', 3),
        ('menatang', 'B', 2), ('burung', 'B', 2), ('peringgi', 'C', 3), ('besar', 'C', 2), ('serimbun', 'C', 2), ('hanyut', 'B', 2),
        ('lalang', 'A', 2), ('dodol', 'A', 1), ('nangka', 'B', 2), ('undan', 'B', 2)]
H_START, H_CUT = 0.6, 0.6          # 12 single cuts of 0.6 s, then a 4-up grid of the last four
H_GRID = H_START + 12 * H_CUT       # 7.8
H_GRID_DUR = 1.6
H_MOS = H_GRID + H_GRID_DUR         # 9.4


def clip(key, slot, t0, vis, src0, src_len, out=None, max_speed=1.0, w=1920):
    # real-time playback: speeding drone footage up made every frame a big jump and looked choppy
    speed = min(max_speed, max(1.0, src_len / vis))
    return dict(key=out or key, src_key=key, slot=slot, t0=round(t0, 3), dur=round(vis, 3), src=src0, speed=round(speed, 3),
                n=int(round(vis * FPS)) + 1, w=w)


def plan():
    t, scenes, clips, sfx, n = 0.0, [], [], [], 0
    for row in ORDER:
        kind, dur = row[0], row[1]
        sc = dict(kind=kind, t0=round(t, 3), dur=dur)
        if kind == 'zone':
            sc['zone'] = row[2]
            sfx += [(t, 'whoosh-cinematic'), (t + .2, 'impact-bass-2')]
        elif kind == 'island':
            key, tr = row[2], row[3]
            n += 1
            slots = seq(key)
            edges = [0] + [round(dur * (i + 1) / len(slots), 3) for i in range(len(slots) - 1)] + [dur + OV]
            sc.update(key=key, tr=tr, num=n, cuts=edges, seq=slots, call=CALL[key])
            for i, slot in enumerate(slots):
                s0, s1 = CUTS[key][slot]
                clips.append(clip(key, slot, t + edges[i], edges[i + 1] - edges[i], s0, s1 - s0))
            sfx += [(t, {'zoom': 'whoosh-cinematic', 'wave': 'whoosh', 'pin': 'whoosh-short', 'slats': 'whoosh-short', 'whip': 'whoosh',
                         'cube': 'whoosh', 'mask': 'whoosh-cinematic', 'split': 'whoosh-short', 'lens': 'whoosh-cinematic',
                         'topo': 'sparkle'}[tr]),
                    (t + .5, 'impact-bass-1'), (t + edges[1] + .3, 'pop'), (t + edges[1] + .55, 'pop')]
            if 'dyk' in ISL[key] or 'chain' in ISL[key] or 'here' in ISL[key]:
                sfx.append((t + edges[2] + .2, 'sparkle'))
            if tr == 'slats':
                sfx += [(t + .08 * i, 'click') for i in range(4)]
        elif kind == 'hook':
            for i, (k, sl, off) in enumerate(HOOK[:12]):
                s0 = CUTS[k][sl][0] + off
                clips.append(clip(k, sl, H_START + i * H_CUT, H_CUT, s0, 1.0, out='hook-' + k))
                sfx.append((H_START + i * H_CUT, 'whoosh-short' if i % 2 else 'pop'))
            for k, sl, off in HOOK[12:]:
                s0 = CUTS[k][sl][0] + off
                clips.append(clip(k, sl, H_GRID, H_GRID_DUR, s0, 2.4, out='hook-' + k, w=960))
            for k, sl, off in HOOK:                      # 4x4 mosaic of every island, playing
                s0 = CUTS[k][sl][0] + off + 1
                clips.append(clip(k, sl, H_MOS, 14 - H_MOS + OV, s0, 6, out='mos-' + k, w=480))
            sfx += [(0.1, 'riser'), (H_GRID, 'impact-bass-1'), (H_GRID + H_GRID_DUR, 'whoosh-cinematic'),
                    (11.4, 'impact-bass-2'), (12.0, 'sparkle'), (13.5, 'riser')]
        elif kind == 'map':
            sfx += [(t, 'impact-bass-1'), (t + .1, 'whoosh-cinematic')] + [(t + 1.6 + i * .16, 'pop') for i in range(16)]
        elif kind == 'zones':
            sfx += [(t + .5 + i * .5, 'whoosh-short') for i in range(3)]
        elif kind == 'close':
            for k, sl, off in HOOK:                      # closing wall plays every island again
                s0 = CUTS[k][sl][0] + off + 2
                clips.append(clip(k, sl, t, dur, s0, dur * 1.3, out='wall-' + k, w=480))
            sfx += [(t, 'whoosh'), (t + 1.2, 'impact-bass-2'), (t + 4.5, 'sparkle')]
        scenes.append(sc)
        t += dur
    return dict(fps=FPS, total=round(t, 3), ov=OV, scenes=scenes, clips=clips, isl=ISL, pin=PIN, hook=HOOK,
                hgrid=[H_START, H_CUT, H_GRID, H_GRID_DUR], sfx=[(round(a, 3), b) for a, b in sorted(sfx)])


def source(key):
    for f in glob.glob(os.path.join(SRC, '*.mp4')):
        b = os.path.basename(f).lower()
        if b.startswith('pulau ' + key):
            return f
    raise SystemExit('no source for ' + key)


def track(p):
    """Follow each callout point through its clip frames with template matching (positions in 960x540)."""
    import cv2
    out = {}
    for key, (slot, pts) in CALL.items():
        d = os.path.join(HERE, 'clips', f'{key}_{slot}')
        files = sorted(os.listdir(d))
        tracks = []
        k = 1920 / 960
        for _, x, y, *_ in pts:
            x, y = x * k, y * k
            prev = cv2.cvtColor(cv2.imread(os.path.join(d, files[0])), cv2.COLOR_BGR2GRAY)
            r, sr, path = 56, 110, [(x, y)]
            for f in files[1:]:
                cur = cv2.cvtColor(cv2.imread(os.path.join(d, f)), cv2.COLOR_BGR2GRAY)
                H, W = cur.shape
                cx, cy = int(round(path[-1][0])), int(round(path[-1][1]))
                tx0, ty0 = max(0, cx - r), max(0, cy - r)
                tpl = prev[ty0:min(H, cy + r), tx0:min(W, cx + r)]
                sx0, sy0 = max(0, cx - r - sr), max(0, cy - r - sr)
                win = cur[sy0:min(H, cy + r + sr), sx0:min(W, cx + r + sr)]
                if tpl.shape[0] < 8 or tpl.shape[1] < 8 or win.shape[0] <= tpl.shape[0] or win.shape[1] <= tpl.shape[1]:
                    path.append(path[-1]); prev = cur; continue
                m = cv2.matchTemplate(win, tpl, cv2.TM_CCOEFF_NORMED)
                _, score, _, loc = cv2.minMaxLoc(m)
                nx, ny = sx0 + loc[0] + (cx - tx0), sy0 + loc[1] + (cy - ty0)
                path.append((nx, ny) if score > .4 else path[-1])
                prev = cur
            tracks.append([[round(a, 1), round(b, 1)] for a, b in path])
        out[f'{key}_{slot}'] = tracks
        print('track', key, slot, len(files), 'frames', flush=True)
    return out


def stutter(src, ss, t):
    """Share of repeated frames when the window is read at FPS, ignoring near-static footage."""
    import numpy as np
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', str(ss), '-t', str(t), '-i', src,
                          '-vf', f'fps={FPS},scale=240:135,format=gray', '-f', 'rawvideo', '-'], capture_output=True).stdout
    fr = np.frombuffer(raw, np.uint8).reshape(-1, 135, 240).astype(np.int16)
    if len(fr) < 3:
        return 0.0
    d = np.abs(np.diff(fr, axis=0)).mean(axis=(1, 2))
    moving = d > .15
    if moving.mean() < .2:                   # essentially a still shot: nothing to smooth
        return 0.0
    return float((d < .15).mean())


def extract_one(c):
    d = os.path.join(HERE, 'clips', f"{c['key']}_{c['slot']}")
    os.makedirs(d, exist_ok=True)
    src = source(c['src_key'])
    # Upeh's source carries a small corner watermark: crop from the bottom-left before scaling
    crop = 'crop=iw*0.88:ih*0.88:0:ih*0.12,' if c['src_key'] == 'upeh' else ''
    # several sources hold low-frame-rate footage padded with repeated frames: drop the repeats and
    # motion-interpolate back to FPS so pans move evenly
    c['interp'] = stutter(src, c['src'], c['dur'] * c['speed']) > .12
    rate = (f'mpdecimate=hi=768:lo=320:frac=0.33,minterpolate=fps={FPS}:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1'
            if c['interp'] else f'fps={FPS}')
    vf = f"setpts=PTS/{c['speed']},{rate},{crop}scale={c['w']}:{c['w'] * 9 // 16}"
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(c['src']), '-t', str(c['dur'] * c['speed'] + .3),
                    '-i', src, '-vf', vf, '-frames:v', str(c['n']), '-q:v', '4',
                    os.path.join(d, '%05d.jpg')], check=True)  # -q:v 4 keeps 1080p frames small
    c['n'] = len(os.listdir(d))
    print(c['key'], c['slot'], c['n'], 'frames', 'interp' if c['interp'] else '', flush=True)


def extract(p, only=None):
    from concurrent.futures import ThreadPoolExecutor
    todo = p['clips']
    if only:
        todo = [c for c in todo if c['key'] in only]
        for c in todo:
            shutil.rmtree(os.path.join(HERE, 'clips', f"{c['key']}_{c['slot']}"), ignore_errors=True)
        for c in p['clips']:                 # untouched clips keep their extracted frame count
            d = os.path.join(HERE, 'clips', f"{c['key']}_{c['slot']}")
            if c not in todo and os.path.isdir(d):
                c['n'] = len(os.listdir(d))
    else:
        shutil.rmtree(os.path.join(HERE, 'clips'), ignore_errors=True)
    with ThreadPoolExecutor(4) as ex:
        list(ex.map(extract_one, todo))


if __name__ == '__main__':
    p = plan()
    only = sys.argv[sys.argv.index('--only') + 1].split(',') if '--only' in sys.argv else None
    if '--no-extract' not in sys.argv:
        extract(p, only)
    p['tracks'] = track(p)
    with open(os.path.join(HERE, 'film-plan.js'), 'w') as fh:
        fh.write('window.PLAN=' + json.dumps(p, ensure_ascii=False) + ';\n')
    print('total', p['total'], 's,', len(p['clips']), 'clips,', len(p['sfx']), 'sfx cues')
