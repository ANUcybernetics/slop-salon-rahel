# one golden sequence of threads, mirrored into warp and weft, woven three ways with honest thread shading
import numpy as np
from PIL import Image
phi=(1+5**.5)/2
N=96; C=14
pal=np.array([(190,52,50),(232,150,60),(240,218,150),(70,110,130),(34,40,70)],float)
def seq(n):
    k=np.arange(n); a=phi**-5
    c=np.floor(5*((k*a)%1)).astype(int)
    shade=1+0.10*np.sin(2*np.pi*((k*phi**-2)%1))
    return c,shade
c,sh=seq(N)
def over_twill(i,j): return ((i+j)%4)<2
def over_satin(i,j): return (i*5-j)%13==0 or ((i*5-j)%13) in (0,)
def over_satin13(i,j): return ((j-5*i)%13)<1
def over_plain(i,j): return (i+j)%2==0
t=np.arange(C); edge=np.minimum(t,C-1-t)/(C/2)
prof=np.cos((t-C/2+.5)/C*np.pi*0.95)
px=np.tile(prof,(C,1)); py=np.tile(prof[:,None],(1,C))
sliver=(np.abs(t-C/2+.5)>C*0.36)
def lit(b,p,dip=1.0): return b*((0.35+0.65*p)*dip)[...,None]
def weave(over):
    img=np.zeros((N*C,N*C,3))
    for j in range(N):
        for i in range(N):
            wc=pal[c[i]]*sh[i]; fc=pal[c[j]]*sh[j]
            if over(i,j):
                under=lit(fc,py,0.5+0.5*np.tile(edge,(C,1)))
                cell=np.where(sliver[None,:,None],under,lit(wc,px))
            else:
                under=lit(wc,px,0.5+0.5*np.tile(edge[:,None],(1,C)))
                cell=np.where(sliver[:,None,None],under,lit(fc,py))
            img[j*C:(j+1)*C,i*C:(i+1)*C]=cell
    return Image.fromarray(np.clip(img,0,255).astype(np.uint8))
# satin: warp-float 1 over 12 under => weft mostly shows; invert so warp floats dominate
for name,f in [("twill",over_twill),("satin",lambda i,j: ((j-5*i)%13)!=0),("plain",over_plain)]:
    weave(f).save(f"assets/w3_{name}.png")
