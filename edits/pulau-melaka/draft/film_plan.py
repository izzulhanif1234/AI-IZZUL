"""Build the 3-minute draft-3 film plan.

Writes draft/film-plan.js (scene schedule, island copy, clip windows, SFX cues) and extracts the
frames each clip window needs from the source videos into draft/clips/<island>_<slot>/NNNNN.jpg,
sampled at the preview frame rate with the clip's speed-up already applied.

usage: python3 film_plan.py [--no-extract]
"""
import glob
import json
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, '..', '..', '..', 'media', 'pulau', 'src', 'GUGUSAN PULAU-PULAU MELAKA')
FPS = 20

CUTS = json.load(open(os.path.join(HERE, '..', 'cuts.json')))

# island copy (concise, from the source document) and per-island treatment
ISL = {
    'masjid':   dict(n='MASJID', z='u', t='Pulau paling utara, bersempadan Negeri Sembilan.', f=['Mukim Kuala Linggi, Alor Gajah', '0.61 ekar · barat Tanjung Tuan']),
    'keramat':  dict(n='KERAMAT', z='u', t='Boleh berjalan kaki ke pulau ketika air surut.', f=['±50 m dari Pulau Konet', '5 kubur lama pedagang Arab / ulama Aceh']),
    'konet':    dict(n='KONET', z='u', t='Beting pasir muncul ketika air surut.', f=['Nama asal: Pulau Kenit', 'Laluan pasir dari tanah besar'],
                     dyk=['Legenda orang bunian', 'Penduduk kampung dikatakan meminjam pinggan mangkuk bunian untuk kenduri.']),
    'upeh':     dict(n='UPEH', z='t', t='Rumah penyu karah di Melaka.', f=['±3 batu ke barat Bukit St. Paul', 'Hutan tebal, pokok setinggi 34 m'],
                     dyk=['Penyu karah bertelur di sini', 'Antara tapak sarang utama penyu karah, spesies yang jarang ditemui.']),
    'melaka':   dict(n='MELAKA', z='t', t='Batu lateritnya membina A’Famosa.', f=['Portugis: “Ilha das Pedras”', 'Ditambak sejak 2013'], chain=True),
    'panjang':  dict(n='PANJANG', z='t', t='Dinamakan sempena bentuknya yang memanjang.', f=['2.17 hektar', 'Boya panduan untuk nelayan']),
    'menatang': dict(n='MENATANG', z='t', t='Air pasang: dua pulau. Air surut: satu pulau.', f=['Berhampiran Teluk Mas', 'Kutip kerang & siput ketika surut']),
    'burung':   dict(n='BURUNG', z='t', t='Satu pulau yang “terbelah dua” oleh pasang surut.', f=['Pulau Burung Ibu & Anak Burung', 'Portugis: “Pulo Buron”'],
                     dyk=['Batu laterit berpahat', 'Dipahat penduduk untuk batu nisan & alas tiang masjid.']),
    'peringgi': dict(n='PERINGGI', z='t', t='“Peringgi”: gelaran nelayan untuk orang Portugis.', f=['Pulau kecil dikelilingi batu', 'Berhampiran Pulau Burung']),
    'besar':    dict(n='BESAR', z='s', t='Antara pusat terawal penyebaran Islam di Nusantara.', f=['Bentuk seperti puteri tidur', 'Abad ke-15'], here=True),
    'serimbun': dict(n='SERIMBUN', z='s', t='Tapak perkhemahan dengan ±25 spesies karang.', f=['20 karang keras + 5 lembut', 'Tempat nelayan berlindung']),
    'hanyut':   dict(n='HANYUT', z='s', t='Dari jauh, seperti daratan yang hanyut.', f=['1.8 hektar', '4.5 km dari Pulau Undan']),
    'lalang':   dict(n='LALANG', z='s', t='Pasir putih, pohon nyiur & pokok ±3,000 tahun.', f=['Portugis: “Alan-Alan”', 'Air surut: jalan kaki ke Pulau Terendak']),
    'dodol':    dict(n='DODOL', z='s', t='Bentuknya seakan-akan kuih dodol.', f=['6.34 hektar', '18 spesies karang']),
    'nangka':   dict(n='NANGKA', z='s', t='Berbentuk buah nangka, pokok berusia 4,000 tahun.', f=['11.76 hektar', 'Bukit setinggi 50 m'],
                     dyk=['Pokok tertua di pulau', 'Sebesar empat pemeluk dan dianggarkan berusia 4,000 tahun.']),
    'undan':    dict(n='UNDAN', z='s', t='Karang “Table Top” terbesar dari Selangor hingga Johor Barat.', f=['Rumah api zaman British', 'Nama sempena burung undan'],
                     dyk=['3 penjaga rumah api', 'Bergilir-gilir setiap 3 minggu, memantau kapal di Selat Melaka.']),
}
# pin centres on the HD poster (2394 x 3263)
PIN = {'masjid': (89, 624), 'keramat': (454, 755), 'konet': (606, 989), 'upeh': (850, 1330), 'melaka': (1229, 1532),
       'panjang': (1352, 1718), 'menatang': (1683, 1824), 'serimbun': (1207, 2049), 'lalang': (1684, 2099),
       'peringgi': (1980, 2210), 'hanyut': (774, 2292), 'burung': (1979, 2360), 'besar': (1440, 2365),
       'dodol': (1515, 2521), 'nangka': (1406, 2710), 'undan': (1227, 2838)}

