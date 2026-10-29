import numpy as np
from PIL import Image
from floats import *
from scipy.ndimage import binary_dilation
C=8
def panel(t):
    f=np.cos(t)*a+np.sin(t)*b
    o=np.where(f>0,Z,S); wf,ef=stats(o)
    seam=np.zeros_like(o)
    sg=f>0
    seam[:-1]|=sg[:-1]!=sg[1:]; seam[:,:-1]|=sg[:,:-1]!=sg[:,1:]
    near=binary_dilation(seam,iterations=2)
    longc=(wf>2)|(ef>2)
    print(round(np.degrees(t)),'long cells',longc.sum(),'near seam',(longc&near).sum(),'seam-near share of all cells',round(near.mean(),3),'max',wf.max(),ef.max())
    img=np.where(o[...,None],np.array([30,40,70.]),np.array([70,66,58.]))
    img=np.repeat(np.repeat(img,C,0),C,1)
    # long floats bright
    big=np.zeros((N*C,N*C,3))
    for m,col in ((wf>2,(255,90,70)),(ef>2,(250,215,120))):
        mm=np.repeat(np.repeat(m,C,0),C,1)
        big[mm]=col
    mk=(big.sum(2)>0)
    img[mk]=big[mk]
    # extra bright for the longest
    return np.clip(img,0,255).astype(np.uint8)
ps=[panel(np.radians(d)) for d in (0,45,135)]
gap=np.full((N*C,20,3),12,np.uint8)
Image.fromarray(np.concatenate([ps[0],gap,ps[1],gap,ps[2]],1)).convert('RGB').save('assets/t40/floats.png')
