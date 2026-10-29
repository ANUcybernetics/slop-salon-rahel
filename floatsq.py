import numpy as np
from floats import runs
def stats(over):
    cr=runs(over.T).T; rr=runs(over)
    return np.where(over,cr,0), np.where(~over,rr,0)
# infinite twill, one straight seam, all phases. W=64 grid, seam at c (vertical: cols<c Z, >=c S) or at r (horizontal)
N=64
i,j=np.meshgrid(np.arange(N),np.arange(N),indexing='ij')
Z=((i+j)%4)<2; S=((i-j)%4)<2
print('vertical seam: seam col c mod 4 -> (max warp float, max weft float) away from edges')
for c in range(28,32):
    o=np.where(j<c,Z,S); w,e=stats(o)
    # interior only: rows all (runs along columns are full height though -> truncated at edges; use rows 8..N-8 for weft, cols 8.. for warp)
    print(c%4,'warp',w[:, :].max(),'weft',e[8:-8,8:-8].max(), 'hist warp',np.bincount(w[8:-8,8:-8].ravel())[1:], 'weft',np.bincount(e[8:-8,8:-8].ravel())[1:])
print('horizontal seam: rows<r Z, else S')
for r in range(28,32):
    o=np.where(i<r,Z,S); w,e=stats(o)
    print(r%4,'warp',w[8:-8,8:-8].max(),'weft',e[8:-8,8:-8].max())
print('reversed order S|Z')
for c in range(28,32):
    o=np.where(j<c,S,Z); w,e=stats(o); print('v',c%4,'warp',w[8:-8,8:-8].max(),'weft',e[8:-8,8:-8].max())
for r in range(28,32):
    o=np.where(i<r,S,Z); w,e=stats(o); print('h',r%4,'warp',w[8:-8,8:-8].max(),'weft',e[8:-8,8:-8].max())
print('transpose test: over->~over.T of a vertical Z|S seam')
o=np.where(j<30,Z,S); w,e=stats(~o.T); print('warp',w[8:-8,8:-8].max(),'weft',e[8:-8,8:-8].max())
