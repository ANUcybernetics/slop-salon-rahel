# colour = min(s(n),5) of Stern's diatomic sequence (s=1 cream, 2 orange, 3 red, 4 teal, >=5 navy); mirrored warp/weft
import numpy as np, sys
src=open('weave3.py').read().split('# satin:')[0]
src=src.replace('N=96; C=14','N=int(sys.argv[1]); C=int(sys.argv[2])')
exec(src)
def stern(n):
    s=np.zeros(n+1,int); s[1]=1
    for i in range(2,n+1): s[i]=s[i//2] if i%2==0 else s[i//2]+s[i//2+1]
    return s
off=int(sys.argv[3]); cap=5
s=stern(N+off+2)[1+off:1+off+N]
order=[2,1,0,3,4]  # palette index for s=1..5
c=np.array([order[min(v,cap)-1] for v in s])
sh=np.ones(N)
print(s[:40], (s==1).sum(), np.bincount(np.minimum(s,cap)))
weave(over_twill).save(f"assets/stern2_{off}.png")
