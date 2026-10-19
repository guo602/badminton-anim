# 每个 cue：[(中文字幕, 英文字幕), ...]，配音读中文
CUES = {
 "hook": [("双打发球，到底该谁发、站哪边？", "Doubles serve: who serves, and from which side?"),
          ("记住三句话，比分一报你就知道。", "Remember three rules and the score tells you everything.")],
 "court": [("先认一下双打的发球区：短而宽。", "First, the doubles service court: short and wide."),
           ("左右宽到最外侧边线，后面只到双打后发球线。", "It reaches the outer side line, but only back to the doubles long service line.")],
 "r1": [("第一句：看发球方自己的比分。", "Rule one: look at the serving side's own score."),
        ("偶数站右区发，奇数站左区发。", "Even: serve from the right. Odd: serve from the left.")],
 "r2": [("第二句：发球方得分，同一个人接着发，和搭档换位。", "Rule two: if the serving side scores, the same player serves again and swaps sides with the partner.")],
 "r3": [("第三句：接发方得分，拿回发球权，但谁都不动。", "Rule three: if the receiving side scores, they win the serve, but nobody moves."),
        ("比分是单是双，就由站在那边的人发。", "Whoever stands on the side matching the score serves.")],
 "w0": [("站到发球人的位置，实战走一遍。", "Now step into the server's shoes."),
        ("零比零，A·B 先发。零是偶数，A 在右区，对角发给 C。", "It's 0–0 and A·B serve. Zero is even, so A serves from the right, diagonally to C.")],
 "w1": [("A·B 得分，1 比 0。", "A·B score: 1–0."),
        ("发球方得分，A 接着发，和 B 换位。", "The serving side scored, so A serves again and swaps with B.")],
 "w2": [("1 是奇数，A 在左区，对角发给 D。", "1 is odd, so A serves from the left, diagonally to D.")],
 "w3": [("这一球 C·D 赢了，发球权过去，谁都不动。", "C·D win this one. The serve passes over, and nobody moves."),
        ("镜头转到 C·D 这边。", "Let's switch to C·D's side.")],
 "w4": [("C·D 1 分，奇数，看左区：站着的是 D。", "C·D have 1, which is odd. Who's on the left? D."),
        ("所以 D 来发，对角发给 A。", "So D serves, diagonally to A.")],
 "w5": [("C·D 再得一分，D 接着发，和 C 换位。", "C·D score again. D serves again and swaps with C."),
        ("2 是偶数，D 从右区发给 B。", "2 is even, so D serves from the right to B.")],
 "sum": [("总结一下：", "To sum up:"),
         ("比分单双定左右，发球方得分换位，接发方得分不动。", "the score picks the side; serving side scores, swap; receiving side scores, stay.")],
 "quiz": [("最后考考你：这一球 A·B 赢了，比分 2 比 2。", "Quiz time: A·B win this rally. It's 2–2."),
          ("该谁发？站哪边？发给谁？", "Who serves, from which side, and to whom?"),
          ("答案打在评论区，看看你能不能一次答对！", "Drop your answer in the comments!")],
}

def tts_text(zh):
    return zh.replace("A·B", "A B").replace("C·D", "C D").replace("“", "").replace("”", "")
