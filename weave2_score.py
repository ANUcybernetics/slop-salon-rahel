# read weave2's crossings as a score: row = beat, column = partial, "warp over" = sounding
import numpy as np, wave
o=np.load("/tmp/over.npy"); N=o.shape[0]; snap_i,snap_j=33,27
sr=22050; step=0.25
scale=[0,2,3,7,9]                      # minor pentatonic over 4 octaves, a few columns share a pitch
freqs=[110*2**((12*(i//5)+scale[i%5])/12)/2 for i in range(N)]
freqs=[f*2 if f<110 else f for f in freqs]
T=int(sr*step*N); out=np.zeros(T)
t=np.arange(int(sr*step*1.6))/sr
env=np.minimum(1,t/0.02)*np.exp(-t/0.35)
for j in range(N):
    s=int(j*sr*step)
    for i in range(N):
        if i==snap_i and j>=snap_j: continue
        if o[j,i]:
            f=freqs[i]
            if f>1800: continue
            seg=np.sin(2*np.pi*f*t)*env*(1/(1+f/400))
            e=min(len(seg),T-s); out[s:s+e]+=seg[:e]
out/=np.abs(out).max()*1.1
w=wave.open("assets/weave2.wav","wb"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
w.writeframes((out*32767).astype(np.int16).tobytes()); w.close()
print(T/sr)
