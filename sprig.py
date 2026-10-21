# line-only sprig: one stem from a snapped end, forks by a drifting phase (no random calls)
import math
from PIL import Image, ImageDraw
S=4; W=1080*S; H=1350*S
img=Image.new("RGB",(W,H),(238,231,216)); d=ImageDraw.Draw(img)
ink=(196,72,52)
phase=[0.0]
def drift():
    phase[0]+=2.399963  # golden angle, each fork unlike the last
    return math.sin(phase[0])
def seg(x,y,a,L,w0,w1,bend):
    n=max(6,int(L/(6*S)))
    pts=[];ws=[]
    for i in range(n+1):
        t=i/n
        aa=a+bend*(t-0.5)
        if i==0: px,py=x,y
        else:
            px+=math.cos(aa)*L/n; py+=math.sin(aa)*L/n
        pts.append((px,py)); ws.append(w0+(w1-w0)*t)
    for (p,q,w) in zip(pts,pts[1:],ws):
        d.line([p,q],fill=ink,width=max(1,int(w)))
        d.ellipse([q[0]-w/2,q[1]-w/2,q[0]+w/2,q[1]+w/2],fill=ink)
    return pts[-1],aa
def grow(x,y,a,L,w,depth):
    if depth==0 or L<10*S: return
    (ex,ey),aa=seg(x,y,a,L,w,w*0.78,drift()*0.25)
    k=2 if depth%3 else 3
    for j in range(k):
        off=(j-(k-1)/2)*0.55+drift()*0.22
        grow(ex,ey,aa+off,L*(0.71+0.05*drift()),w*0.74,depth-1)
    # a few unforked twigs along the way
    if depth>3:
        grow(x+(ex-x)*0.55,y+(ey-y)*0.55,aa+(0.9 if drift()>0 else -0.9),L*0.45,w*0.6,depth-3)
# stem: cut end at the bottom, sheared
bx,by=W*0.5,H*0.93
d.line([(bx-14*S,by),(bx+14*S,by-5*S)],fill=ink,width=3*S)
grow(bx,by,-math.pi/2,H*0.19,13*S,8)
img=img.resize((W//S,H//S),Image.LANCZOS)
img.save("assets/sprig.png"); img.convert("RGB").save("assets/sprig.jpg",quality=90)
