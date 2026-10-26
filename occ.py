from PIL import Image, ImageDraw
import numpy as np
from scipy.ndimage import gaussian_filter, binary_dilation
im=Image.open('assets/t26/1/out-0.webp').convert('RGB'); a=np.asarray(im).astype(float)
poly=[(566,826),(562,770),(576,735),(600,722),(630,738),(644,775),(642,826),(610,836)]
pm=Image.new('L',im.size,0); ImageDraw.Draw(pm).polygon(poly,fill=255); pm=np.asarray(pm)>0
lum=a.mean(2); d=lum-gaussian_filter(lum,5)
m=binary_dilation(pm&(d>22),iterations=1).astype(float); m=gaussian_filter(m,0.5)
np.save('assets/occ.npy',m)
