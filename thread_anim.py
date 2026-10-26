from PIL import Image, ImageDraw, ImageFilter
import numpy as np, os
from scipy.ndimage import gaussian_filter
exec(open('thread.py').read().split("sh=Image.new")[0])  # S, big, path, cr, W
S=2
base=Image.open('assets/t26/1/out-0.webp').convert('RGB')
rng=np.random.default_rng(3); g=gaussian_filter(rng.normal(0,1,(W,W)),0.8); g/=g.std()
occ=np.load('assets/occ.npy')[...,None]*0.92; b0=np.asarray(base).astype(float)
n=len(path); os.makedirs('assets/ta',exist_ok=True)
def widths(i): 
    y=path[i][1]; return (1.5+5.5*((y-600)/430)**1.5)*S*(1+0.25*np.sin(i*0.37)+0.15*np.sin(i*1.9))
F=150; hold=30
bigb=base.resize((W*S,W*S),Image.LANCZOS)
for f in range(F+hold):
    t=min(1,f/F); e=3*t*t-2*t**3; k=max(2,int(e*(n-1)))
    sh=Image.new('L',bigb.size,0); th=Image.new('RGBA',bigb.size,(0,0,0,0)); hi=Image.new('L',bigb.size,0)
    ds,dt,dh=ImageDraw.Draw(sh),ImageDraw.Draw(th),ImageDraw.Draw(hi)
    sway=lambda i: 3*S*np.sin(f*0.12+i*0.05)*(i/n)*(1 if f<F else 0.5)
    for i in range(k):
        w=widths(i); a=(path[i][0]*S+sway(i),path[i][1]*S); b=(path[i+1][0]*S+sway(i+1),path[i+1][1]*S)
        ds.line([a[0]+w*.8,a[1]+w*.9,b[0]+w*.8,b[1]+w*.9],fill=150,width=int(w*1.2))
        dt.line([*a,*b],fill=(168,26,26,255),width=int(w))
        dh.line([a[0]-w*.2,a[1]-w*.2,b[0]-w*.2,b[1]-w*.2],fill=255,width=max(1,int(w*.3)))
    sh=sh.filter(ImageFilter.GaussianBlur(5*S))
    im=Image.composite(Image.new('RGB',bigb.size,(10,14,30)),bigb,sh.point(lambda v:int(v*.55)))
    im.paste(th,(0,0),th)
    im=Image.composite(Image.new('RGB',bigb.size,(255,150,120)),im,hi.filter(ImageFilter.GaussianBlur(S*.6)).point(lambda v:int(v*.5)))
    out=im.resize((W,W),Image.LANCZOS)
    o=np.asarray(out).astype(float); out=Image.fromarray((o*(1-occ)+b0*occ).astype('uint8'))
    a=np.asarray(out).astype(float)*(1+0.035*g[...,None])
    Image.fromarray(np.clip(a,0,255).astype('uint8')).save(f'assets/ta/{f:04d}.png')
