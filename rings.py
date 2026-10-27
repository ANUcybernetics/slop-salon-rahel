from PIL import Image, ImageDraw, ImageFilter
import numpy as np
from scipy.ndimage import gaussian_filter
S=4; W=1024; B=W*S
rng=np.random.default_rng(7)
paper=np.ones((W,W,3))*np.array([243,236,220])
g=gaussian_filter(rng.normal(0,1,(W,W)),1.0); g/=g.std()
cx,cy=520,760; ry_k=0.26
# one continuous thread: falls from top, then winds outward as rings on the water
pts=[]
# fall
for t in np.linspace(0,1,260):
    y=-20+(cy-4+20)*t**1.15
    x=cx+ 38*np.sin(t*5.5)*(1-t)**1.6+ 14*np.sin(t*17)*(1-t)**2
    pts.append((x,y,1.3+1.6*t))
# spiral
turns=11.5; N=5200
for i in range(N):
    u=i/N; th=u*turns*2*np.pi
    r=6+ 410*u**0.78
    wob=1+0.035*np.sin(th*3+u*9)+0.02*np.sin(th*7)
    x=cx+r*np.cos(th+0.3)*wob
    y=cy+r*ry_k*np.sin(th+0.3)*wob
    pts.append((x,y,2.9*(1-0.55*u)+0.4*np.sin(i*0.05)))
wash=Image.new('L',(B,B),0); dw=ImageDraw.Draw(wash)
thr=Image.new('RGBA',(B,B),(0,0,0,0)); dt=ImageDraw.Draw(thr)
sh=Image.new('L',(B,B),0); ds=ImageDraw.Draw(sh)
for k,(a,b) in enumerate(zip(pts[:-1],pts[1:])):
    w=max(1,a[2]*S)
    col=(170,28,30,255)
    dt.line([a[0]*S,a[1]*S,b[0]*S,b[1]*S],fill=col,width=int(w))
    if k>260:
        ds.line([a[0]*S+3*S,a[1]*S+4*S,b[0]*S+3*S,b[1]*S+4*S],fill=120,width=int(w*1.6))
# wash: pond pooled under rings
for r in range(1,60):
    rr=r*8
    dw.ellipse([(cx-rr)*S,(cy-rr*ry_k)*S,(cx+rr)*S,(cy+rr*ry_k)*S],fill=int(255*0.02*(60-r)/60*3))
wash=wash.filter(ImageFilter.GaussianBlur(14*S)).resize((W,W),Image.LANCZOS)
sh=sh.filter(ImageFilter.GaussianBlur(3*S)).resize((W,W),Image.LANCZOS)
w=np.asarray(wash).astype(float)/255; s=np.asarray(sh).astype(float)/255
img=paper.copy()
tint=np.array([120,150,165])
img=img*(1-0.9*w[...,None])+ (tint)*0.9*w[...,None]*0+img*0
img=paper*(1-0.5*w[...,None])+paper*np.array([.55,.68,.74])*0.5*w[...,None]
img=img*(1-0.45*s[...,None])
im=Image.fromarray(np.clip(img,0,255).astype('uint8')).convert('RGBA').resize((B,B),Image.LANCZOS)
im.alpha_composite(thr)
im=im.convert('RGB').resize((W,W),Image.LANCZOS)
a=np.asarray(im).astype(float)*(1+0.04*g[...,None])
Image.fromarray(np.clip(a,0,255).astype('uint8')).save('assets/rings.png')
