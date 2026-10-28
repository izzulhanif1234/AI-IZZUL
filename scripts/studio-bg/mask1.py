import sys
from rembg import new_session, remove
from PIL import Image
m = remove(Image.open(sys.argv[1]).convert('RGB'), session=new_session('birefnet-general'), only_mask=True)
m.save(sys.argv[2])
