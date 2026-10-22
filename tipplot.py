import json, random, numpy as np, sys
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
sys.setrecursionlimit(10000)
sz=np.array(sorted(json.load(open('assets/sprig_sizes.json')),reverse=True))
def yule(n):
    ch={0:[]}; tips=[0]; nid=1
    while len(tips)<n:
        i=random.randrange(len(tips)); t=tips[i]; tips[i]=tips[-1]; tips.pop()
        a,b=nid,nid+1; nid+=2; ch[t]=[a,b]; ch[a]=[]; ch[b]=[]; tips+=[a,b]
    out=[]
    def f(x):
        s=1 if not ch[x] else sum(f(c) for c in ch[x]); out.append(s); return s
    f(0); return np.array(sorted(out,reverse=True))
random.seed(3)
grid=np.unique(np.round(np.logspace(0,np.log10(414),60)).astype(int))
def ccdf(s,g): return np.array([ (s>=x).sum() for x in g])
runs=np.array([ccdf(yule(414),grid) for _ in range(60)])
lo,hi=np.percentile(runs,5,axis=0),np.percentile(runs,95,axis=0)
paper=(238/255,231/255,216/255); ink=(196/255,72/255,52/255)
fig,ax=plt.subplots(figsize=(6.4,6.4),dpi=170,facecolor=paper); ax.set_facecolor(paper)
ax.fill_between(grid,lo,hi,color='#8a8478',alpha=.35,lw=0)
x=np.arange(1,1000)
ax.plot(x,715/x*1.0,color='#444',lw=.9,ls=(0,(4,3)))
ax.step(grid,ccdf(sz,grid),where='post',color=ink,lw=1.2,alpha=.5)
u=np.unique(sz); ax.scatter(u,[ (sz>=v).sum() for v in u],s=70,color=ink,zorder=5)
ax.set_xscale('log'); ax.set_yscale('log'); ax.set_xlim(.8,600); ax.set_ylim(.8,1000)
ax.set_xlabel('tips above a limb',color='#333'); ax.set_ylabel('limbs with at least that many',color='#333')
for s in ax.spines.values(): s.set_color('#555')
ax.tick_params(colors='#333')
ax.set_title('eight sizes, one for each generation',color='#333',fontsize=11)
plt.tight_layout(); plt.savefig('assets/tipladder.png',facecolor=paper)
