"""Hand-placed SAM prompts for regions the automatic pass missed. Writes chair_<n>x.png and body_<n>x.png."""
import sys, json, numpy as np
from PIL import Image
from samchairs import sam_crop
n, spec = sys.argv[1], json.loads(sys.argv[2])
im = np.asarray(Image.open(f'../dl/orig_{n}.bin').convert('RGB'))
H, W = im.shape[:2]
x0, y0, cw, chh = spec['box']
crop = im[y0:y0 + chh, x0:x0 + cw]
rel = lambda pts: [(float(x - x0), float(y - y0)) for x, y in pts]
for kind in ('chair', 'body'):
    neg = spec['chair'] if kind == 'body' else spec['body']
    logit = sam_crop(crop, rel(spec[kind]), rel(neg + spec.get('neg', [])))
    out = np.zeros((H, W), np.float32)
    out[y0:y0 + chh, x0:x0 + cw] = 1 / (1 + np.exp(-logit))
    print(kind, int((out > .5).sum()))
    Image.fromarray((out * 255).astype(np.uint8)).save(f'{kind}_{n}x.png')
