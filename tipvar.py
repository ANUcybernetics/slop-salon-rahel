import math, random, numpy as np
def tree_sizes(kf, twig, G=8, r=0.71):
    # regular tree: returns tips-above per limb; twig = extra side limb at depth>3 of depth-3
    sizes=[]
    def g(d):
        if d==0: return 1
        k=kf(d); t=sum(g(d-1) for _ in range(k))
        if twig and d>3: t+=g(d-3)
        sizes.append(t); return t
    g(G); return sizes
def slope(sz):
    sz=np.array(sorted(sz,reverse=True)); rank=np.arange(1,len(sz)+1)
    m=sz>=1
    return np.polyfit(np.log(sz),np.log(rank),1)[0]  # N(>=s) ~ s^slope
def yule(n):
    # coin tree: random tip forks into two; sizes of every clade
    ch={0:[]}; tips=[0]; nid=1
    while len(tips)<n:
        t=random.choice(tips); tips.remove(t)
        a,b=nid,nid+1; nid+=2; ch[t]=[a,b]; ch[a]=[]; ch[b]=[]; tips+= [a,b]
    sz={}
    def f(x):
        s=1 if not ch[x] else sum(f(c) for c in ch[x]); sz[x]=s; return s
    import sys; sys.setrecursionlimit(10000); f(0); return list(sz.values())
for name,kf,tw in [('mine(2/3 forks + twigs)',lambda d:2 if d%3 else 3,True),('no twigs',lambda d:2 if d%3 else 3,False),('always 2, twigs',lambda d:2,True),('always 2, no twigs',lambda d:2,False),('always 3 no twigs',lambda d:3,False)]:
    s=tree_sizes(kf,tw); print(name,len(s),max(s),round(slope(s),2))
random.seed(1)
print('coin 375 tips', np.mean([slope(yule(375)) for _ in range(40)]))
