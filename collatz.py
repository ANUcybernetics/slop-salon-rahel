import numpy as np, sys
from PIL import Image, ImageDraw
N=int(sys.argv[1]); L=float(sys.argv[2]); R=float(sys.argv[3]); name=sys.argv[4]
nxt=lambda n: n//2 if n%2==0 else 3*n+1
pos={1:(0.0,0.0,np.pi/2)}; edges=[]
for n in range(2,N):
    path=[]; m=n
    while m not in pos: path.append(m); m=nxt(m)
    for m in reversed(path):
        x,y,a=pos[nxt(m)]
        a2=a+(np.radians(L) if m%2==0 else -np.radians(R))
        pos[m]=(x+np.cos(a2),y+np.sin(a2),a2); edges.append((nxt(m),m))
w={m:(1 if m<N else 0) for m in pos}
for p,c in reversed(edges): w[p]+=w[c]
xs=np.array([p[0] for p in pos.values()]); ys=np.array([p[1] for p in pos.values()])
x0,x1,y0,y1=xs.min(),xs.max(),ys.min(),ys.max()
S=4; W=1600*S; H=int(W*(y1-y0)/(x1-x0))+20
sc=(W-20)/(x1-x0)
im=Image.new('RGB',(W,H),(14,12,20)); d=ImageDraw.Draw(im)
mx=max(w.values())
for p,c in edges:
    a=pos[p]; b=pos[c]
    t=np.log(w[c]+1)/np.log(mx)
    col=(int(40+215*t),int(30+150*t**1.5),int(70+40*t*(1-t)*4)) if t>0 else (40,30,70)
    wd=max(1,int(S*(0.6+5*t**2)))
    d.line([(10+(a[0]-x0)*sc,H-10-(a[1]-y0)*sc),(10+(b[0]-x0)*sc,H-10-(b[1]-y0)*sc)],fill=col,width=wd)
im=im.resize((W//S,H//S),Image.LANCZOS); im.save(f'assets/{name}.png'); print(im.size,mx)
