import numpy as np, random
from PIL import Image, ImageDraw, ImageFilter
random.seed(7); np.random.seed(7)
W=H=1600
img=Image.new("RGB",(W,H),(22,20,26))
d=ImageDraw.Draw(img,"RGBA")
pal=[(226,92,64),(240,190,90),(90,150,170),(236,228,214),(150,60,90)]
# warp threads: vertical, wobble with a shared slow wave; weft: horizontal, skipping where "pattern" says
n=90
xs=np.linspace(60,W-60,n)
def wave(y,i): return 18*np.sin(y/170+i*0.35)+9*np.sin(y/53+i*1.7)
for i,x in enumerate(xs):
    c=pal[(i*3+i//7)%len(pal)]
    pts=[(x+wave(y,i),y) for y in range(0,H+1,8)]
    d.line(pts,fill=c+(200,),width=7)
for j in range(110):
    y=40+j*(H-80)/110
    c=pal[(j*2+j//5)%len(pal)]
    segs=[];cur=[]
    for k,x in enumerate(np.arange(0,W+1,8)):
        # over/under: weft hides where parity flips, with a drifting twill
        i=np.argmin(abs(xs-x))
        over=((i+j//2+int(j*i/60))%4)<2
        yy=y+10*np.sin(x/140+j*0.2)
        if over: cur.append((x,yy))
        else:
            if len(cur)>1: segs.append(cur)
            cur=[]
    if len(cur)>1: segs.append(cur)
    for s in segs: d.line(s,fill=c+(235,),width=6)
img=img.filter(ImageFilter.GaussianBlur(0.8))
img.save("weave.png")
