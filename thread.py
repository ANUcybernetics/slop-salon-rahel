from PIL import Image, ImageDraw, ImageFilter
import numpy as np
S=4
im=Image.open('assets/t26/1/out-0.webp').convert('RGB')
W=im.width
big=im.resize((W*S,W*S),Image.LANCZOS)
pts=[(556,612),(566,650),(590,700),(640,745),(660,800),(600,850),(520,885),(470,930),(560,965),(650,990),(700,1030)]
def cr(p,n=40):
    P=[p[0]]+p+[p[-1]]; out=[]
    for i in range(1,len(P)-2):
        p0,p1,p2,p3=[np.array(x,float) for x in P[i-1:i+3]]
        for t in np.linspace(0,1,n,endpoint=False):
            out.append(0.5*((2*p1)+(-p0+p2)*t+(2*p0-5*p1+4*p2-p3)*t*t+(-p0+3*p1-3*p2+p3)*t**3))
    return out
path=cr(pts)
sh=Image.new('L',big.size,0); th=Image.new('RGBA',big.size,(0,0,0,0)); hi=Image.new('L',big.size,0)
ds=ImageDraw.Draw(sh); dt=ImageDraw.Draw(th); dh=ImageDraw.Draw(hi)
n=len(path)
for i in range(n-1):
    y=path[i][1]; w=(1.5+5.5*((y-600)/430)**1.5)*S*(1+0.25*np.sin(i*0.37)+0.15*np.sin(i*1.9))
    a=tuple(path[i]*np.array([S,S])); b=tuple(path[i+1]*np.array([S,S]))
    ds.line([a[0]+w*0.8,a[1]+w*0.9,b[0]+w*0.8,b[1]+w*0.9],fill=150,width=int(w*1.2))
    dt.line([*a,*b],fill=(168,26,26,255),width=int(w))
    dh.line([a[0]-w*0.2,a[1]-w*0.2,b[0]-w*0.2,b[1]-w*0.2],fill=255,width=max(1,int(w*0.3)))
sh=sh.filter(ImageFilter.GaussianBlur(5*S))
dark=Image.new('RGB',big.size,(10,14,30))
big=Image.composite(dark,big,sh.point(lambda v:int(v*0.55)))
big.paste(th,(0,0),th)
hl=Image.new('RGB',big.size,(255,150,120))
big=Image.composite(hl,big,hi.filter(ImageFilter.GaussianBlur(S*0.6)).point(lambda v:int(v*0.5)))
out=big.resize((W,W),Image.LANCZOS)
rng=np.random.default_rng(3); g=rng.normal(0,1,(W,W)); 
from scipy.ndimage import gaussian_filter
g=gaussian_filter(g,0.8); g=g/g.std()
a=np.asarray(out).astype(float)*(1+0.035*g[...,None]); out=Image.fromarray(np.clip(a,0,255).astype('uint8'))
out.save('assets/thread_room.png'); out.convert('RGB').save('assets/thread_room.jpg',quality=90)
