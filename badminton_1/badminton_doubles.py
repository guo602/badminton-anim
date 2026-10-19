"""羽毛球双打发球轮换（badminton_1）
Manim Community v0.22（与 badminton_0 / yylogo 的 ManimGL 不同版本，代码不混用）
渲染：manim -qh --disable_caching badminton_doubles.py DoublesRotation
"""
import json
from manim import *
import numpy as np

# ---------- 系列配色（取自 badminton_0 / yylogo） ----------
BG = "#c8e5cc"        # 浅薄荷背景
COURT = "#2aa570"     # 场地绿
DEEP = "#005436"      # 深绿文字
NET_C = "#5d6b66"
POST = "#66CCFF"
AB_C = "#2f7fd8"      # A·B 蓝
CD_C = "#e2574c"      # C·D 红
HL = "#ffd400"        # 黄色高亮描边
RZ = "#8ed65a"        # 右区填充（黄绿）
LZ = "#66CCFF"        # 左区填充（浅蓝）
FONT = "Noto Sans CJK SC"

# ---------- 场地尺寸（米，真实比例） ----------
HW, HL_, WS, SS, DL = 3.05, 6.7, 2.59, 1.98, 5.94   # 半宽/半长/单打半宽/前发球线/双打后发球线
DURS = json.load(open("./vo/durs.json"))

def T(s, size=30, color=DEEP, weight=NORMAL, **kw):
    kw.setdefault("line_spacing", 1.2)
    return Text(s, font=FONT, font_size=size, color=color, weight=weight, **kw)

def P(x, y, z=0.0):
    return np.array([x, y, z])

def rect(x1, x2, y1, y2, color, op=0.8, z=0.005, stroke=None, sw=4):
    r = Polygon(P(x1, y1, z), P(x2, y1, z), P(x2, y2, z), P(x1, y2, z),
                fill_color=color, fill_opacity=op, stroke_width=0)
    if stroke:
        r.set_stroke(stroke, sw)
    return r

# A·B 在 y<0 一侧面向 +y：右手 = +x；C·D 在 y>0 面向 -y：右手 = -x
SPOT = {("AB", "R"): P(1.5, -4.0, 0.01), ("AB", "L"): P(-1.5, -4.0, 0.01),
        ("CD", "R"): P(-1.5, 4.0, 0.01), ("CD", "L"): P(1.5, 4.0, 0.01)}
ZONE = {("AB", "R"): (0, HW, -DL, -SS), ("AB", "L"): (-HW, 0, -DL, -SS),
        ("CD", "R"): (-HW, 0, SS, DL), ("CD", "L"): (0, HW, SS, DL)}

TOP = dict(phi=0, theta=-90 * DEGREES, zoom=0.46, frame_center=P(0, -0.7, 0))
FPV_AB = dict(phi=62 * DEGREES, theta=-90 * DEGREES, zoom=0.62, frame_center=P(0, 0, 0))
FPV_CD = dict(phi=62 * DEGREES, theta=90 * DEGREES, zoom=0.62, frame_center=P(0, 0, 0))
RCOL = 3.35   # 右栏左边界
LCOL = -4.45  # 左栏中心


class Player(VGroup):
    def __init__(self, name, color):
        disc = Circle(radius=0.62, fill_color=color, fill_opacity=1, stroke_color=WHITE, stroke_width=3)
        lab = Text(name, font=FONT, font_size=40, color=WHITE, weight=BOLD).scale_to_fit_height(0.6)
        super().__init__(disc, lab)
        self.lab = lab
        self.shift(P(0, 0, 0.02))


