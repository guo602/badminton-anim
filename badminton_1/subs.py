import json,sys
sys.path.insert(0,'.'); from narration import CUES
d=json.load(open(sys.argv[1])); cues=d['cues']; durs=json.load(open('./vo/durs.json'))
def ts(x,sep='.'):
    h=int(x//3600); m=int(x%3600//60); s=x%60
    return f"{h}:{m:02d}:{s:05.2f}" if sep=='.' else f"{h:02d}:{m:02d}:{int(s):02d},{int(round((s%1)*1000))%1000:03d}"
ev=[]
for k,pairs in CUES.items():
    st=cues[k]; du=durs[k]; w=[max(len(z),1) for z,_ in pairs]; tot=sum(w); t=st
    for (z,e),wi in zip(pairs,w):
        dt=du*wi/tot; ev.append((t,t+dt+0.15,z,e)); t+=dt
# avoid overlap
for i in range(len(ev)-1):
    if ev[i][1]>ev[i+1][0]: ev[i]=(ev[i][0],ev[i+1][0],ev[i][2],ev[i][3])
hdr="""[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: ZH,Noto Sans CJK SC,54,&H00FFFFFF,&H00FFFFFF,&H00365400,&H64000000,1,0,0,0,100,100,1,0,1,3.4,0,2,60,60,26,1
Style: EN,Noto Sans CJK SC,36,&H00FFFFFF,&H00FFFFFF,&H00365400,&H64000000,0,0,0,0,100,100,0,0,1,2.6,0,2,80,80,22,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
with open('./out/subs.ass','w') as f:
    f.write(hdr)
    for a,b,z,e in ev:
        f.write(f"Dialogue: 0,{ts(a)},{ts(b)},ZH,,0,0,0,,{z}\\N{{\\rEN}}{e}\n")
with open('./out/subs.srt','w') as f:
    for i,(a,b,z,e) in enumerate(ev,1):
        f.write(f"{i}\n{ts(a,',')} --> {ts(b,',')}\n{z}\n{e}\n\n")
# voice track filter
keys=list(CUES); args=[]; fl=[]
for i,k in enumerate(keys):
    ms=int(cues[k]*1000); fl.append(f"[{i}:a]adelay={ms}|{ms},aresample=44100,aformat=sample_fmts=fltp:channel_layouts=stereo[v{i}]")
json.dump({"keys":keys,"filter":";".join(fl)+";"+"".join(f"[v{i}]" for i in range(len(keys)))+f"amix=inputs={len(keys)}:normalize=0,apad[vo]","total":d['total']},open('./out/mix.json','w'))
json.dump(cues,open('./out/cues_used.json','w')); print(len(ev),'events')
