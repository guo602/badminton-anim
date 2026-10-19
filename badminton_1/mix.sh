#!/bin/bash
set -e
cd .
python3 - <<'P'
import json,numpy as np,subprocess,wave
m=json.load(open('./out/mix.json')); cues=json.load(open('./out/cues_used.json'))
sr=44100; N=int(m['total']*sr); v=np.zeros(N,np.float32)
for k in m['keys']:
    raw=subprocess.run(['ffmpeg','-loglevel','error','-i',f'./vo/{k}.mp3','-f','f32le','-ac','1','-ar',str(sr),'-'],capture_output=True).stdout
    a=np.frombuffer(raw,np.float32); s=int(cues[k]*sr); e=min(N,s+len(a)); v[s:e]+=a[:e-s]
v=v/np.abs(v).max()*0.9
w=wave.open('./out/music.wav'); mu=np.frombuffer(w.readframes(w.getnframes()),np.int16).reshape(-1,2).astype(np.float32)/32767
mu=mu[:N] if len(mu)>=N else np.pad(mu,((0,N-len(mu)),(0,0)))
# duck envelope: voice active (20ms blocks), smoothed
blk=int(0.02*sr); nb=N//blk+1
rms=np.array([np.sqrt(np.mean(v[i*blk:(i+1)*blk]**2)) if i*blk<N else 0 for i in range(nb)])
act=(rms>0.02).astype(float)
# hold 0.4s, then smooth attack/release
act=np.convolve(act,np.ones(20),'same')>0
g=np.zeros(nb); cur=0
for i in range(nb):
    tgt=1.0 if act[i] else 0.0; k=0.25 if tgt>cur else 0.04; cur+=(tgt-cur)*k; g[i]=cur
gain=1-0.62*g; gain=np.repeat(gain,blk)[:N]
mvol=0.30
out=np.stack([v,v],1)+mu*mvol*gain[:,None]
out=np.clip(out,-0.98,0.98)
w=wave.open('./out/final_audio.wav','wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr)
w.writeframes((out*32767).astype(np.int16).tobytes()); w.close()
P
ffmpeg -loglevel error -y -i "$1" -i out/final_audio.wav -vf "ass=out/subs.ass" -map 0:v -map 1:a \
 -c:v libx264 -crf 19 -preset medium -threads 2 -pix_fmt yuv420p -c:a aac -b:a 192k -shortest "$2"
