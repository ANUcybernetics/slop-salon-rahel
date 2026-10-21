# sprig.py's tree, recorded as segments, then grown in time: each limb extends along its length after its parent finishes
import math, subprocess, os
from PIL import Image, ImageDraw
S=2; W=1080*S; H=1350*S
ink=(196,72,52); bg=(238,231,216)
phase=[0.0]
def drift():
    phase[0]+=2.399963
    return math.sin(phase[0])
segs=[]  # (pts, widths, t0, t1)
def seg(x,y,a,L,w0,w1,bend):
    n=max(6,int(L/(6*S)))
    pts=[(x,y)];ws=[w0]
    for i in range(1,n+1):
        t=i/n; aa=a+bend*(t-0.5)
        x+=math.cos(aa)*L/n; y+=math.sin(aa)*L/n
        pts.append((x,y)); ws.append(w0+(w1-w0)*t)
    return pts,ws,aa
def grow(x,y,a,L,w,depth,t0):
    if depth==0 or L<10*S: return
    pts,ws,aa=seg(x,y,a,L,w,w*0.78,drift()*0.25)
    dur=0.9+L/(H*0.19)*0.9
    segs.append((pts,ws,t0,t0+dur))
    ex,ey=pts[-1]
    k=2 if depth%3 else 3
    for j in range(k):
        off=(j-(k-1)/2)*0.55+drift()*0.22
        grow(ex,ey,aa+off,L*(0.71+0.05*drift()),w*0.74,depth-1,t0+dur)
    if depth>3:
        mx=x+(ex-x)*0.55; my=y+(ey-y)*0.55
        grow(mx,my,aa+(0.9 if drift()>0 else -0.9),L*0.45,w*0.6,depth-3,t0+dur*0.55)
bx,by=W*0.5,H*0.93
grow(bx,by,-math.pi/2,H*0.19,13*S,8,0.0)
T=max(s[3] for s in segs); FPS=24; DUR=11.0; hold=1.5
os.makedirs("assets/gf",exist_ok=True)
N=int(DUR*FPS)
for f in range(N):
    t=min(f/FPS/(DUR-hold),1.0)*T
    img=Image.new("RGB",(W,H),bg); d=ImageDraw.Draw(img)
    d.line([(bx-14*S,by),(bx+14*S,by-5*S)],fill=ink,width=3*S)
    for pts,ws,t0,t1 in segs:
        if t<=t0: continue
        p=min(1,(t-t0)/(t1-t0)); p=p*p*(3-2*p)
        m=int(p*(len(pts)-1))
        for i in range(m):
            w=ws[i]; q=pts[i+1]
            d.line([pts[i],q],fill=ink,width=max(1,int(w)))
            d.ellipse([q[0]-w/2,q[1]-w/2,q[0]+w/2,q[1]+w/2],fill=ink)
    img.resize((1080,1350),Image.LANCZOS).save(f"assets/gf/{f:04d}.png")
print(len(segs),T,N)
