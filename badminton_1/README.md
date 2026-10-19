# badminton_1 · 羽毛球双打发球轮换

成片：`羽毛球双打发球轮换.mp4`（1920×1080，96 s，已烧录双语字幕），字幕另附 `羽毛球双打发球轮换_双语字幕.srt`。

> 用的是 Manim Community v0.22（`from manim import *`），和 badminton_0 / yylogo 的 ManimGL 不是一个库，不能混用。

## 文件
| 文件 | 作用 |
|---|---|
| narration.py | 13 段中英文案（配音读中文） |
| gen_vo.py | edge-tts 生成配音（zh-CN-YunjianNeural，+4%）→ vo/*.mp3 + vo/durs.json |
| use_my_voice.py | 用自己的录音替换 AI 配音（见下） |
| badminton_doubles.py | 动画，按 vo/durs.json 自动卡点，渲染后输出 cues.json |
| subs.py | 根据 cues.json 生成 out/subs.ass / subs.srt |
| music.py | 合成背景音乐 out/music.wav |
| mix.sh | 人声 + 背景乐（自动压低）+ 字幕烧录 |

## 一键流程（在本文件夹内运行）
```bash
mkdir -p out
python3 gen_vo.py                         # 或 python3 use_my_voice.py
manim -qh --disable_caching badminton_doubles.py DoublesRotation
python3 subs.py cues.json
python3 music.py 100
./mix.sh media/videos/badminton_doubles/1080p60/DoublesRotation.mp4 out/final.mp4
```

## 换成自己的声音
在 my_voice/ 里放 13 段录音，文件名为：
hook, court, r1, r2, r3, w0, w1, w2, w3, w4, w5, sum, quiz（扩展名 m4a/mp3/wav 都行），
每段读 narration.py 对应 cue 的中文。然后运行 `python3 use_my_voice.py`，再按上面流程重新渲染，画面会自动按你的语速对齐。

## 评论区置顶答案
2:2，A·B 作为接发方得分 → 谁都不动；A·B 是 2 分（偶数）→ 右区；此时 A·B 右区站的是 B，对角是 D。
**答案：B 在右区发球，发给 D。**
