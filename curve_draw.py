import json, numpy as np, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
d=json.load(open("/tmp/curve.json")); S=np.array(d["S"]); N2=56*56
fig,ax=plt.subplots(figsize=(8,6),dpi=140); bg="#f3ede0"; fig.patch.set_facecolor(bg); ax.set_facecolor(bg)
ax.plot(S,np.array(d["coin"])/N2*100,color="#9a9588",lw=2,label="coin flips (fitted the same way)")
ax.plot(S,np.array(d["mine"])/N2*100,color="#b3402a",lw=3,marker="o",ms=5,label="rahel's cloth")
ax.scatter([8],[419/2304*100],s=90,color="#2a5d7a",zorder=5); ax.scatter([8],[644/2304*100],s=90,facecolor=bg,edgecolor="#2a5d7a",lw=2,zorder=5)
ax.scatter([8],[0],s=90,color="#c79a2b",zorder=5)
ax.annotate("mina: 0, done at 8",(8,0),(10,4),color="#8a6a14",fontsize=10)
ax.annotate("germaine: 18%\n(her coin flips: 28%)",(8,18.2),(9.5,12),color="#2a5d7a",fontsize=10)
ax.annotate("mine: 33%\n(coin flips: 33%)",(8,32.6),(2.1,12),color="#b3402a",fontsize=10)
ax.set_xscale("log",base=2); ax.set_xticks([1,2,4,8,16,32,56]); ax.set_xticklabels([1,2,4,8,16,32,56])
ax.set_xlabel("shafts on the loom"); ax.set_ylabel("% of crossings the loom gets wrong")
ax.set_ylim(-2,52); ax.legend(frameon=False,loc="upper right",fontsize=10)
for s in ("top","right"): ax.spines[s].set_visible(False)
plt.tight_layout(); plt.savefig("assets/curve.png"); 
