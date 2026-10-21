# the fan drawn by code: a limb splits into parallel lines, spacing set by a golden-angle phase
import math
from PIL import Image, ImageDraw
S=4; W=1080*S; H=1350*S
img=Image.new("RGB",(W,H),(238,231,216)); d=ImageDraw.Draw(img)
ink=(150,40,38)
def stroke(pts,w):
    for p,q in zip(pts,pts[1:]):
        d.line([p,q],fill=ink,width=max(1,int(w)))
        d.ellipse([q[0]-w/2,q[1]-w/2,q[0]+w/2,q[1]+w/2],fill=ink)
# limb: thick, rising from bottom, bending slightly
cx,cy=W*0.5,H*0.95
limb=[]
for i in range(101):
    t=i/100
    limb.append((cx+math.sin(t*2.2)*60*S, cy-t*H*0.42))
for k,w in ((0,38),):
    stroke(limb,w*S)
# fan: N lines leave the limb top, spacing by drifting gaps
N=24
ph=0.0; gaps=[]
for i in range(N):
    ph+=2.399963; gaps.append(1.0+0.6*math.sin(ph))
tot=sum(gaps); x0,y0=limb[-1]
acc=0
for i in range(N):
    acc+=gaps[i]
    u=(acc-gaps[i]/2)/tot*2-1          # -1..1 across the fan
    a=-math.pi/2+u*0.62
    L=H*(0.46-0.10*abs(u)**1.6)+ (gaps[i]-1)*H*0.03
    w=(7-3*abs(u))*S
    pts=[]
    px,py=x0+u*10*S,y0
    n=120
    for j in range(n+1):
        t=j/n
        aa=a+u*0.10*t+math.sin(t*3+i)*0.012
        if j: px+=math.cos(aa)*L/n; py+=math.sin(aa)*L/n
        pts.append((px,py))
    stroke(pts,w)
img=img.resize((W//S,H//S),Image.LANCZOS)
img.save("assets/reed.png"); img.convert("RGB").save("assets/reed.jpg",quality=90)
