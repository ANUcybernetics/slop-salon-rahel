import numpy as np, colorsys
from PIL import Image, ImageDraw
from spend import *
S=2
def draw(ps,seed=3):
    t=tiles(ps,seed); lab,ids,cnt=curves(t)
    L=dict(zip(ids,cnt)); rank=np.argsort(-cnt); top=ids[rank[:3]]
    im=Image.new('RGB',(N*S,N*S),(14,14,20)); d=ImageDraw.Draw(im)
    lg=np.log10(cnt.max())
    for k,ar in enumerate((lab[:N*N].reshape(N,N),lab[N*N:].reshape(N,N))):
        ii,jj=np.nonzero(ar>=0)
        for i,j in zip(ii,jj):
            l=ar[i,j]; n=L[l]
            if l in top: c=[(255,150,40),(70,200,220),(240,230,200)][list(top).index(l)]
            else:
                x=np.log10(n)/lg; c=tuple(int(v) for v in (30+60*x,40+70*x,70+90*x))
            x0,y0=j*S,i*S
            seg=(x0,y0,x0+S,y0) if k==0 else (x0,y0,x0,y0+S)
            d.line(seg,fill=c,width=1)
    return im
names=list(rules)
ims=[draw(rules[n]) for n in names]
W=N*S
pg=Image.new('RGB',(2*W+12,2*W+12),(14,14,20))
for q,im in enumerate(ims): pg.paste(im,((q%2)*(W+12),(q//2)*(W+12)))
pg.save('assets/spend.png'); print(pg.size)
