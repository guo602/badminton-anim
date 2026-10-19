import asyncio, json, subprocess, edge_tts, sys
sys.path.insert(0, ".")
from narration import CUES, tts_text
VOICE = "zh-CN-YunjianNeural"
async def one(k, rows):
    txt = "".join(tts_text(z) for z, _ in rows)
    out = f"./vo/{k}.mp3"
    for attempt in range(3):
        try:
            await edge_tts.Communicate(txt, VOICE, rate="+4%").save(out); break
        except Exception as e:
            print("retry", k, e); await asyncio.sleep(2)
    d = float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",out]))
    return k, d
async def main():
    res = await asyncio.gather(*[one(k, r) for k, r in CUES.items()])
    durs = dict(res); json.dump(durs, open("./vo/durs.json","w"), ensure_ascii=False, indent=1)
    print(durs, sum(durs.values()))
asyncio.run(main())
