"""用自己的录音替换 AI 配音。
把 13 段录音放进 my_voice/ 文件夹，文件名为 cue 名（hook.m4a、court.m4a … quiz.m4a，mp3/wav/m4a 都行），
然后运行：python3 use_my_voice.py  → 自动去首尾静音、统一响度，写入 vo/*.mp3 和 vo/durs.json。
之后重新渲染动画 + 字幕 + 混音即可，画面节奏会自动按你的语速对齐。
"""
import glob, json, os, subprocess
from narration import CUES
os.makedirs("vo", exist_ok=True)
durs = json.load(open("vo/durs.json")) if os.path.exists("vo/durs.json") else {}
for k in CUES:
    src = next(iter(sorted(glob.glob(f"my_voice/{k}.*"))), None)
    if not src:
        print("缺少", k, "（保留原 AI 配音）"); continue
    af = ("silenceremove=start_periods=1:start_threshold=-45dB,areverse,"
          "silenceremove=start_periods=1:start_threshold=-45dB,areverse,loudnorm=I=-16:TP=-1.5")
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", src, "-af", af, "-ar", "24000", "-ac", "1",
                    f"vo/{k}.mp3"], check=True)
    d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                              f"vo/{k}.mp3"], capture_output=True, text=True).stdout)
    durs[k] = round(d, 3); print(k, durs[k])
json.dump(durs, open("vo/durs.json", "w"), indent=1)