# film order: (scene, seconds[, island, entry])  entry = map | mask | tri | glitch
ORDER = [
    ('hook', 8), ('map', 10), ('zones', 8),
    ('zone', 2, 'u'), ('island', 7.3, 'masjid', 'map'), ('island', 7.3, 'keramat', 'glitch'), ('island', 7.4, 'konet', 'map'),
    ('zone', 2, 't'), ('island', 8, 'upeh', 'mask'), ('island', 10, 'melaka', 'map'), ('island', 8, 'panjang', 'glitch'),
    ('island', 8, 'menatang', 'map'), ('island', 8, 'burung', 'tri'), ('island', 8, 'peringgi', 'map'),
    ('quiz', 8),
    ('zone', 2, 's'), ('island', 12, 'besar', 'map'), ('island', 6.6, 'serimbun', 'glitch'), ('island', 6.6, 'hanyut', 'map'),
    ('island', 6.6, 'lalang', 'mask'), ('island', 6.6, 'dodol', 'tri'), ('island', 6.6, 'nangka', 'glitch'), ('island', 7, 'undan', 'map'),
    ('taman', 8), ('close', 8),
]


def plan():
    t, scenes, clips, sfx, n = 0.0, [], [], [], 0
    for row in ORDER:
        kind, dur = row[0], row[1]
        sc = dict(kind=kind, t0=round(t, 3), dur=dur)
        if kind == 'zone':
            sc['zone'] = row[2]
            sfx += [(t, 'whoosh-cinematic'), (t + .25, 'impact-bass-2')]
        elif kind == 'island':
            key, entry = row[2], row[3]
            n += 1
            e = 1.0 if entry == 'map' else 0.8
            body = dur - e
            a, b = e + .38 * body, e + .70 * body          # A | B | C boundaries (relative)
            sc.update(key=key, entry=entry, num=n, e=e, a=round(a, 3), b=round(b, 3))
            win = {'A': (0 if entry in ('mask', 'tri') else e, a), 'B': (0 if entry == 'tri' else a, b), 'C': (0 if entry == 'tri' else b, dur)}
            for slot, (w0, w1) in win.items():
                src0, src1 = CUTS[key][slot]
                vis = w1 - w0
                speed = min(3.0, max(.8, (src1 - src0) / vis))
                clips.append(dict(key=key, slot=slot, t0=round(t + w0, 3), dur=round(vis, 3), src=src0, speed=round(speed, 3),
                                  n=int(round(vis * FPS)) + 1))
            sfx += [(t, {'map': 'whoosh', 'mask': 'whoosh-cinematic', 'tri': 'whoosh', 'glitch': 'glitch-1'}[entry]),
                    (t + e, 'impact-bass-1'), (t + a + .2, 'pop'), (t + a + .4, 'pop')]
            if 'dyk' in ISL[key] or 'chain' in ISL[key] or 'here' in ISL[key]:
                sfx.append((t + b + .2, 'sparkle'))
        elif kind == 'hook':
            sfx += [(0.3, 'impact-bass-2'), (0.8, 'whoosh-short'), (6.6, 'riser')]
        elif kind == 'map':
            sfx += [(t, 'impact-bass-1'), (t + .1, 'whoosh-cinematic')] + [(t + 1.6 + i * .18, 'pop') for i in range(16)]
        elif kind == 'zones':
            sfx += [(t + .5 + i * .6, 'whoosh-short') for i in range(3)]
        elif kind == 'quiz':
            sfx += [(t, 'notification')] + [(t + 1.5 + i, 'click') for i in range(5)] + [(t + 6.5, 'chime')]
        elif kind == 'taman':
            sfx += [(t, 'whoosh-cinematic')] + [(t + .8 + i * .35, 'whoosh-short') for i in range(3)]
        elif kind == 'close':
            sfx += [(t, 'whoosh'), (t + 1.2, 'impact-bass-2'), (t + 4.5, 'sparkle')]
        scenes.append(sc)
        t += dur
    return dict(fps=FPS, total=round(t, 3), scenes=scenes, clips=clips, isl=ISL, pin=PIN,
                sfx=[(round(a, 3), b) for a, b in sorted(sfx)])


def source(key):
    for f in glob.glob(os.path.join(SRC, '*.mp4')):
        b = os.path.basename(f).lower()
        if b.startswith('pulau ' + key):
            return f
    raise SystemExit('no source for ' + key)


def extract(p):
    root = os.path.join(HERE, 'clips')
    shutil.rmtree(root, ignore_errors=True)
    for c in p['clips']:
        d = os.path.join(root, f"{c['key']}_{c['slot']}")
        os.makedirs(d, exist_ok=True)
        # Upeh's source carries a small corner watermark: crop from the bottom-left before scaling
        crop = 'crop=iw*0.88:ih*0.88:0:ih*0.12,' if c['key'] == 'upeh' else ''
        vf = f"setpts=PTS/{c['speed']},fps={FPS},{crop}scale=960:540"
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(c['src']), '-t', str(c['dur'] * c['speed'] + .3),
                        '-i', source(c['key']), '-vf', vf, '-frames:v', str(c['n']), '-q:v', '4',
                        os.path.join(d, '%05d.jpg')], check=True)
        got = len(os.listdir(d))
        c['n'] = got
        print(c['key'], c['slot'], got, 'frames', flush=True)


if __name__ == '__main__':
    p = plan()
    if '--no-extract' not in sys.argv:
        extract(p)
    with open(os.path.join(HERE, 'film-plan.js'), 'w') as fh:
        fh.write('window.PLAN=' + json.dumps(p, ensure_ascii=False) + ';\n')
    print('total', p['total'], 's,', len(p['clips']), 'clips,', len(p['sfx']), 'sfx cues')
