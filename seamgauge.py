import numpy as np
from PIL import Image, ImageDraw
from floats import runs
def stats(o):
    return np.where(o,runs(o.T).T,0), np.where(~o,runs(o),0)
W=18; C=22
i,j=np.meshgrid(np.arange(W),np.arange(W),indexing='ij')
Z=((i+j)%4)<2
def panel(k,vert,c=9):
    S=((i-j+k)%4)<2
    o=np.where((j if vert else i)<c,Z,S)
    wf,ef=stats(o)
    # runs are truncated by the panel edge: only trust cells at least 4 from the border
    img=np.where(o[...,None],np.array([30,40,70.]),np.array([70,66,58.]))
    img=np.repeat(np.repeat(img,C,0),C,1)
    for m,col in ((wf>2,(255,90,70)),(ef>2,(250,215,120))):
        mm=np.repeat(np.repeat(m,C,0),C,1); img[mm]=col
    # seam line
    p=c*C
    if vert: img[:,p-1:p+1]=(235,235,235)
    else: img[p-1:p+1,:]=(235,235,235)
    return np.clip(img,0,255).astype(np.uint8), wf.max(), ef.max()
rows=[]
for k in (0,1):
    ps=[panel(k,True),panel(k,False)]
    print(k,[(p[1],p[2]) for p in ps])
    gap=np.full((W*C,16,3),12,np.uint8)
    rows.append(np.concatenate([ps[0][0],gap,ps[1][0]],1))
g=np.full((16,rows[0].shape[1],3),12,np.uint8)
Image.fromarray(np.concatenate([rows[0],g,rows[1]],0)).save('assets/t41/gauge.png')
