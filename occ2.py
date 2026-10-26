from PIL import Image
import numpy as np
from scipy.ndimage import gaussian_filter
a=np.asarray(Image.open('assets/t26/1/out-0.webp').convert('RGB')).astype(float)
lum=a.mean(2); d=lum-gaussian_filter(lum,5)
print(np.percentile(d[722:836,562:644],[5,25,50,75,95]))
v=np.clip(128+d*4,0,255).astype('uint8')
Image.fromarray(v).crop((540,700,680,860)).resize((560,640),Image.LANCZOS).save('assets/occ_d.png')