class DoublesRotation(ThreeDScene):
    # ---------- 配音对时 ----------
    def say(self, k):
        self.cues[k] = self.renderer.time
        self._cur = k

    def hold(self, pad=0.3):
        rem = self.cues[self._cur] + DURS[self._cur] + pad - self.renderer.time
        if rem > 0.02:
            self.wait(rem)

    # ---------- 屏幕固定元素 ----------
    def fix(self, *ms):
        self.add_fixed_in_frame_mobjects(*ms)
        self.remove(*ms)

    def set_panel(self, rows, size=38, at=(RCOL, 2.6), anim=True, maxw=3.5):
        g = VGroup(*[T(s, size, col, weight=w) for s, col, w in
                     [(r + (NORMAL,)) if len(r) == 2 else r for r in rows]])
        g.arrange(DOWN, aligned_edge=LEFT, buff=0.26)
        if g.width > maxw:
            g.scale_to_fit_width(maxw)
        g.move_to(P(at[0], at[1], 0), aligned_edge=UL)
        self.fix(g)
        anims = [FadeIn(g, shift=LEFT * 0.15)]
        if self.panel is not None:
            anims.insert(0, FadeOut(self.panel))
        self.play(*anims, run_time=0.6)
        self.panel = g

    def clear_panel(self):
        if self.panel is not None:
            self.play(FadeOut(self.panel), run_time=0.4)
            self.panel = None

    def scoreboard(self, a, b, serving):
        la = T("A·B", 40, AB_C, weight=BOLD)
        sc = T(f"{a} : {b}", 52, DEEP, weight=BOLD)
        lb = T("C·D", 40, CD_C, weight=BOLD)
        row = VGroup(la, sc, lb).arrange(RIGHT, buff=0.3)
        box = SurroundingRectangle(row, color=WHITE, fill_color=WHITE, fill_opacity=0.75,
                                   stroke_width=0, buff=0.22, corner_radius=0.15)
        mark = T("● 发球", 22, "#b8860b", weight=BOLD).next_to(la if serving == "AB" else lb, DOWN, buff=0.3)
        g = VGroup(box, row, mark)
        g.scale_to_fit_width(min(g.width, 4.0)).move_to(P(LCOL, 3.0, 0))
        return g

    def update_score(self, a, b, serving):
        new = self.scoreboard(a, b, serving)
        self.add_fixed_in_frame_mobjects(new)
        self.remove(new)
        self.play(FadeOut(self.sb), FadeIn(new), run_time=0.6)
        self.sb = new

    def banner(self, s, color):
        b = T(s, 40, color, weight=BOLD)
        box = SurroundingRectangle(b, fill_color=WHITE, fill_opacity=0.85, stroke_width=0,
                                   buff=0.2, corner_radius=0.12)
        g = VGroup(box, b).move_to(P(LCOL, 1.55, 0))
        self.fix(g)
        self.play(FadeIn(g, scale=1.15), run_time=0.4)
        return g

    def qmark(self, p, flip=False):
        q = T("?", 96, "#b8860b", weight=BOLD)
        q.set_stroke(WHITE, 3, background=True)
        q.rotate(PI / 2, RIGHT)          # 竖起来，面向 -y 方向的镜头
        if flip:
            q.rotate(PI, OUT)            # 面向 C·D 身后的镜头
        return q.move_to(p.get_center() + P(0, 0, 1.4))

    # ---------- 场上动作 ----------
    def serve(self, frm, to_zone, peak=3.2):
        s = frm.get_center() + P(0, 0, 0.9)
        x1, x2, y1, y2 = to_zone
        e = P((x1 + x2) / 2, y1 + (y2 - y1) * (0.35 if y1 > 0 else 0.65), 0.02)
        def f(t):
            p = s + (e - s) * t
            p[2] = s[2] * (1 - t) + e[2] * t + 4 * peak * t * (1 - t)
            return p
        # 轨迹和球共用同一个参数 t，保证球始终在轨迹最前端
        tk = ValueTracker(0.001)
        path = always_redraw(lambda: ParametricFunction(
            f, t_range=[0, max(tk.get_value(), 0.001)], color=HL, stroke_width=5))
        sh = Dot3D(s, radius=0.12, color=WHITE, resolution=(6, 6))
        sh.add_updater(lambda m: m.move_to(f(tk.get_value())))
        land = Circle(radius=0.35, color=HL, stroke_width=5).move_to(e)
        self.add(path, sh)
        self.play(tk.animate.set_value(1), run_time=1.1, rate_func=linear)
        sh.clear_updaters(); path.clear_updaters()
        self.play(FadeIn(land, scale=0.4), run_time=0.3)
        self.play(FadeOut(path), FadeOut(sh), FadeOut(land), run_time=0.4)

    def swap(self, p, q):
        a, b = p.get_center(), q.get_center()
        self.play(p.animate(path_arc=PI / 2).move_to(b),
                  q.animate(path_arc=PI / 2).move_to(a), run_time=1.1)

    def build_court(self):
        surf = Rectangle(width=2 * HW + 1.2, height=2 * HL_ + 1.2, fill_color=COURT,
                         fill_opacity=1, stroke_width=0)
        L = []
        def ln(a, b):
            L.append(Line(P(*a, 0.003), P(*b, 0.003)))
        ln((-HW, -HL_), (HW, -HL_)); ln((-HW, HL_), (HW, HL_))
        ln((-HW, -HL_), (-HW, HL_)); ln((HW, -HL_), (HW, HL_))
        ln((-WS, -HL_), (-WS, HL_)); ln((WS, -HL_), (WS, HL_))
        for sgn in (1, -1):
            ln((-HW, sgn * SS), (HW, sgn * SS))
            ln((-HW, sgn * DL), (HW, sgn * DL))
            ln((0, sgn * SS), (0, sgn * HL_))
        lines = VGroup(*L).set_stroke(WHITE, 3)
        net = Polygon(P(-HW - 0.2, 0, 0.0), P(HW + 0.2, 0, 0.0), P(HW + 0.2, 0, 1.55),
                      P(-HW - 0.2, 0, 1.55), fill_color=NET_C, fill_opacity=0.45,
                      stroke_color=WHITE, stroke_width=2)
        posts = VGroup(Line(P(-HW - 0.2, 0, 0), P(-HW - 0.2, 0, 1.55)),
                       Line(P(HW + 0.2, 0, 0), P(HW + 0.2, 0, 1.55))).set_stroke(POST, 5)
        return surf, lines, VGroup(net, posts)

    def construct(self):
        self.camera.background_color = BG
        self.cues, self.panel = {}, None

        surf, lines, net = self.build_court()
        A, B = Player("A", AB_C), Player("B", AB_C)
        C, D = Player("C", CD_C), Player("D", CD_C)
        A.move_to(SPOT[("AB", "R")]); B.move_to(SPOT[("AB", "L")])
        C.move_to(SPOT[("CD", "R")]); D.move_to(SPOT[("CD", "L")])
        players = [A, B, C, D]

        # ================= 0. 钩子（第 0 帧就有完整画面） =================
        self.set_camera_orientation(phi=55 * DEGREES, theta=-58 * DEGREES, zoom=0.6,
                                    frame_center=P(0, 0, 0))
        self.add(surf, lines, C, D, net, A, B)
        title = VGroup(T("双打发球", 80, DEEP, weight=BOLD),
                       T("谁发？", 80, CD_C, weight=BOLD),
                       T("站哪？", 80, CD_C, weight=BOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        title.scale_to_fit_width(min(title.width, 4.6)).move_to(P(LCOL, 1.2, 0))
        self.add_fixed_in_frame_mobjects(title)
        qs = VGroup(*[self.qmark(p) for p in players])
        self.say("hook")
        self.play(*[FadeIn(q, shift=OUT * 0.4) for q in qs], run_time=0.5)
        self.move_camera(**FPV_AB,
                         added_anims=[Wiggle(q, scale_value=1.4, rotation_angle=0.05 * TAU) for q in qs],
                         run_time=2.6)
        sub = VGroup(T("记住 3 句话", 40, DEEP, weight=BOLD), T("比分一报就知道", 40, DEEP)).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        sub.scale_to_fit_width(min(sub.width, 3.4)).move_to(P(RCOL, 1.6, 0), aligned_edge=LEFT)
        self.fix(sub)
        self.play(FadeIn(sub, shift=UP * 0.2), run_time=0.5)
        self.hold(0.1)
        self.play(FadeOut(title), FadeOut(sub), FadeOut(qs), *[FadeOut(p) for p in players], run_time=0.5)

        # ================= 1. 发球区（俯视） =================
        self.say("court")
        self.move_camera(**TOP, run_time=1.4)
        self.set_panel([("双打发球区", DEEP, BOLD), ("短而宽", "#b8860b", BOLD),
                        ("· 宽：到最外边线", DEEP),
                        ("· 短：到双打后发球线", DEEP),
                        ("（底线前 0.76 m）", "#4b7f6a")], at=(1.9, 2.4), maxw=5.0, size=44)
        dz = rect(0, HW, -DL, -SS, RZ, 0.85, stroke=HL)
        self.play(FadeIn(dz), run_time=0.6)
        self.wait(1.6)
        self.wait(0.5)
        self.hold(0.1)
        self.play(FadeOut(dz), run_time=0.4)

        # ================= 2. 三句话 =================
        self.say("r1")
        rz = rect(*ZONE[("AB", "R")], RZ, 0.85, stroke=HL)
        lz = rect(*ZONE[("AB", "L")], LZ, 0.75, stroke=WHITE)
        rl = T("偶数", 30, DEEP, weight=BOLD).move_to(P(HW / 2, -3.96, 0.01))
        ll = T("奇数", 30, DEEP, weight=BOLD).move_to(P(-HW / 2, -3.96, 0.01))
        for m in (rl, ll):
            m.scale(2.0)
        self.set_panel([("① 看发球方比分", DEEP, BOLD),
                        ("偶数 → 右区发", "#3f8f1f", BOLD),
                        ("奇数 → 左区发", "#1f78b4", BOLD),
                        ("（面向球网分左右）", "#4b7f6a")], at=(1.9, 2.4), maxw=5.0, size=44)
        self.wait(1.4)
        self.play(FadeIn(rz), FadeIn(rl), run_time=0.5)
        self.wait(0.6)
        self.play(FadeIn(lz), FadeIn(ll), run_time=0.5)
        self.hold(0.1)

        self.say("r2")
        self.set_panel([("② 发球方得分", DEEP, BOLD),
                        ("同一人接着发", DEEP),
                        ("和搭档左右换位", "#b8860b", BOLD)], at=(1.9, 2.4), maxw=5.0, size=44)
        self.hold(0.1)
        self.say("r3")
        self.set_panel([("③ 接发方得分", DEEP, BOLD),
                        ("拿回发球权", DEEP),
                        ("谁都不动！", CD_C, BOLD),
                        ("单双 → 那边的人发", DEEP)], at=(1.9, 2.4), maxw=5.0, size=44)
        self.hold(0.1)
        self.play(FadeOut(VGroup(rz, lz, rl, ll)), run_time=0.4)
        self.clear_panel()

        # ================= 3. 实战（发球人第一视角） =================
        self.say("w0")
        for p in players:
            self.add(p)
        self.add(net, A, B)   # 近处球员画在网前
        self.move_camera(**FPV_AB, added_anims=[FadeIn(p) for p in players], run_time=1.8)
        self.sb = self.scoreboard(0, 0, "AB")
        self.fix(self.sb)
        self.play(FadeIn(self.sb), run_time=0.5)
        ring = Circle(radius=0.9, color=HL, stroke_width=7).move_to(A.get_center() + P(0, 0, 0.01))
        self.play(Create(ring), run_time=0.5)
        ring.add_updater(lambda m: m.move_to(A.get_center() + P(0, 0, 0.01)))
        self.set_panel([("0 是偶数", DEEP), ("A 在右区", DEEP), ("A 发给 C", "#b8860b", BOLD)])
        self.wait(2.2)
        self.serve(A, ZONE[("CD", "R")])
        self.hold(0.1)

        self.say("w1")
        bn = self.banner("A·B 得分！", AB_C)
        self.update_score(1, 0, "AB")
        self.play(FadeOut(bn), run_time=0.3)
        self.set_panel([("发球方得分", AB_C, BOLD), ("A 接着发", "#b8860b", BOLD), ("和 B 换位", "#b8860b", BOLD)])
        self.swap(A, B)
        self.hold(0.1)

        self.say("w2")
        self.set_panel([("1 是奇数", DEEP), ("A 在左区", DEEP), ("A 发给 D", "#b8860b", BOLD)])
        self.wait(0.8)
        self.serve(A, ZONE[("CD", "L")])
        self.hold(0.1)

        self.say("w3")
        bn = self.banner("C·D 得分！", CD_C)
        self.update_score(1, 1, "CD")
        self.play(FadeOut(bn), run_time=0.3)
        self.set_panel([("接发方得分", CD_C, BOLD), ("换发球，谁都不动", "#b8860b", BOLD)])
        self.wait(1.6)
        ring.clear_updaters()
        self.play(ring.animate.move_to(D.get_center() + P(0, 0, 0.01)), run_time=0.5)
        ring.add_updater(lambda m: m.move_to(D.get_center() + P(0, 0, 0.01)))
        self.clear_panel()
        # 镜头绕到 C·D 身后；字母跟着转正
        self.add(surf, lines, ring, A, B, net, C, D)
        self.move_camera(**FPV_CD, added_anims=[Rotate(p.lab, PI, axis=OUT) for p in players], run_time=2.2)
        self.hold(0.1)

        self.say("w4")
        lz2 = rect(*ZONE[("CD", "L")], LZ, 0.7, stroke=WHITE)
        self.add(surf, lines, lz2, ring, A, B, net, C, D)
        self.set_panel([("C·D 1 分，奇数", DEEP), ("左区是 D", DEEP), ("D 发给 A", "#b8860b", BOLD)])
        self.play(FadeIn(lz2), run_time=0.5)
        self.wait(2.4)
        self.play(FadeOut(lz2), run_time=0.4)
        self.serve(D, ZONE[("AB", "L")])
        self.hold(0.1)

        self.say("w5")
        bn = self.banner("C·D 再得分！", CD_C)
        self.update_score(1, 2, "CD")
        self.play(FadeOut(bn), run_time=0.3)
        self.set_panel([("D 接着发", "#b8860b", BOLD), ("和 C 换位", "#b8860b", BOLD)])
        self.swap(D, C)
        self.set_panel([("2 是偶数", DEEP), ("D 在右区", DEEP), ("D 发给 B", "#b8860b", BOLD)])
        self.wait(0.6)
        self.serve(D, ZONE[("AB", "R")])
        self.hold(0.2)

        # ================= 4. 总结 =================
        self.say("sum")
        self.clear_panel()
        ring.clear_updaters()
        self.play(FadeOut(ring), FadeOut(self.sb), run_time=0.4)
        card = VGroup(
            T("比分单双定左右", 46, DEEP, weight=BOLD),
            T("发球方得分 → 换位", 46, AB_C, weight=BOLD),
            T("接发方得分 → 不动", 46, CD_C, weight=BOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.42)
        bg = SurroundingRectangle(card, fill_color=WHITE, fill_opacity=0.85, stroke_width=0,
                                  buff=0.45, corner_radius=0.2)
        cg = VGroup(bg, card).move_to(P(0, 0.5, 0))
        veil = Rectangle(width=16, height=9, fill_color=BG, fill_opacity=0.78, stroke_width=0)
        self.fix(veil, cg)
        self.play(FadeIn(veil), FadeIn(bg), run_time=0.4)
        self.wait(0.6)
        for it in card:
            self.play(FadeIn(it, shift=RIGHT * 0.3), run_time=0.45)
            self.wait(0.6)
        self.hold(0.3)
        self.play(FadeOut(cg), FadeOut(veil), run_time=0.4)

        # ================= 5. 互动题 =================
        self.say("quiz")
        self.sb = self.scoreboard(1, 2, "CD")
        self.fix(self.sb)
        self.play(FadeIn(self.sb), run_time=0.3)
        bn = self.banner("A·B 得分！", AB_C)
        self.update_score(2, 2, "AB")
        self.play(FadeOut(bn), run_time=0.3)
        qcard = VGroup(T("考考你", 40, "#b8860b", weight=BOLD),
                       T("该谁发？", 46, DEEP, weight=BOLD),
                       T("站哪边？", 46, DEEP, weight=BOLD),
                       T("发给谁？", 46, DEEP, weight=BOLD))
        qcard.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        qbg = SurroundingRectangle(qcard, fill_color=WHITE, fill_opacity=0.85, stroke_width=0,
                                   buff=0.35, corner_radius=0.2)
        qg = VGroup(qbg, qcard).move_to(P(RCOL, 1.4, 0), aligned_edge=LEFT)
        self.fix(qg)
        self.play(FadeIn(qg, shift=UP * 0.2), run_time=0.5)
        q2 = VGroup(*[self.qmark(p, flip=True) for p in (A, B)])
        self.play(*[FadeIn(q, shift=OUT * 0.4) for q in q2], run_time=0.4)
        self.wait(1.6)
        cm = VGroup(T("答案打在", 40, CD_C, weight=BOLD), T("评论区 ↓", 40, CD_C, weight=BOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(qg, DOWN, buff=0.35, aligned_edge=LEFT)
        self.fix(cm)
        self.play(FadeIn(cm, shift=UP * 0.2), run_time=0.5)
        self.play(*[Wiggle(q) for q in q2], run_time=1.2)
        self.hold(1.8)
        json.dump({"cues": self.cues, "total": self.renderer.time},
                  open("./cues.json", "w"), indent=1)
