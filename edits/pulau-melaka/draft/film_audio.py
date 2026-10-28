"""Mix the draft-3 soundtrack: music bed looped to the film length plus every SFX cue from film-plan.js.
The source videos' own audio is their channel's music, so it is not used.

usage: python3 film_audio.py <out.wav>
"""
import json
import os
import subprocess
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
SR = 48000
BED = os.path.join(HERE, '..', '..', 'mcorp-estimate', 'hf', 'assets', 'bgm', 'bed.wav')
SFX = os.path.join(HERE, '..', '..', 'mcorp-estimate', 'hf', 'assets', 'sfx')

LEVEL = {'whoosh': .4, 'whoosh-short': .35, 'whoosh-cinematic': .3, 'impact-bass-1': .28, 'impact-bass-2': .3,
         'pop': .35, 'glitch-1': .45, 'sparkle': .4, 'riser': .5, 'notification': .5, 'click': .4, 'chime': .6}


def load(path, ss=None, t=None):
    cmd = ['ffmpeg', '-v', 'error']
    if ss is not None:
        cmd += ['-ss', str(ss), '-t', str(t)]
    cmd += ['-i', path, '-f', 'f32le', '-ac', '2', '-ar', str(SR), '-']
    a = np.frombuffer(subprocess.run(cmd, capture_output=True, check=True).stdout, np.float32)
    return a.reshape(-1, 2).copy()


def main(out):
    P = json.loads(open(os.path.join(HERE, 'film-plan.js')).read()[len('window.PLAN='):-2])
    n = int(P['total'] * SR) + SR
    mix = np.zeros((n, 2), np.float32)

    # music bed, looped with a 2 s crossfade, faded in/out
    bed = load(BED)
    music = np.zeros((n, 2), np.float32)
    pos, xf = 0, 2 * SR
    while pos < n:
        seg = bed[:min(len(bed), n - pos)].copy()
        if pos:
            ramp = np.linspace(0, 1, min(xf, len(seg)))[:, None]
            seg[:len(ramp)] *= ramp
            music[pos:pos + len(ramp)] *= (1 - ramp)
        music[pos:pos + len(seg)] += seg
        pos += len(bed) - xf
    music[:SR] *= np.linspace(0, 1, SR)[:, None]
    end = int(P['total'] * SR)
    music[end - 3 * SR:end] *= np.linspace(1, 0, 3 * SR)[:, None]
    music[end:] = 0
    mix += music * 1.0

    # SFX cues
    cache = {}
    for t, name in P['sfx']:
        if name not in cache:
            cache[name] = load(os.path.join(SFX, name + '.mp3'))
        a = cache[name] * LEVEL.get(name, .5)
        i0 = int(t * SR)
        j = min(n, i0 + len(a))
        mix[i0:j] += a[:j - i0]

    mix = mix[:end]
    peak = np.abs(mix).max()
    if peak > .98:
        mix *= .98 / peak
    tmp = out + '.raw'
    mix.astype(np.float32).tofile(tmp)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'f32le', '-ar', str(SR), '-ac', '2', '-i', tmp,
                    '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11', '-ar', str(SR), out], check=True)
    os.remove(tmp)
    print('wrote', out, round(len(mix) / SR, 2), 's')


if __name__ == '__main__':
    main(sys.argv[1])
