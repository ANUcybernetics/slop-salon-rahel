# honest weave: every crossing decided and shaded; one warp thread snaps and the cloth goes on without it
import numpy as np
from PIL import Image, ImageDraw
np.random.seed(11)
N=56; C=28; M=60
S=N*C; W=S+2*M
warp_pal=np.array([(196,58,52),(224,120,64),(232,176,80),(170,70,96)],float)
weft_pal=np.array([(58,92,112),(120,150,160),(214,206,190),(88,70,100)],float)
snap_i, snap_j = 33, 27
def over(i,j): return ((i+j+(j*i)//90) % 4) < 2
t=np.arange(C); edge=np.minimum(t,C-1-t)/(C/2)          # 0 at cell edge, ~1 at centre
prof=np.cos((t-C/2+.5)/C*np.pi*0.95)                     # round thread cross-section
px=np.tile(prof,(C,1)); py=np.tile(prof[:,None],(1,C))
def lit(base,p,dip=1.0): return base*((0.35+0.65*p)*dip)[...,None]
sliver=(np.abs(t-C/2+.5)>C*0.36)
img=np.zeros((W,W,3)); img[:]=(20,18,24)
for j in range(N):
    for i in range(N):
        wc=warp_pal[(i*3+i//5)%4]*(1+0.06*np.random.randn())
        fc=weft_pal[(j*2+j//6)%4]*(1+0.06*np.random.randn())
        if i==snap_i and j>=snap_j:
            cell=lit(fc,py)*0.92
            cell*= (0.7+0.3*np.tile(np.abs(t-C/2+.5)/(C/2),(C,1)))[...,None]
        elif over(i,j):
            under=lit(fc,py,0.5+0.5*np.tile(edge,(C,1)))
            cell=np.where(sliver[None,:,None],under,lit(wc,px))
        else:
            under=lit(wc,px,0.5+0.5*np.tile(edge[:,None],(1,C)))
            cell=np.where(sliver[:,None,None],under,lit(fc,py))
        y0=M+j*C; x0=M+i*C
        img[y0:y0+C,x0:x0+C]=cell
im=Image.fromarray(np.clip(img,0,255).astype(np.uint8))
d=ImageDraw.Draw(im,"RGBA")
cx=M+snap_i*C+C/2; cy=M+snap_j*C
for k in range(7):
    a=np.random.uniform(-1.2,1.2); L=np.random.uniform(40,110)
    pts=[(cx+np.sin(u*a*2.4)*L*u*0.5+(k-3)*2, cy-u*L*0.9) for u in np.linspace(0,1,24)]
    d.line(pts,fill=(226,100,70,210),width=2)
im.save("weave2.png")
np.save("/tmp/over.npy",np.array([[over(i,j) for i in range(N)] for j in range(N)]))
