set -e
n=$1
ex=""; [ "$n" = 06 -o "$n" = 07 ] && ex="chair_${n}x.png"
python3 merge3.py ../dl/orig_$n.bin pm_$n.png mc_$n.png m3_$n.png $ex
python3 refine.py ../dl/orig_$n.bin pm_$n.png m3_$n.png m4_$n.png
python3 -c "
import numpy as np,cv2; from PIL import Image
b=np.asarray(Image.open('br_$n.png')).astype(np.float32)/255
k,l,st,_=cv2.connectedComponentsWithStats((b>0.1).astype(np.uint8),8)
for i in range(1,k):
  if st[i][0]+st[i][2]>1500: b[l==i]=0
b=cv2.GaussianBlur(b,(0,0),0.7)
f=np.asarray(Image.open('m4_$n.png')).astype(np.float32)/255
Image.fromarray((np.maximum(f,b)*255+.5).astype(np.uint8)).save('m5_$n.png')"
python3 darkfill.py ../dl/orig_$n.bin m5_$n.png m6_$n.png >/dev/null
python3 studio.py ../dl/orig_$n.bin m6_$n.png v$n.jpg >/dev/null
