import numpy as np
from PIL import Image
exec(open('stern3.py').read().split('N=256')[0])
N=512
s=stern(2*N+5)
i,j=np.meshgrid(np.arange(1,N+1),np.arange(1,N+1),indexing='ij')
v=s[i^j]
pal=np.array([[245,236,214],[226,130,50],[176,44,40],[40,120,125],[24,36,84]],np.uint8)  # cream orange red teal navy
img=pal[np.minimum(v,5)-1]
Image.fromarray(img).resize((1536,1536),Image.NEAREST).save('assets/s4_xor_cap.png')
v3=v%3
pal3=np.array([[245,236,214],[176,44,40],[24,36,84]],np.uint8)
Image.fromarray(pal3[v3]).resize((1536,1536),Image.NEAREST).save('assets/s4_xor_m3.png')
print(np.bincount(np.minimum(v.ravel(),5)))
pal6=np.vstack([[[10,12,24]],pal]).astype(np.uint8)  # index 0 = s(0)=0
img=pal6[np.minimum(v,5)]
Image.fromarray(img).resize((1536,1536),Image.NEAREST).convert('RGB').save('assets/s4_full.jpg',quality=90)
Image.fromarray(img[:128,:128]).resize((1024,1024),Image.NEAREST).convert('RGB').save('assets/s4_crop.jpg',quality=92)
# claims
print('navy share',(v>=5).mean(), 'cream cells', (v==1).sum())
# long runs: longest same-colour run along anti-diag? longest run of cream along a diagonal
