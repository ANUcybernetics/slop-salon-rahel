# point-twill: threading and treadling both reverse at a seam; same golden sett mirrored; bands widened by W
import numpy as np, sys
from PIL import Image
exec(open('weave3.py').read().split('def over_twill')[0])
src=open('weave3.py').read()
# reuse shading helpers and weave() from weave3 without running its render loop
exec(src[src.index('t=np.arange(C)'):src.index('# satin:')])
def point(n,seam): 
    k=np.arange(n); return np.where(k<seam,k,2*seam-1-k)%n
def run(name,N_,seam_i,seam_j,W,mirror_colour=True):
    global N,c,sh
    N=N_
    base,bs=seq(N//W+2)
    c=np.repeat(base,W)[:N]; sh=np.repeat(bs,W)[:N]
    if mirror_colour:
        s=N//2; idx=np.where(np.arange(N)<s,np.arange(N),2*s-1-np.arange(N)); c=c[idx]; sh=sh[idx]
    pi=np.where(np.arange(N)<seam_i,np.arange(N),2*seam_i-1-np.arange(N))
    pj=np.where(np.arange(N)<seam_j,np.arange(N),2*seam_j-1-np.arange(N))
    over=lambda i,j: ((pi[i]+pj[j])%4)<2
    weave(over).save(f"assets/w4_{name}.png")
run('point',96,48,48,1)
run('wide',96,48,48,6)
