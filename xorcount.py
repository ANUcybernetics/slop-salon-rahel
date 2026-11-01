import numpy as np
def runs(lo,N,k):
    # strokes = maximal runs of cells with i^j==2^k along a diagonal (j-i const)
    cnt=0;lens=[]
    for d in (1<<k,-(1<<k)):
        L=0
        for i in range(lo,lo+N):
            j=i+d
            ok = lo<=j<lo+N and (i^j)==(1<<k)
            if ok: L+=1
            else:
                if L: cnt+=1;lens.append(L)
                L=0
        if L: cnt+=1;lens.append(L)
    return cnt,sorted(set(lens))
for lo,name in ((0,'0..511'),(1,'1..512')):
    print(name,[ (1<<k,)+runs(lo,512,k) for k in range(9)])
print()
for k in range(1,9):
    c=runs(1,512,k)
    import collections
    # count by length
    L=0;d=[]
    for dd in (1<<k,-(1<<k)):
        L=0
        for i in range(1,513):
            j=i+dd
            if 1<=j<=512 and (i^j)==(1<<k): L+=1
            else:
                if L:d.append(L)
                L=0
        if L:d.append(L)
    print(1<<k,collections.Counter(d))
