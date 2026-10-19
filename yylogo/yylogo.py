from manimlib import *
from math import sqrt
from decimal import Decimal

get_angle = lambda c: np.angle(-c) + PI if not c/abs(c) == 1 else 0
convert_angle = lambda a: a if a>=0 else a + TAU


class Compass(VGroup):

    CONFIG = {
        # 'stroke_color': GREY_E,
        # 'fill_color': WHITE,
        'fill_color': '#c9e9dc',
        'stroke_color': '#c9e9dc',
        'stroke_width': 2,
        'leg_length': 3,
        'leg_width': 0.12,
        'r': 0.2,
        'depth_test': True,
    }

    def __init__(self, span=2.5,  **kwargs):

        VGroup.__init__(self, **kwargs)
        self.span = span
        self.create_compass()


    # def create_compass_old(self):
    #
    #     s, l, r = self.span, self.leg_length, self.r
    #     theta = np.arcsin(s/2/l)
    #     arc = Arc(start_angle=-PI/2 + theta, angle=TAU-theta*2, radius=r, stroke_color=self.stroke_color, stroke_width=self.stroke_width*4)
    #     dot = Dot(color=self.stroke_color).set_height(self.stroke_width*8/100)
    #     leg_01 = Line(arc.get_center(), arc.get_center() + complex_to_R3(l * np.exp(1j * (-PI/2-theta))), stroke_color=self.stroke_color, stroke_width=self.stroke_width)
    #     leg_02 = Line(arc.get_center(), arc.get_center() + complex_to_R3(l * np.exp(1j * (-PI/2+theta))), stroke_color=self.stroke_color, stroke_width=self.stroke_width * 1)
    #     leg_11 = Line(arc.get_center(), arc.get_center() + complex_to_R3((l - r * 0.8) * np.exp(1j * (-PI/2-theta))), stroke_color=self.stroke_color, stroke_width=self.stroke_width * 4)
    #     leg_12 = Line(arc.get_center(), arc.get_center() + complex_to_R3((l - r * 0.8) * np.exp(1j * (-PI/2+theta))), stroke_color=self.stroke_color, stroke_width=self.stroke_width * 4)
    #     pen_point = Dot(color=self.stroke_color).set_height(self.stroke_width * 1/125).move_to(leg_02.get_end())
    #     leg_1, leg_2 = VGroup(leg_01, leg_11),  VGroup(leg_02, leg_12, pen_point)
    #     head = Line(UP * r, UP * (r + r * 1), stroke_color=self.stroke_color, stroke_width=self.stroke_width * 4)
    #
    #     self.add(arc, dot, head, leg_1, leg_2)
    #     self.move_to(ORIGIN)
    #
    #     return self

    def create_compass(self):

        s, l, r, w = self.span, self.leg_length, self.r, self.leg_width
        self.theta = np.arcsin(s/2/l)

        self.c = Circle(radius=r, fill_color=self.fill_color, fill_opacity=1, stroke_color=self.stroke_color, stroke_width=self.stroke_width*5)
        c2 = Circle(radius=r+self.stroke_width*5/100/2, fill_opacity=0, stroke_color=self.fill_color, stroke_width=self.stroke_width)

        self.leg_1 = Polygon(ORIGIN, l * RIGHT, (l-w*np.sqrt(3)) * RIGHT + w * DOWN, w * DOWN,
                             stroke_width=0, stroke_color=self.fill_color, fill_color=self.stroke_color,
                             fill_opacity=1).rotate(-PI/2-self.theta, about_point=self.c.get_center())
        self.leg_2 = Polygon(ORIGIN, l * RIGHT, (l-w*np.sqrt(3)) * RIGHT + w * UP, w * UP,
                             stroke_width=0, stroke_color=self.fill_color, fill_color=self.stroke_color,
                             fill_opacity=1).rotate(-PI/2+self.theta, about_point=self.c.get_center())


        # self.leg_1, self.leg_2 = VGroup(leg_01, leg_11),  VGroup(leg_02, leg_12, pen_point)
        h = Line(UP * r, UP * (r + r * 1.8), stroke_color=self.stroke_color, stroke_width=self.stroke_width*6)

        self.head = VGroup(h, self.c, c2)
        self.add(self.leg_1, self.leg_2, self.head)
        self.move_to(ORIGIN)

        return self

    def get_niddle_tip(self):
        return self.leg_1.get_vertices()[1]

    def get_pen_tip(self):
        return self.leg_2.get_vertices()[1]

    def move_niddle_tip_to(self, pos):
        self.shift(pos-self.get_niddle_tip())
        return self

    def rotate_about_niddle_tip(self, angle=PI/2):
        self.rotate(angle=angle, about_point=self.get_niddle_tip())

    def get_span(self):
        # return self.span 如果进行了缩放而self.span没变会有问题
        return get_norm(self.get_pen_tip() - self.get_niddle_tip())

    def set_span(self, s):
        self.span = s
        l, r, w = self.leg_length, self.r, self.leg_width
        theta_new, theta_old = np.arcsin(s/2/l), self.theta
        sign = np.sign(get_angle(R3_to_complex(self.leg_2.get_vertices()[1] - self.leg_2.get_vertices()[0])) - get_angle(R3_to_complex(self.leg_1.get_vertices()[1] - self.leg_1.get_vertices()[0])))
        rotate_angle = 2 * (theta_new - theta_old) * sign
        self.leg_2.rotate(rotate_angle, about_point=self.c.get_center())
        self.theta=theta_new
        self.head.rotate(rotate_angle/2, about_point=self.c.get_center())
        self.rotate_about_niddle_tip(-rotate_angle/2)
        return self

    def set_compass(self, center, pen_tip):
        self.move_niddle_tip_to(center)
        self.set_span(get_norm(pen_tip - center))
        self.rotate_about_niddle_tip(np.angle(R3_to_complex(pen_tip - center)) - np.angle(R3_to_complex(self.get_pen_tip() - center)))
        return self

    def set_compass_to_draw_arc(self, arc):
        return self.set_compass(arc.arc_center, arc.get_start())

    def reverse_tip(self):
        return self.flip(axis=self.head[0].get_end() - self.head[0].get_start(), about_point=self.c.get_center())

class yylogo_draw(Scene):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.TRIANGLE_SIDE_LENGTH = 36 #三角形边长
    
    def construct(self):

        frame = self.camera.frame
        frame.move_to(np.array([30,0,0])),
        self.play(
            
            frame.animate.set_width(200), # 旋转缩放相机帧
            
            run_time=0
        )
        path2 = VMobject()
        start_point = np.array([0,0,0])
        path_point = start_point
        path2.start_new_path(np.array([0,0,0]))
        path2.add_line_to(np.array([36,0,0]))
        path2.add_line_to(np.array([18,-18*sqrt(3),0]))

        arc = ArcBetweenPoints(np.array([0,0,0]),np.array([18,-18*sqrt(3),0]),angle = -PI/3)
        # path2.add_line_to(arc.get_points()[-1])
        path2.add_subpath(arc.get_points()[::-1])
        # path2.add_line_to(start_point)
        
        # self.play(ShowCreation(path2))
        # self.play(ShowCreation(arc))


        path3 = VMobject()
        start_point = np.array([36,0,0]) 
        path_point = start_point
        path3.start_new_path(np.array([0,0,0])+ start_point)
        path3.add_line_to(np.array([36,0,0])+start_point)
        path3.add_line_to(np.array([18,-18*sqrt(3),0])+start_point)

        arc2 = ArcBetweenPoints(np.array([0,0,0])+start_point,np.array([18,-18*sqrt(3),0])+start_point,angle = -PI/3)
        path3.add_subpath(arc2.get_points()[::-1])
        # self.play(ShowCreation(path3))

        path2.set_fill(color='#feffff',opacity=1)
        path3.set_fill(color='#feffff',opacity=1)

        self.play(DrawBorderThenFill(path2),
        DrawBorderThenFill(path3))
        pass


class DrawingScene(Scene):

    CONFIG = {
        'compass_config':{
            'stroke_color': GREY_E,
            # 'fill_color': WHITE,
            'fill_color': '#c9e9dc',
            'stroke_width': 3,
            'leg_length': 4.5,
            'leg_width': 0.18,
            'r': 0.3,
            'depth_test': True,
        },
        'ruler_config':{
            'width': 15,
            'height': 1.2,
            'stroke_width': 8,
            'stroke_color': GREY_E,
            'stroke_opacity': 0.4,
            'fill_color': WHITE,
            'fill_opacity': 0.5,
        },
        'dot_config':{
            'radius': 0.1,
            'color': GREY_E,
        },
        'line_config':{
            'stroke_color': GREY_E,
            'stroke_width': 5,
        },
        'brace_config':{
            'fill_color': GREY_E,
            'buff':0.025,
        },
        'text_config':{
            'size': 0.6 * 5, # 5 times than the actual size and the sacle down
            'font': 'Cambria Math',
            'color': GREY_E,
        },
        'add_ruler': False,
    }

    def setup(self):
        self.cp = Compass(**self.compass_config)
        self.ruler = VGroup(Rectangle(**self.ruler_config).set_height(self.ruler_config['height'] - self.ruler_config['stroke_width']/2/100, stretch=True)\
                            .round_corners(self.ruler_config['height']/8),
                            Rectangle(**self.ruler_config).set_opacity(0))
        self.dot = Dot(**self.dot_config)

        self.cp.move_to(UP * 10)
        if self.add_ruler:
            self.ruler.move_to(DOWN * 10)
            self.add(self.ruler)
        self.add(self.cp)

        self.temp_points = []

    def construct(self):

        self.add(self.cp)
        self.play(self.cp.move_niddle_tip_to, ORIGIN, run_time=1)
        self.wait(0.3)
        self.set_span(3.6, run_time=1, rate_func=smooth)
        self.wait(0.5)
        self.set_compass(DL * 0.5, UR * 0.5, run_time=1, rate_func=there_and_back)
        arc = Arc(color=GREY_E)
        self.set_compass_to_draw_arc(arc)
        self.draw_arc_by_compass(arc)

        self.wait()

    def set_span(self, s, run_time=1, rate_func=smooth):

        s_old = self.cp.get_span()
        n = int(run_time * self.camera.frame_rate)
        dt = 1/self.camera.frame_rate
        t_series = np.linspace(1, n, n)/n
        # s_series = s_old + rate_func(t_series) * (s - s_old)
        s_series = [s_old + rate_func(t_series[i]) * (s - s_old) for i in range(n)]
        for i in range(n):
            self.cp.set_span(s_series[i])
            self.wait(dt)

    def set_compass_direction(self, start, end, run_time=1, rate_func=smooth):
        vect = end - start
        a = np.angle(R3_to_complex(vect))
        c_old, p_old = self.cp.get_niddle_tip(), self.cp.get_pen_tip()
        a_old = np.angle(R3_to_complex(p_old - c_old))
        n = int(run_time * self.camera.frame_rate)
        dt = 1/self.camera.frame_rate
        t_series = np.linspace(1, n, n)/n
        c_series = [c_old + rate_func(t_series[i]) * (start - c_old) for i in range(n)]
        delta_a = (a - a_old)/n
        for i in range(n):
            self.bring_to_front(self.cp)
            self.cp.move_niddle_tip_to(c_series[i])
            self.cp.rotate_about_niddle_tip(delta_a)
            self.wait(dt)

    def set_compass(self, center, pen_tip, run_time=1, rate_func=smooth, emphasize_dot=False):
        if emphasize_dot:
            run_time -= 0.15
        c_old, p_old = self.cp.get_niddle_tip(), self.cp.get_pen_tip()
        n = int(run_time * self.camera.frame_rate)
        dt = 1/self.camera.frame_rate
        t_series = np.linspace(1, n, n)/n
        # s_series = s_old + rate_func(t_series) * (s - s_old)
        c_series = [c_old + rate_func(t_series[i]) * (center - c_old) for i in range(n)]
        p_series = [p_old + rate_func(t_series[i]) * (pen_tip - p_old) for i in range(n)]

        for i in range(n):
            self.bring_to_front(self.cp)
            self.cp.set_compass(c_series[i], p_series[i])
            self.wait(dt)
        if emphasize_dot:
            self.emphasize_dot([center, pen_tip], run_time=0.15)

    def set_compass_(self, center, pen_tip, adjust_angle=0, run_time=1, rate_func=smooth, emphasize_dot=False):

        vect = center - pen_tip
        a = np.angle(R3_to_complex(vect)) + adjust_angle
        s = get_norm(vect)
        c_old, p_old, s_old = self.cp.get_niddle_tip(), self.cp.get_pen_tip(), self.cp.get_span()
        a_old = np.angle(R3_to_complex(p_old - c_old))
        if emphasize_dot:
            run_time -= 0.15
        n = int(run_time * self.camera.frame_rate)
        dt = 1/self.camera.frame_rate
        t_series = np.linspace(1, n, n)/n
        c_series = [c_old + rate_func(t_series[i]) * (center - c_old) for i in range(n)]
        delta_a = (a - a_old)/n
        s_series = [s_old + rate_func(t_series[i]) * (s - s_old) for i in range(n)]

        for i in range(n):
            self.bring_to_front(self.cp)
            self.cp.move_niddle_tip_to(c_series[i])
            self.cp.rotate_about_niddle_tip(delta_a)
            self.cp.set_span(s_series[i])
            self.wait(dt)
        if emphasize_dot:
            self.emphasize_dot([center, pen_tip], run_time=0.15)

    def set_compass_to_draw_arc(self, arc,start = None, **kwargs):
        if start is None:
            self.set_compass(arc.arc_center, arc.get_start(), **kwargs)
        else:
            self.set_compass_(arc.arc_center, start, **kwargs)

    def set_compass_to_draw_arc_(self, arc, start = None,**kwargs):
        if start is None:
            self.set_compass_(arc.arc_center, arc.get_start(), **kwargs)
        else:
            self.set_compass_(arc.arc_center, start, **kwargs)

    def draw_arc_by_compass(self, arc, is_prepared=True, run_time=1, rate_func=smooth, reverse=False, add_center=False, **kwargs):
        self.bring_to_front(self.cp)
        if not is_prepared: self.set_compass_to_draw_arc(arc, run_time=0.5)
        theta = arc.angle if not reverse else -1 * arc.angle
        self.play(Rotating(self.cp, angle=theta, about_point=self.cp.get_niddle_tip()), ShowCreation(arc), rate_func=rate_func, run_time=run_time)
        if add_center:
            d = Dot(self.cp.get_niddle_tip(), **self.dot_config).scale(0.5)
            self.temp_points.append(d)
            self.add(d)

    def emphasize_dot(self, pos, add_dot=False, size=1.2, run_time=0.2, **kwargs):
        if type(pos) == list:
            d = VGroup(*[Dot(pos[i], radius=size/2, color=GREY_C, fill_opacity=0.25).scale(0.25) for i in range(len(pos))])
        else:
            d = Dot(pos, radius=size/2, color=GREY_C, fill_opacity=0.25).scale(0.25)
        self.add(d)
        if type(pos) == list:
            self.play(d[0].scale, 4, d[1].scale, 4, rate_func=linear, run_time=run_time)
            
        else:
            self.play(d.scale, 4, rate_func=linear, run_time=run_time)

        self.remove(d)
        if add_dot:
            if type(pos) == list:
                dot = VGroup(*[Dot(pos[i],**kwargs) for i in range(len(pos))])
            else:
                dot = Dot(pos, **kwargs)
            self.add(dot)
            return dot

    def set_ruler(self, pos1, pos2, run_time=1, rate_func=smooth):
        p1, p2 = self.ruler[-1].get_vertices()[1], self.ruler[-1].get_vertices()[0]
        c12 = (p1 + p2) / 2
        center = (pos1 + pos2)/2
        self.bring_to_front(self.ruler)
        self.play(self.ruler.shift, center - c12, run_time=run_time/2, rate_func=rate_func)
        self.play(Rotating(self.ruler, angle=np.angle(R3_to_complex(pos2 - pos1)) - np.angle(R3_to_complex(p2 - p1)), about_point=center), run_time=run_time/2, rate_func=rate_func)

    def draw_line(self, pos1, pos2, is_prepared=True, run_time=1.2, rate_func=smooth, pre_time=0.8,emphasize = True,dashed = False):
        if not is_prepared: self.set_ruler(pos1, pos2, run_time=pre_time)
        self.dot.move_to(pos1)
        if emphasize:
            self.emphasize_dot(pos1, run_time=0.15)
        self.add(self.dot)
        if dashed:
            l = DashedLine(pos1, pos2, **self.line_config,positive_space_ratio = 0.3)
        else:
            l = Line(pos1, pos2, **self.line_config)
        self.play(ShowCreation(l), self.dot.move_to, pos2, run_time=run_time-0.3, rate_func=rate_func)
        self.emphasize_dot(pos2, run_time=0.15)
        self.remove(self.dot)
        return l

    def draw_line_(self, l, is_prepared=True, run_time=1.2, rate_func=smooth):
        pos1, pos2 = l.get_start(), l.get_end()
        if not is_prepared: self.set_ruler(pos1, pos2, run_time=0.5)
        self.dot.move_to(pos1)
        self.emphasize_dot(pos1, run_time=0.15)
        self.add(self.dot)
        # l = Line(pos1, pos2, **self.line_config)
        self.play(ShowCreation(l), self.dot.move_to, pos2, run_time=run_time-0.3, rate_func=rate_func)
        self.emphasize_dot(pos2, run_time=0.15)
        self.remove(self.dot)
        return l

    def put_aside_ruler(self, direction=DOWN, run_time=0.5):
        self.bring_to_front(self.ruler)
        self.play(self.ruler.move_to, direction * 15, run_time=run_time)

    def put_aside_compass(self, direction=DOWN, run_time=0.5):
        self.bring_to_front(self.cp)
        self.play(self.cp.move_to, direction * 15, run_time=run_time)

    def get_length_label(self, p1, p2, text='', reverse_label=False, add_bg=False, bg_color=WHITE):
        l = Line(p1, p2)
        b = Brace(l, direction=complex_to_R3(np.exp(1j * (l.get_angle()+PI/2 * (1 -2 * float(reverse_label))))), **self.brace_config)
        t = Text(text, **self.text_config).scale(0.2)
        if add_bg:
            bg = SurroundingRectangle(t, fill_color=bg_color, fill_opacity=0.6, stroke_opacity=0).set_height(t.get_height() + 0.05, stretch=True).set_width(t.get_width() + 0.05, stretch=True)
            b.put_at_tip(bg, buff=0.0)
            b.put_at_tip(t, buff=0.05)
            return b, bg, t
        else:
            b.put_at_tip(t, buff=0.05)
            return b, t

    def set_compass_and_show_span(self, p1, p2, run_time=1, show_span_time=[0.4, 0.3, 0.9, 0.4], text='', reverse_label=False, add_bg=True, **kwargs):
        self.set_compass(p1, p2, run_time=run_time, **kwargs)
        bt = self.get_length_label(p1, p2, text=text, reverse_label=reverse_label, add_bg=add_bg)
        b, t = bt[0], bt[-1]
        st = show_span_time
        self.play(ShowCreation(b), run_time=st[0])
        if add_bg:
            self.add(bt[1])
            self.play(FadeIn(t), run_time=st[1])
        else:
            self.play(FadeIn(t), run_time=st[1])
        self.wait(st[2])
        self.play(FadeOut(VGroup(*bt)), run_time=st[3])
        return bt

    def set_compass_and_show_span_(self, p1, p2, run_time=1, show_span_time=[0.4, 0.3, 0.9, 0.4], text='', reverse_label=False, add_bg=True, **kwargs):
        self.set_compass_(p1, p2, run_time=run_time, **kwargs)
        bt = self.get_length_label(p1, p2, text=text, reverse_label=reverse_label)
        b, t = bt[0], bt[-1]
        st = show_span_time
        self.play(ShowCreation(b), run_time=st[0])
        if add_bg:
            self.add(bt[1])
            self.play(FadeIn(t), run_time=st[1])
        else:
            self.play(FadeIn(t), run_time=st[1])
        self.wait(st[2])
        self.play(FadeOut(VGroup(*bt)), run_time=st[3])
        return bt

    def highlight_on(self, *mobjects, to_front=True, stroke_config={'color': '#66CCFF', 'width': 4}, run_time=1, **kwargs):
        self.highlight = VGroup(*mobjects)
        self.play(self.highlight.set_stroke, stroke_config, run_time=run_time, **kwargs)
        if to_front:
            self.bring_to_front(self.highlight)
            self.bring_to_front(self.cp, self.ruler)

    def highlight_off(self, *mobjects):

        pass

    def show_arc_info(self, arc, time_list=[0.5, 0.2, 0.3]):

        c, r, s, a, ps, pe = arc.arc_center, arc.radius, arc.start_angle, arc.angle, arc.get_start(), arc.get_end()
        d_center = Dot(c, radius=0.08, color=PINK)
        r1, r2 = DashedLine(c, ps, stroke_width=3.5, stroke_color=PINK), DashedLine(c, pe , stroke_width=3.5, stroke_color=PINK)
        arc_new = Arc(arc_center=c, radius=r, start_angle=s, angle=a, stroke_width=8, stroke_color=RED)
        self.play(ShowCreation(arc_new), run_time=time_list[0])
        self.play(FadeIn(arc_new), run_time=time_list[1])
        self.play(ShowCreation(r1), ShowCreation(r2), run_time=time_list[2])
class Apple_logo(VGroup):

    CONFIG = {
        'scale': 0.25,
        'logo_color': RED_D,
        'logo_stroke': 8,
        'coord_center': DOWN * 1.25,
        'assistent_lines_config': {
            'stroke_width': 2,
            'stroke_color': GREY,
        },
        'key_lines_config': {
            'stroke_width': 2.5,
            'stroke_color': GREY_E,
        },
        'step_size': 0.02,
        'create_shape': True,

    }

    def __init__(self, **kwargs):

        VGroup.__init__(self, **kwargs)
        self.set_key_lines()
        self.set_outline()
        if self.create_shape:
            self.set_logo_shape()

    def set_key_lines(self):

        s = self.scale
        center = self.coord_center
        self.c1 = Circle(arc_center=center+ORIGIN, radius=1/2*s, **self.key_lines_config)
        self.c5_r = Circle(arc_center=center+3*s*RIGHT, radius=5/2*s, **self.key_lines_config)
        self.c5_l = Circle(arc_center=center+3*s*LEFT,  radius=5/2*s, **self.key_lines_config)
        # self.c5_l = self.c5_r.copy().flip()
        self.c8_d = Circle(arc_center=center + s * 5.77 * DOWN, radius=8/2*s, **self.key_lines_config)
        self.c13  = Circle(arc_center=center + s * 4.73 * UP, radius=13/2*s, **self.key_lines_config)
        self.c8_r = Circle(arc_center=center + s * ( 3.48 * RIGHT + 7.69 * UP),
                           radius=8/2*s, **self.key_lines_config)
        self.c8_l = Circle(arc_center=center + s * (-3.48 * RIGHT + 7.69 * UP),
                           radius=8/2*s, **self.key_lines_config)
        self.c3_r = Circle(arc_center=center + s * ( 5.9 * RIGHT + 2.75 * UP),
                           radius=3/2*s, **self.key_lines_config)
        self.c3_l = Circle(arc_center=center + s * (-5.9 * RIGHT + 2.75 * UP),
                           radius=3/2*s, **self.key_lines_config)
        self.c24_r = Circle(arc_center=center + s * ( 3.89 * RIGHT + 6.54 * UP),
                           radius=24/2*s, **self.key_lines_config)
        self.c24_l = Circle(arc_center=center + s * (-3.89 * RIGHT + 6.54 * UP),
                           radius=24/2*s, **self.key_lines_config)


        self.c12_r = Circle(arc_center=center + s * ( 2.11 * RIGHT + 6.23 * UP),
                           radius=12/2*s, **self.key_lines_config)
        self.c12_l = Circle(arc_center=center + s * (-2.11 * RIGHT + 6.23 * UP),
                           radius=12/2*s, **self.key_lines_config)
        self.c8_u = Circle(arc_center=center + s * 14.89 * UP, radius=8/2*s, **self.key_lines_config)
        self.c8_01 = Circle(arc_center=center + s * (8.82 * RIGHT + 6.23 * UP),
                            radius=8/2*s, **self.key_lines_config)
        self.c8_02 = Circle(arc_center=center + s * (3.61 * RIGHT + 12.23 * UP),
                            radius=8/2*s, **self.key_lines_config)
        self.c8_03 = Circle(arc_center=center + s * (-0.46 * RIGHT + 15.69 * UP),
                            radius=8/2*s, **self.key_lines_config)

        self.key_lines = VGroup(self.c1, self.c5_r, self.c5_l,
                                self.c8_d, self.c13,
                                self.c8_r, self.c8_l,
                                self.c3_r, self.c3_l,
                                self.c24_r, self.c24_l,
                                self.c12_r, self.c12_l,
                                self.c8_u,
                                self.c8_01,
                                self.c8_02, self.c8_03,
                                )
        self.key_lines_center = VGroup(* [Dot(c.get_center(), stroke_color=self.key_lines_config['stroke_color'],
                                              radius=self.key_lines_config['stroke_width']/100) for c in self.key_lines])
        return self

    def set_outline(self):
        s = self.scale
        center = self.coord_center
        # kp_list = [[7.41, 2.49, 0], [4.81, -1.72, 0], [1.85, -2.22, 0], [-1.85, -2.22, 0], [-4.81, 1.72, 0], [-8.1, 5.91, 0],
        #            [-6.22, 10.6, 0], [-1.74, 11.29, 0], [1.74, 11.29, 0], [6.22, 10.6, 0], [6.95, 9.77, 0], [-0.37, 11.87, 0], [3.42, 16.22, 0]]
        kp_list = [[6.95, 9.77, 0], [6.22, 10.6, 0], [1.74, 11.29, 0], [-1.74, 11.29, 0], [-6.22, 10.6, 0], [-8.1, 5.91, 0],
                   [-4.81, -1.72, 0], [-1.85, -2.22, 0], [1.85, -2.22, 0], [4.81, -1.72, 0], [7.41, 2.49, 0], [-0.35, 11.69, 0], [3.5, 16.23, 0]]

        self.key_angles = np.array([10.62, 69, -51.5, 69, 49.77, 40.52, 73.94, -54.97, 73.94, 23.77, -131.51, 96.09, -96.09]) * DEGREES
        self.key_radius = np.array([12/2, 8/2, 8/2, 8/2, 12/2, 24/2, 5/2, 8/2, 5/2, 24/2, 8/2]) * s
        self.key_points = np.array(kp_list) * s + center
        n = len(kp_list)
        self.outline_by_arcs = VGroup_(step_size=self.step_size)
        for i in range(n-2):
            p1, p2 = self.key_points[i], self.key_points[(i+1) % (n-2)]
            arc_i = ArcBetweenPoints(p1, p2, angle=self.key_angles[i], radius=self.key_radius[i], stroke_color=self.logo_color, stroke_width=self.logo_stroke)
            self.outline_by_arcs.add(arc_i)
        arc_1 = ArcBetweenPoints(self.key_points[-2], self.key_points[-1], angle=self.key_angles[-2], radius=self.key_radius[-2], stroke_color=self.logo_color, stroke_width=self.logo_stroke)
        arc_2 = ArcBetweenPoints(self.key_points[-2], self.key_points[-1], angle=self.key_angles[-1], radius=self.key_radius[-1], stroke_color=self.logo_color, stroke_width=self.logo_stroke)

        self.outline_by_arcs.add(arc_1, arc_2)
        return self

    def set_logo_shape(self):
        s = self.scale
        center = self.coord_center
        self.outline_by_arcs.get_all_outline_points()
        self.shape_1 = self.outline_by_arcs.get_shape(center=center + s * (-3.89 * RIGHT + 6.54 * UP), fill_color=self.logo_color, fill_opacity=1, stroke_color=self.logo_color, stroke_width=self.logo_stroke)
        self.shape_2 = self.outline_by_arcs.get_shape(center=center + s * (1.52 * RIGHT + 14.05 * UP), fill_color=self.logo_color, fill_opacity=1, stroke_color=self.logo_color, stroke_width=self.logo_stroke)
        # shape_1.set_fill(self.logo_color, 1).set_stroke(self.logo_color, self.logo_stroke, 1)
        # shape_2.set_fill(self.logo_color, 1).set_stroke(self.logo_color, self.logo_stroke, 1)
        self.add(self.shape_1, self.shape_2)
        return self

class Test_01(Scene):

    def construct(self):

        logo = Apple_logo()
        kl = logo.key_lines
        ol = logo.outline_by_arcs
        self.play(ShowCreation(kl), run_time=6)
        self.wait(0.25)
        # self.play(ShowCreation(ol), run_time=4)
        # self.wait(0.8)

        self.play(DrawBorderThenFill(logo.shape_1, stroke_width=logo.logo_stroke), run_time=3)
        self.play(DrawBorderThenFill(logo.shape_2, stroke_width=logo.logo_stroke), run_time=1.6)
        self.wait(0.2)
        self.play(Uncreate(kl), run_time=1.5)

        self.wait(2)

class Test_compass(Scene):

    def construct(self):
        coord = NumberPlane(axis_config={"stroke_color": GREY_D}, background_line_style={"stroke_color": BLUE_C},)
        self.add(coord)
        cp = Compass(stroke_color=PINK)
        c = Circle(radius=cp.get_span())
        self.add(cp)
        self.wait()
        self.play(cp.move_niddle_tip_to, ORIGIN, run_time=1)
        self.wait()

        self.bring_to_front(cp)
        self.play(Rotating(cp, about_point=cp.get_niddle_tip()), ShowCreation(c), rate_func=smooth, run_time=1.5)
        self.bring_to_front(cp)
        c1 = Circle(stroke_color=GREY_E)
        # self.play(cp.set_span, 1, run_time=1)
        # cp.set_span(1)
        # self.wait()
        # self.play(Rotating(cp, about_point=cp.get_niddle_tip()), ShowCreation(c1), rate_func=smooth, run_time=1.5)
        self.bring_to_front(cp)
        # self.play(cp.set_compass, DL * 2, UR * 2, run_time=1.5)
        cp.set_compass(DL * 2, UR * 2)

        self.wait(1)
   

class Test_1(DrawingScene):

    def construct(self):
        # print(self.camera.get_pixel_size())
        print(self.camera.background_rgba)
        s = 0.5
        # axis = Axes(x_range=[-30, 30, 1], y_range=[-20, 20, 1], axis_config={"stroke_color": GREY_D, "stroke_width": 2.5, "stroke_opacity": 1},).scale(s)
        # logo = Apple_logo(create_shape=False, coord_center=ORIGIN, scale=s*2)
        # self.add(axis, logo.c1)
        c = Circle(color=BLACK)
        c1 = Circle(color=BLACK)
        c2 = Circle(color=BLACK)
        self.add(c, c1, c2)
        self.wait()
        self.play(ApplyMethod(c.shift, RIGHT * 4, run_time=1),
                  ApplyMethod(c1.shift, RIGHT * 4, run_time=2),
                  ApplyMethod(c2.shift, RIGHT * 4, run_time=4)
        )
        # self.play(self.camera.set_background_color( RED, 1 ))
        self.camera.background_rgba = list(color_to_rgba('#2aa570', 1))
        

class Step_0(DrawingScene):

    '''
    画出基本的直角坐标系作为辅助
    '''

    def construct(self):
        s = 0.5
        # coord = NumberPlane(x_range=[-15, 15, 1], y_range=[-15, 15, 1], axis_config={"stroke_color": GREY_D}, background_line_style={"stroke_color": BLUE_C},).scale(s)
        # logo = Apple_logo(create_shape=False, coord_center=ORIGIN, scale=s)
        self.cp.move_to(UP * 10)
        # self.add(coord)
        self.wait()
        self.play(FadeIn(self.ruler))

        l1 = self.draw_line(LEFT * 4.5, RIGHT * 4.5, is_prepared=False)
        self.put_aside_ruler()
        self.wait()

        arc_1 = Arc(arc_center=LEFT * 2, radius=3, start_angle=-PI/3, angle=2*PI/3, **self.line_config)
        arc_2 = Arc(arc_center=RIGHT * 2, radius=3, start_angle=2 * PI/3, angle=2*PI/3, **self.line_config)

        self.play(self.cp.move_to, ORIGIN)
        self.wait(0.2)
        self.set_compass_to_draw_arc(arc_1, emphasize_dot=True)
        self.draw_arc_by_compass(arc_1)
        self.wait(0.1)
        self.set_compass_to_draw_arc_(arc_2, adjust_angle=PI, emphasize_dot=True)
        self.draw_arc_by_compass(arc_2)
        self.wait(0.2)
        self.put_aside_compass()
        self.set_ruler(UP, DOWN)
        l2 = self.draw_line(UP * 3, DOWN * 3)
        self.put_aside_ruler(direction=LEFT)

        self.wait(0.6)
        self.play(FadeOut(arc_1), FadeOut(arc_2), l1.scale, 2, l2.scale, 2, run_time=1.2)
        self.wait(0.8)

        c1 = Circle(radius=1*s, **self.line_config)
        # c2_l = Circle(arc_center=6*s*LEFT, radius=5*s, **self.line_config)
        # c2_r = Arc(arc_center=6*s*RIGHT, radius=5*s, start_angle=PI, angle=-TAU, **self.line_config)
        self.set_compass_to_draw_arc(c1, run_time=1.2)
        self.wait(0.12)
        self.draw_arc_by_compass(c1)
        self.wait(0.2)
        arcs = VGroup(*[Arc(arc_center=i*s*RIGHT, radius=1*s, start_angle=-PI/6, angle=PI/3, **self.line_config) for i in range(1, 7)])
        for i in range(6):
            self.set_compass_to_draw_arc(arcs[i], run_time=0.32, emphasize_dot=False)
            self.draw_arc_by_compass(arcs[i], run_time=0.5)
        self.wait(0.6)
        axis = Axes(x_range=[-15, 15, 1], y_range=[-10, 10, 1], axis_config={"stroke_color": GREY_D, "stroke_width": 2.5}, ).scale(s)
        dot = Dot(color=GREY_E, radius=0.06)
        self.play(FadeIn(axis), FadeIn(dot), FadeOut(l1), FadeOut(l2), FadeOut(self.cp), FadeOut(arcs))
        self.wait(2)

class Perpendicular_bisector(DrawingScene):

    CONFIG = {
        'compass_config':{
            'stroke_color': GREY_E,
            'fill_color': WHITE,
            'stroke_width': 2,
            'leg_length': 3.6,
            'leg_width': 0.12,
            'r': 0.2,
            'depth_test': True,
        },
        'add_ruler': True,
    }

    def construct(self):

        l = Line(LEFT * 3, RIGHT * 3, stroke_width=8, stroke_color='#66CCFF')
        d1, d2 = Dot(l.get_start(), color=GREY_C).set_height(0.2), Dot(l.get_end(), color=GREY_C).set_height(0.2)
        self.add(l, d1, d2)
        self.wait()
        self.set_compass(l.get_start(), l.get_start()+RIGHT*2)
        self.wait(0.1)
        self.set_compass(l.get_start(), l.get_start()+RIGHT*4, run_time=0.75)
        self.wait(0.1)
        arc_l = Arc(arc_center=l.get_start(), start_angle=-60*DEGREES, angle=120*DEGREES, radius=4, **self.line_config)
        arc_r = Arc(arc_center=l.get_end(),   start_angle=120*DEGREES, angle=120*DEGREES, radius=4, **self.line_config)
        self.set_compass_to_draw_arc_(arc_l, adjust_angle=-PI, run_time=0.6)
        self.wait(0.1)
        self.draw_arc_by_compass(arc_l)
        self.wait(0.3)
        self.set_compass_to_draw_arc_(arc_r, adjust_angle=PI, run_time=0.6)
        self.wait(0.1)
        self.draw_arc_by_compass(arc_r)
        self.wait(0.1)
        self.put_aside_compass(DR * 0.6)
        self.wait(0.6)
        p1, p2 = np.sqrt(7) * UP, np.sqrt(7) * DOWN
        self.set_ruler(p1, p2)
        self.emphasize_dot([p1,p2], run_time=0.25)
        self.wait(0.2)
        l = Line(p1, p2, **self.line_config).scale(1.25).set_color(PINK)
        self.draw_line_(l)
        self.wait(0.1)
        self.put_aside_ruler(LEFT * 0.7)
        center = Dot((p1+p2)/2, color=RED).set_height(0.15)
        angle_90 = Square(0.32, stroke_width=2.5, stroke_color=GREY_C).shift(UR * 0.16)
        self.bring_to_back(angle_90)
        self.add(center)
        self.play(WiggleOutThenIn(center), FadeIn(angle_90), run_time=0.64)

        self.wait(2)


class Tangent_circle(DrawingScene):

    CONFIG = {
        'compass_config':{
            'stroke_color': GREY_E,
            'fill_color': WHITE,
            'stroke_width': 2,
            'leg_length': 4.05,
            'leg_width': 0.12,
            'r': 0.2,
            'depth_test': True,
        },
        'add_ruler': True,
    }

    def construct(self):
        s = 0.7
        p0 = DOWN * 1.5
        c1 = Circle(arc_center=3*LEFT*s+p0, radius=1*s, stroke_width=5, stroke_color='#66CCFF')
        c2 = Circle(arc_center=3*RIGHT*s+p0, radius=(3*np.sqrt(3)-2)*s, stroke_width=5, stroke_color='#66CCFF')
        l = Line(LEFT * 3*s+p0, RIGHT * 3*s+p0, stroke_width=4, stroke_color=GREY_E)
        d1, d2 = Dot(3*LEFT*s+p0, color=GREY_C).set_height(0.2), Dot(3*RIGHT*s+p0, color=GREY_C).set_height(0.2)


        self.add(c1, c2, l, d1, d2)
        self.wait()
        self.set_compass_and_show_span(c1.get_start(), c1.get_start() + 2*RIGHT*s, show_span_time=[0.4, 0.25, 0.6, 0.3], text='r', reverse_label=True)
        self.set_compass(c1.get_center(), c1.get_start() + 2*RIGHT*s, run_time=0.4)
        arc_l = Arc(arc_center=c1.get_center(), radius=3*s, angle=75 * DEGREES, **self.line_config)
        self.wait(0.14)
        self.draw_arc_by_compass(arc_l, run_time=0.6)
        self.wait(0.25)
        self.set_compass_and_show_span(c2.get_center()+3*np.sqrt(3)*s*LEFT, c2.get_center()+(3*np.sqrt(3)-2)*s*LEFT, show_span_time=[0.3, 0.25, 0.6, 0.3], text='r', reverse_label=True)
        self.set_compass(c2.get_center()+3*np.sqrt(3)*s*LEFT, c2.get_center(), run_time=0.4)
        arc_r = Arc(arc_center=c2.get_center(), radius=3*np.sqrt(3)*s, start_angle=PI, angle=-36 * DEGREES, **self.line_config)
        self.cp.reverse_tip()
        self.wait(0.1)
        self.draw_arc_by_compass(arc_r, run_time=0.6)
        self.wait(0.2)
        self.cp.reverse_tip()
        self.set_compass(c2.get_center()+3*np.sqrt(3)*s*LEFT, c2.get_center()+(3*np.sqrt(3)-2)*s*LEFT)
        self.wait(0.3)
        circle = Circle(arc_center=LEFT * 1.5 * s + UP * 1.5 * np.sqrt(3) * s + p0, radius=2*s, stroke_color=RED, stroke_width=4)
        self.set_compass_to_draw_arc(circle, run_time=0.4)
        self.wait(0.1)
        self.draw_arc_by_compass(circle, run_time=0.8, add_center=True)
        self.wait(0.08)
        self.put_aside_compass(UP * 0.6)

        self.wait(2)

class Equal_angle(DrawingScene):

    CONFIG = {
        'add_ruler': True,
    }

    def construct(self):

        p0 = LEFT * 4.5 + DOWN * 1.5
        p1, p2 = p0 + UR * 4/np.sqrt(2), p0 + 4 * complex_to_R3(np.exp(1j * 15 * DEGREES))
        p_0 = RIGHT* 0.5 + DOWN * 1.5
        p_1, p_2 = p_0 + 4 * complex_to_R3(np.exp(1j * 30 * DEGREES)), p_0 + 4 * RIGHT
        l1 = Line(p0, p1, stroke_width=5, stroke_color='#66CCFF')
        l2 = Line(p0, p2, stroke_width=5, stroke_color='#66CCFF')
        d0 = Dot(p0, color=GREY_C).set_height(0.18)

        l_1 = Line(p_0, p_1, stroke_width=4, stroke_color=RED)
        l_2 = Line(p_0, p_2, stroke_width=5, stroke_color=GREY_E)
        d_0 = Dot(p_0, color=GREY_E).set_height(0.1)

        self.add(l1, l2, d0, d_0,l_2)
        self.wait()
        arc_l = Arc(arc_center=p0, radius=2.5, angle=PI/3, **self.line_config)
        arc_r = Arc(arc_center=p_0, radius=2.5, angle=PI/3, start_angle=-PI/12, **self.line_config)
        self.set_compass_to_draw_arc(arc_l, run_time=0.6)
        self.wait(0.2)
        self.draw_arc_by_compass(arc_l, run_time=0.64)
        self.wait(0.3)
        self.set_compass_to_draw_arc(arc_r, run_time=0.5)
        self.wait(0.2)
        self.draw_arc_by_compass(arc_r, run_time=0.64)
        self.wait(0.3)
        p3, p4 = p0+2.5*complex_to_R3(np.exp(1j*15*DEGREES)), p0+2.5*complex_to_R3(np.exp(1j*45*DEGREES))
        p_3, p_4 = p_0+2.5*complex_to_R3(np.exp(1j*30*DEGREES)), p_0+2.5*RIGHT
        self.set_compass(p4, p3, run_time=0.8, emphasize_dot=True)
        self.wait(0.2)
        self.set_compass_(p_4, p_3, run_time=0.5, adjust_angle=PI)
        self.wait(0.2)
        arc = Arc(arc_center=p_4, start_angle=85 * DEGREES, angle=40*DEGREES, radius=get_norm(p_3 - p_4), **self.line_config)
        self.set_compass_to_draw_arc_(arc, run_time=0.25, adjust_angle=PI)
        self.draw_arc_by_compass(arc, run_time=0.45)
        self.wait(0.15)
        self.put_aside_compass(DOWN * 0.6)
        self.wait(0.2)
        self.set_ruler(p_0, p_3, run_time=0.6)
        self.wait(0.12)
        self.draw_line_(l_1, run_time=0.6)
        self.bring_to_front(d_0)
        self.wait(0.12)
        self.put_aside_ruler(DR * 0.6)
        self.wait(0.2)

        a1 = Arc(arc_center=p0, radius=0.5, start_angle=PI/12, angle=PI/6, stroke_color=PINK, stroke_width=8, stroke_opacity=0.8)
        a2 = Arc(arc_center=p_0, radius=0.5, start_angle=0, angle=PI/6, stroke_color=PINK, stroke_width=8, stroke_opacity=0.8)
        self.play(ShowCreation(a1), ShowCreation(a2), run_time=0.75)

        self.wait(2)


class test_ruler_compass(DrawingScene):
    def construct(self):
        # frame = self.camera.frame
        # frame.move_to(np.array([10,0,0])),
        # self.play(
            
        #     frame.animate.set_width(40), # 旋转缩放相机帧
            
        #     run_time=0
        # )
        s = 0.5
        self.setup()
        dl = np.array([1,1,0])
        dr = np.array([-1,-1,0])
        d13 = np.array([0,-2,0])
        self.set_ruler(dl, dr)
        self.cp.move_to(UP * 10)
        self.emphasize_dot([dl, dr], run_time=0.2)
        # l = Line(dl + LEFT * 4.5, dr + RIGHT *4.5, **self.line_config)
        self.wait(0.5)
        l = self.draw_line(dl , dr , run_time=1.25)
        self.put_aside_ruler(DOWN * 4)
        self.wait(0.1)
        dm = (dl+dr)/2
        # self.set_compass(d13, dm, emphasize_dot=True, run_time=1.5)
        self.wait(0.2)
        
        # a_13_l = Arc(arc_center=RIGHT * 2, radius=3, start_angle=2 * PI/3, angle=2*PI/3, **self.line_config)
        # self.cp.move_to(ORIGIN)
        # self.set_compass_to_draw_arc_(a_13_l, adjust_angle=PI,  emphasize_dot=True,run_time=1.4)
        # self.draw_arc_by_compass(a_13_l,run_time=4)


        # arc_1 = Arc(arc_center=LEFT * 2, radius=3, start_angle=-PI/3, angle=2*PI/3, **self.line_config)
        arc_2 = Arc(arc_center=RIGHT * 2, radius=3, start_angle=2 * PI/3, angle=2*PI/3, **self.line_config)

        self.play(self.cp.move_to, ORIGIN)
        self.wait(0.2)
        # self.set_compass_to_draw_arc(arc_1, emphasize_dot=True)
        # self.draw_arc_by_compass(arc_1)
        self.wait(0.1)
        self.set_compass_to_draw_arc_(arc_2, adjust_angle=-PI, emphasize_dot=True,run_time = 2.4)
        self.draw_arc_by_compass(arc_2)
        self.wait(0.2)

        arc_1 = Arc(arc_center=LEFT * 2, radius=3, start_angle=-PI/3, angle=2*PI/3, **self.line_config)
        self.set_compass_to_draw_arc(arc_1, emphasize_dot=True)
        self.draw_arc_by_compass(arc_1)
        self.wait(0.2)

        self.set_compass_to_draw_arc_(arc_2,adjust_angle=PI, emphasize_dot=True,run_time = 2.4)
        self.draw_arc_by_compass(arc_2)
        self.wait(0.2)

        arc_3 = Arc(arc_center=RIGHT * 1.5, radius=2, start_angle=1.3 * PI/3, angle=1.5*PI/3, **self.line_config)
        # self.set_compass_to_draw_arc_(arc_3,adjust_angle=PI, emphasize_dot=True,run_time = 2.4)
        self.set_compass_to_draw_arc_(arc_3,adjust_angle= PI, emphasize_dot=True,run_time = 12.4)
        self.draw_arc_by_compass(arc_3)
        self.wait(0.2)

        # arc_3 = Arc(arc_center=LEFT * 1.5, radius=2, start_angle=0.5 * PI, angle=0.5*PI/3, **self.line_config)
        arc_3 = Circle(arc_center=LEFT * 1.5,radius=2.6)
        # self.set_compass_to_draw_arc_(arc_3,adjust_angle=PI, emphasize_dot=True,run_time = 2.4)
        self.set_compass_to_draw_arc_(arc_3, adjust_angle=  PI,emphasize_dot=True,run_time = 12.4)
        self.draw_arc_by_compass(arc_3)
        self.wait(0.2)




class Draw_YY(DrawingScene):
    Scene_config = {
        'start_x':4,
        'start_y':-1.2,
        'start_z':0,
        'default_length': 400,
        'default_width': 30
    }

    
    UNIT_lEN = 2

    def __init__(self,  **kwargs):
        DrawingScene.__init__(self, **kwargs)
        frame = self.camera.frame
        frame.move_to(np.array([self.Scene_config['start_x'],\
            self.Scene_config['start_y'],\
            self.Scene_config['start_z']])),
        self.play(
            frame.animate.set_width(self.Scene_config['default_width']), # 旋转缩放相机帧
            run_time=0
        )
        self.init_yy_logo()
        self.init_yy_logo_outline(5)

    @staticmethod
    def eclipse(t):
        x = sqrt(7) * np.cos(t) * Draw_YY.UNIT_lEN + Draw_YY.UNIT_lEN * 2
        y =  sqrt(6) * np.sin(t) * Draw_YY.UNIT_lEN
        return np.array([x, y, 0.0])
    
    def init_supprt_lines(self):
        unit = self.UNIT_lEN
        
        support_line_color = '#92CB98'

        # text = Text("如何精确绘制 yonex logo？", gradient=('#4091c9','#92cb98'),font_size=120,font="Times New Roman").move_to(UP*3 + LEFT)
        # background_rect = BackgroundRectangle(text, fill_opacity=0.5, color="#feffff")
        # self.add(background_rect,text)
        # 将文本对象添加到场景中
        # self.play(Write(text))
        self.camera.frame.move_to(np.array([3.6,-2,0])),
        axes = NumberPlane()
        print(LEFT)
        e = Ellipse(width=2*sqrt(7)*unit,height=2*sqrt(6)*unit,stroke_color = support_line_color)
        e.move_to(RIGHT*2*unit)
        

       

        d0_1 = LEFT * 3.6 * unit + DOWN * sqrt(3) * unit
        d0_2 = RIGHT  * 3.3 * unit  + DOWN * sqrt(3) * unit
       
        l = Line(start = d0_1 , end = d0_2).set_color(support_line_color)
       

       

        circle_down_left_center = LEFT * unit + DOWN * sqrt(3) * unit
        arc_circle_l = Circle(arc_center=circle_down_left_center, radius=2 * unit, **self.line_config).set_color(support_line_color)
       
        arc_circle_m = Circle(arc_center=RIGHT  * unit  + DOWN * sqrt(3) * unit, radius=2 * unit, **self.line_config).set_color(support_line_color)

        arc_circle_r = Circle(arc_center=RIGHT  * 3 * unit  + DOWN * sqrt(3) * unit, radius=2 * unit, **self.line_config).set_color(support_line_color)

      

        d1 = np.array([0,0,0])
        d2 = np.array([4 * unit,0,0])

        l_hori = Line(start = d1 , end = d2 , ).set_color(support_line_color)

        l3_d0 = RIGHT * 2 * unit
        l3_d1 = RIGHT * 1 * unit + DOWN * sqrt(3) * unit

        l4_d0 = RIGHT * 4 * unit
        l4_d1 = RIGHT * 3 * unit + DOWN * sqrt(3) * unit

        l3 = Line(start = l3_d0 , end = l3_d1 ).set_color(support_line_color)
        l4 = Line(start = l4_d0 , end = l4_d1).set_color(support_line_color)

        

        circle_up_left_center = RIGHT * unit 
        circle_up_left_radius = np.linalg.norm(circle_up_left_center - circle_down_left_center)
 
        arc_circle_up_left = Circle(start_angle =  np.arctan(sqrt(3)/2) - PI,arc_center=circle_up_left_center,\
                                    radius=circle_up_left_radius, \
                                        **self.line_config).set_color(support_line_color)

        dot_left_up_circle_center = Dot(color = '#feffff').move_to(circle_up_left_center)

        circle_up_right_center = RIGHT * 3 * unit 

        
        arc_circle_up_right = Circle(arc_center=circle_up_right_center,\
                                    radius=circle_up_left_radius, start_angle = np.arctan(sqrt(3)/2) - PI,\
                                        ).set_color(support_line_color)
        # self.emphasize_dot(circle_up_right_center)
        dot_right_up_circle_center = Dot(color = '#feffff').move_to(circle_up_right_center)    
       
        eclipse_path = ParametricCurve(
            t_func=self.eclipse,
            t_range=[PI,  3/2 * PI,1e-4],
            color=GREEN,
        )
        perpen_0 = ORIGIN
        perpen_1 = ORIGIN + 2*unit*RIGHT
        perpen_2 = ORIGIN + 4*unit*RIGHT

        support_arc_1 = Arc(start_angle=2/3 * PI + 0.05*PI,angle=0.1 *PI,radius = 1.3*unit,arc_center= perpen_1,**self.line_config).set_color(support_line_color)
        support_arc_0 = Arc(start_angle=1/3 * PI - 0.15*PI,angle=0.1 *PI,radius = 1.3*unit,arc_center= perpen_0,**self.line_config).set_color(support_line_color)
        support_arc_2 = Arc(start_angle=2/3 * PI + 0.05*PI,angle=0.1 *PI,radius = 1.3*unit,arc_center= perpen_2,**self.line_config).set_color(support_line_color)
        support_arc_3 = Arc(start_angle=1/3 * PI - 0.15*PI,angle=0.1 *PI,radius = 1.3*unit,arc_center= perpen_1,**self.line_config).set_color(support_line_color)
        
        


        start_x_cor = 0.129
        # r_logo_circle = 1.4374718483411222 / 2 * unit
        r_logo_circle = 1.437 / 2 * unit
        moving_circle = Circle(radius = r_logo_circle,color=BLACK)
        moving_circle.move_to(axes.i2gp(start_x_cor * unit, eclipse_path)).set_color(support_line_color)
        moving_circle_center_dot = Dot(color = '#259630')
        moving_circle_center_dot.move_to(axes.i2gp(start_x_cor * unit, eclipse_path))
        
        determine_right_center_arc = Arc(arc_center = moving_circle.get_center(),\
                                        start_angle= -0.02 * PI,angle = 0.04*PI,\
                                        radius = unit*2,\
                                        emphasize_dot=False,color = BLACK).set_color(support_line_color)
       

       
        logo_circle_right = Circle(start_angle =  0 ,arc_center=moving_circle.get_center() + 2 * unit * RIGHT,\
                                    radius=r_logo_circle, \
                                        ).set_color(support_line_color)
        
       
        self._left_triangle_path.set_fill('#feffff',opacity=0.7)
        self._right_triangle_path.set_fill('#feffff',opacity=0.7)
        self._left_circle.set_fill('#feffff',opacity=0.7)
        self._right_circle.set_fill('#feffff',opacity=0.7)
        self.init_yy_logo_outline(stroke_width = 10)
   
        f_ani = ShowCreationThenFadeOut
        # f_ani = ShowPassingFlash

        
        self.play(
            

            
            f_ani(e),

            f_ani(l),
            f_ani(l_hori),
            f_ani(l3),
            f_ani(l4),

            f_ani(support_arc_0),
            f_ani(support_arc_1),
            f_ani(support_arc_2),
            f_ani(support_arc_3),

            f_ani(determine_right_center_arc),
            
            f_ani(arc_circle_l),
            f_ani(arc_circle_m),
            f_ani(arc_circle_r),

            f_ani(arc_circle_up_left),
            f_ani(arc_circle_up_right),

            f_ani(moving_circle),
            f_ani(logo_circle_right),
            
            
            run_time = 0.6,
            
        )

        f_ani2 = FadeOut
        self.play(f_ani2(self._left_triangle_path),
            f_ani2(self._right_triangle_path),
            f_ani2(self._left_circle),
            f_ani2(self._right_circle),

            # remove logo outlines
            f_ani2(self._outline_left_triangle_path),
            f_ani2(self._outline_right_triangle_path),
            f_ani2(self._outline_left_circle),
            f_ani2(self._outline_right_circle),
            run_time = 0.6)


       

        self._left_triangle_path.set_fill('#FEFFFF',opacity=1)
        self._right_triangle_path.set_fill('#FEFFFF',opacity=1)
        self._left_circle.set_fill('#FEFFFF',opacity=1)
        self._right_circle.set_fill('#FEFFFF',opacity=1)

        pass


    
    def init_yy_logo(self):
        unit = self.UNIT_lEN
        self._left_triangle_path = VMobject()
        start_point = np.array([0,0,0])
        path_point = start_point
        self._left_triangle_path.start_new_path(np.array([0,0,0]))
        self._left_triangle_path.add_line_to(np.array([2 * unit,0,0]))
        self._left_triangle_path.add_line_to(np.array([unit,-unit*sqrt(3),0]))

        arc = ArcBetweenPoints(np.array([0,0,0]),np.array([unit,-unit*(sqrt(3)),0]),angle = -PI/3)
        # path2.add_line_to(arc.get_points()[-1])
        self._left_triangle_path.add_subpath(arc.get_points()[::-1])
        # path2.add_line_to(start_point)
        
        


        self._right_triangle_path = VMobject()
        start_point = np.array([2 * unit,0,0]) 
        path_point = start_point
        self._right_triangle_path.start_new_path(np.array([0,0,0])+ start_point)
        self._right_triangle_path.add_line_to(np.array([2*unit,0,0])+start_point)
        self._right_triangle_path.add_line_to(np.array([unit,-unit*sqrt(3),0])+start_point)

        arc2 = ArcBetweenPoints(np.array([0,0,0])+start_point,np.array([unit,-unit*sqrt(3),0])+start_point,angle = -PI/3)
        self._right_triangle_path.add_subpath(arc2.get_points()[::-1])

        self._left_triangle_path.set_fill('#FEFFFF',opacity=1)
        self._right_triangle_path.set_fill('#FEFFFF',opacity=1)

        # radius = 1.4374718483411222 / 2 * unit
        radius = 1.437 / 2 * unit
        
        self._left_circle = Circle(arc_center = DOWN * unit * sqrt(3) + 0.129 * unit * RIGHT,radius=radius,  stroke_color='#FEFFFF',stroke_width = 0)
        self._left_circle.set_fill('#FEFFFF',opacity=1)
        
        self._right_circle = Circle(start_angle =  0 ,arc_center=self._left_circle.get_center() + 2 * unit * RIGHT,\
                                    radius=radius, \
                                    stroke_color='#FEFFFF',stroke_width =0)
        self._right_circle.set_fill('#FEFFFF',opacity=1)

    def init_yy_logo_outline(self,stroke_width = 5):
        unit = self.UNIT_lEN
        self._outline_left_triangle_path = VMobject(stroke_width = stroke_width)
        start_point = np.array([0,0,0])
        
        self._outline_left_triangle_path.start_new_path(np.array([0,0,0]))
        self._outline_left_triangle_path.add_line_to(np.array([2 * unit,0,0]))
        self._outline_left_triangle_path.add_line_to(np.array([unit,-unit*sqrt(3),0]))

        arc = ArcBetweenPoints(np.array([0,0,0]),np.array([unit,-unit*(sqrt(3)),0]),angle = -PI/3)
        # path2.add_line_to(arc.get_points()[-1])
        self._outline_left_triangle_path.add_subpath(arc.get_points()[::-1])
        # path2.add_line_to(start_point)
        
        # self.play(ShowCreation(path2))
        # self.play(ShowCreation(arc))



        self._outline_right_triangle_path = VMobject(stroke_width = stroke_width)
        start_point = np.array([2 * unit,0,0]) 
       
        self._outline_right_triangle_path.start_new_path(np.array([0,0,0])+ start_point)
        self._outline_right_triangle_path.add_line_to(np.array([2*unit,0,0])+start_point)
        self._outline_right_triangle_path.add_line_to(np.array([unit,-unit*sqrt(3),0])+start_point)

        arc2 = ArcBetweenPoints(np.array([0,0,0])+start_point,np.array([unit,-unit*sqrt(3),0])+start_point,angle = -PI/3)
        self._outline_right_triangle_path.add_subpath(arc2.get_points()[::-1])
        # self.play(ShowCreation(path3))

        

        # radius = 1.4374718483411222 / 2 * unit
        radius = 1.437 / 2 * unit
        self._outline_left_circle = Circle(arc_center = DOWN * unit * sqrt(3) + 0.129 * unit * RIGHT,radius=radius,  stroke_color='#FEFFFF',stroke_width = stroke_width)
        
        self._outline_right_circle = Circle(start_angle =  0 ,arc_center=self._outline_left_circle.get_center() + 2 * unit * RIGHT,\
                                    radius=radius, \
                                    stroke_color='#FEFFFF',stroke_width = stroke_width)
        

    def draw_logo_outline(self,run_time = 1):
    
        self.play(ShowCreation(self._outline_left_triangle_path),
        # DrawBorderThenFill(right_triangle_path)
        ShowCreation(self._outline_right_triangle_path),
        ShowCreation(self._outline_left_circle),
        ShowCreation(self._outline_right_circle),
        run_time = run_time
        )

    def rm_logo_outline(self,run_time = 1):
        self.play(FadeOut(self._outline_left_triangle_path),
        # DrawBorderThenFill(right_triangle_path)
        FadeOut(self._outline_right_triangle_path),
        FadeOut(self._outline_left_circle),
        FadeOut(self._outline_right_circle),
        run_time = run_time
        )

    def rm_filled_logo(self,run_time = 1):
        self.play(FadeOut(self._left_triangle_path),
        # DrawBorderThenFill(right_triangle_path)
        FadeOut(self._right_triangle_path),
        FadeOut(self._left_circle),
        FadeOut(self._right_circle),
        run_time = run_time

        )

    def fill_logo(self,run_time = 1):
        self.play(
            FadeIn(self._left_triangle_path),
            FadeIn(self._right_triangle_path),
            FadeIn(self._left_circle),
            FadeIn(self._right_circle),
            run_time = run_time
        )

    def construct(self):
        unit = self.UNIT_lEN
        self.init_yy_logo()
        self.init_yy_logo_outline(stroke_width = 10)

        
        # self.draw_logo_outline(run_time=2)
        # self.fill_logo(run_time=2)
        # self.wait()
        # self.rm_logo_outline(run_time=0.01)
        # self.rm_filled_logo()
        
        # self.wait(1)

        

        self.init_supprt_lines()

        axes = NumberPlane()
        print(LEFT)
        e = Ellipse(width=2*sqrt(7)*unit,height=2*sqrt(6)*unit,stroke_color = BLACK)
        e.move_to(RIGHT*2*unit)
        

        self.put_aside_compass(UP * 2 * self.UNIT_lEN)

        d0_1 = LEFT * 3.6 * unit + DOWN * sqrt(3) * unit
        d0_2 = RIGHT  * 3.3 * unit  + DOWN * sqrt(3) * unit
        self.set_ruler(d0_1, d0_2,run_time=0.5)
        #拉伸镜头
        self.play(
            self.camera.frame.animate.move_to(np.array([1.8,-2,0])),
            run_time = 0.2 
        )
        self.play(
            self.camera.frame.animate.set_width(self.Scene_config['default_width']*0.8), # 旋转缩放相机帧
            run_time = 0.2 
        )
        l = self.draw_line(d0_1 , d0_2 , run_time=1.25,emphasize=False,dashed=True)
        self.put_aside_ruler(DOWN * 4)

        self.cp.move_to(ORIGIN)

        circle_down_left_center = LEFT * unit + DOWN * sqrt(3) * unit
        arc_circle_l = Circle(arc_center=circle_down_left_center, radius=2 * unit, **self.line_config)

        self.set_compass_to_draw_arc_(arc_circle_l, adjust_angle=-PI, emphasize_dot=True,run_time = 1.2)
        self.draw_arc_by_compass(arc_circle_l)
        self.wait(0.15)

        arc_circle_m = Circle(arc_center=RIGHT  * unit  + DOWN * sqrt(3) * unit, radius=2 * unit, **self.line_config)
        self.set_compass_to_draw_arc_(arc_circle_m, adjust_angle= - PI, emphasize_dot=True,run_time = 0.9)
        self.draw_arc_by_compass(arc_circle_m)
        self.wait(0.12)
        self.play(
            self.camera.frame.animate.move_to(np.array([2.4,-2,0])),
            run_time = 0.2
        )
        
        arc_circle_r = Circle(arc_center=RIGHT  * 3 * unit  + DOWN * sqrt(3) * unit, radius=2 * unit, **self.line_config)
        self.set_compass_to_draw_arc_(arc_circle_r, adjust_angle= - PI, emphasize_dot=True,run_time = 0.6)
        self.draw_arc_by_compass(arc_circle_r)
        self.wait(0.1)

        #还原镜头
        self.play(
            self.camera.frame.animate.move_to(np.array([self.Scene_config['start_x'],\
                                                        self.Scene_config['start_y'],\
                                                        self.Scene_config['start_z']])),
            run_time = 0.2
        )
        self.play(
            self.camera.frame.animate.set_width(self.Scene_config['default_width']), # 旋转缩放相机帧
            run_time = 0.2 
        )

        self.set_span(0.3)
        self.put_aside_compass(RIGHT * 1,run_time=0.5)
        self.wait(0.15)

        d1 = np.array([0,0,0])
        d2 = np.array([4 * unit,0,0])
        self.set_ruler(d1, d2)

        self.play(
            self.camera.frame.animate.move_to(np.array([self.Scene_config['start_x'] + 1,\
                                                        self.Scene_config['start_y']+ 0.3,\
                                                        self.Scene_config['start_z']])),
            run_time = 0.2
        )
        self.play(
            self.camera.frame.animate.set_width(self.Scene_config['default_width']* 0.9), # 旋转缩放相机帧
            run_time = 0.2 
        )

        self.emphasize_dot([d1, d2])
        self.wait(0.1)
        l_hori = self.draw_line(d1 , d2 , run_time=0.5)
        # self.put_aside_ruler(DOWN * 4)
        self.wait(0.1)

        l3_d0 = RIGHT * 2 * unit
        l3_d1 = RIGHT * 1 * unit + DOWN * sqrt(3) * unit

        l4_d0 = RIGHT * 4 * unit
        l4_d1 = RIGHT * 3 * unit + DOWN * sqrt(3) * unit

        self.play(
            self.camera.frame.animate.move_to(np.array([self.Scene_config['start_x'] + 1,\
                                                        self.Scene_config['start_y']+ 0.1,\
                                                        self.Scene_config['start_z']])),
            run_time = 0.2
        )
        

        self.set_ruler(l3_d0, l3_d1)
        
        l3 = self.draw_line(l3_d0 , l3_d1 , run_time=1)

        self.wait(0.12)
        self.play(
            self.camera.frame.animate.move_to(np.array([self.Scene_config['start_x'] + 1.5,\
                                                        self.Scene_config['start_y']+ 0.1,\
                                                        self.Scene_config['start_z']])),
            run_time = 0.2
        )

        self.set_ruler(l4_d0, l4_d1,run_time=0.5)
        l4 = self.draw_line(l4_d0 , l4_d1 , run_time=0.6)

        self.wait(0.15)

        self.play(
            self.camera.frame.animate.move_to(np.array([self.Scene_config['start_x'] ,\
                                                        self.Scene_config['start_y'],\
                                                        self.Scene_config['start_z']])),
            run_time = 0.2
        )
        self.play(
            self.camera.frame.animate.set_width(self.Scene_config['default_width']), # 旋转缩放相机帧
            run_time = 0.2 
        )

        self.put_aside_ruler(DOWN * 4)

        self.wait(0.15)

        self.play(
            self.camera.frame.animate.move_to(np.array([self.Scene_config['start_x'] + 0.3 ,\
                                                        self.Scene_config['start_y'] + 0.1,\
                                                        self.Scene_config['start_z']])),
            run_time = 0.2
        )
        self.play(
            self.camera.frame.animate.set_width(self.Scene_config['default_width']*0.76), # 旋转缩放相机帧
            run_time = 0.2 
        )

        #中垂线
        perpen_0 = ORIGIN
        perpen_1 = ORIGIN + 2*unit*RIGHT
        perpen_2 = ORIGIN + 4*unit*RIGHT

        support_arc_1 = Arc(start_angle=2/3 * PI + 0.05*PI,angle=0.1 *PI,radius = 1.3*unit,arc_center= perpen_1,**self.line_config)
        self.set_compass_to_draw_arc_(support_arc_1, start = None,adjust_angle= - PI, emphasize_dot=True,run_time = 1.2)
        self.draw_arc_by_compass(support_arc_1,run_time=0.6)

        self.wait(0.1)

        support_arc_0 = Arc(start_angle=1/3 * PI - 0.15*PI,angle=0.1 *PI,radius = 1.3*unit,arc_center= perpen_0,**self.line_config)
        self.set_compass_to_draw_arc_(support_arc_0, start = None, adjust_angle=  PI,emphasize_dot=True,run_time = 1.2)
        self.draw_arc_by_compass(support_arc_0,run_time=0.6)

        self.wait(0.1)

        support_arc_2 = Arc(start_angle=2/3 * PI + 0.05*PI,angle=0.1 *PI,radius = 1.3*unit,arc_center= perpen_2,**self.line_config)
        self.set_compass_to_draw_arc_(support_arc_2, start = None,adjust_angle= - PI, emphasize_dot=True,run_time = 1.2)
        self.draw_arc_by_compass(support_arc_2,run_time=0.6)
        self.wait(0.1)
        support_arc_3 = Arc(start_angle=1/3 * PI - 0.15*PI,angle=0.1 *PI,radius = 1.3*unit,arc_center= perpen_1,**self.line_config)
        self.set_compass_to_draw_arc_(support_arc_3, start = None,adjust_angle=  PI, emphasize_dot=True,run_time = 1.2)
        self.draw_arc_by_compass(support_arc_3,run_time=0.6)
        self.wait(0.1)
        self.put_aside_compass(RIGHT* 0.5* unit)

        intersection_l = np.array([unit ,0.8305 * unit ,0])
        intersection_r = np.array([3*unit ,0.8305 * unit ,0])
        p =  np.array([unit,-unit*sqrt(3),0])
        
        

        

        circle_up_left_center = RIGHT * unit 
        dot_left_up_circle_center = Dot(color = '#feffff').move_to(circle_up_left_center)
        circle_up_right_center = RIGHT * 3 * unit 
        dot_right_up_circle_center = Dot(color = '#feffff').move_to(circle_up_right_center)
        circle_up_left_radius = np.linalg.norm(circle_up_left_center - circle_down_left_center)

        self.set_ruler(intersection_l,p)
        self.wait(0.2)
        self.emphasize_dot(intersection_l)
        self.wait(0.1)
        self.emphasize_dot(p)
        self.wait(0.1)
        self.emphasize_dot(circle_up_left_center)
        
        self.play(FadeIn(dot_left_up_circle_center),run_time=0.2)
        self.wait(0.1)
        

        self.set_ruler(intersection_r,np.array([3*unit,-unit*sqrt(3),0]))
        self.wait(0.2)
        self.emphasize_dot(intersection_r)
        self.wait(0.1)
        self.emphasize_dot(np.array([3*unit,-unit*sqrt(3),0]))
        self.wait(0.1)
        self.emphasize_dot(circle_up_right_center)
        self.wait(0.1)
        
        self.play(FadeIn(dot_right_up_circle_center),run_time=0.1)
        self.wait(0.1)

        self.play(
            self.camera.frame.animate.move_to(np.array([self.Scene_config['start_x']  ,\
                                                        self.Scene_config['start_y'] ,\
                                                        self.Scene_config['start_z']])),
            run_time = 0.2
        )
        self.play(
            self.camera.frame.animate.set_width(self.Scene_config['default_width']*0.9), # 旋转缩放相机帧
            run_time = 0.2 
        )

        self.put_aside_ruler(RIGHT * unit, run_time=1)

        

        arc_circle_up_left = Circle(start_angle =  np.arctan(sqrt(3)/2) - PI,arc_center=circle_up_left_center,\
                                    radius=circle_up_left_radius, \
                                        **self.line_config)

        
        self.set_compass_to_draw_arc_(arc_circle_up_left, start = None,adjust_angle= - PI, emphasize_dot=True,run_time = 2.4)
        self.draw_arc_by_compass(arc_circle_up_left)
        self.play(
            FadeOut(dot_left_up_circle_center),
            run_time=0.2
        )
        self.wait(0.2)

        
        circle_up_right_edge = RIGHT * 1 * unit + DOWN * sqrt(3) * unit

        
        arc_circle_up_right = Circle(arc_center=circle_up_right_center,\
                                    radius=circle_up_left_radius, start_angle = np.arctan(sqrt(3)/2) - PI,\
                                        **self.line_config)
        # 
        self.set_compass_to_draw_arc_(arc_circle_up_right, adjust_angle= - PI, emphasize_dot=True,run_time = 1.4)
        self.draw_arc_by_compass(arc_circle_up_right)
        self.play(
            FadeOut(dot_right_up_circle_center),
            run_time=0.2
        )
        self.wait(0.1)
        
        self.put_aside_compass(RIGHT * 2 * unit)        
       
        eclipse_path = ParametricCurve(
            t_func=self.eclipse,
            t_range=[PI,  3/2 * PI,1e-4],
            color=GREEN,
        )

        start_x_cor = 2
        moving_circle = Circle(radius = 2.02,color=BLACK)
        moving_circle.move_to(axes.i2gp(start_x_cor * unit, eclipse_path))
        moving_circle_center_dot = Dot(color = '#259630')
        moving_circle_center_dot.move_to(axes.i2gp(start_x_cor * unit, eclipse_path))
        x_tracker = ValueTracker(start_x_cor * unit)

        self.play(
            self.camera.frame.animate.move_to(np.array([self.Scene_config['start_x'] + 0.3 ,\
                                                        self.Scene_config['start_y'] -1,\
                                                        self.Scene_config['start_z']])),
            run_time = 0.2
        )
        self.play(
            self.camera.frame.animate.set_width(self.Scene_config['default_width']*0.6), # 旋转缩放相机帧
            run_time = 0.2 
        )
        

        self.play(FocusOn(moving_circle_center_dot))
        self.play(ShowCreation(moving_circle_center_dot),run_time=0.6)



        

        def func_get_r(x,path):
            # axes = Axes()
            
            circle_up_right_center = RIGHT * 3 * unit 
            p = axes.i2gp(x, path)
            # dis = np.linalg.norm(p - circle_up_right_center,np.float128)
            dis = (Decimal(p[0])-Decimal(circle_up_right_center[0])) * (Decimal(p[0])-Decimal(circle_up_right_center[0])) +\
                  (Decimal(p[1])-Decimal(circle_up_right_center[1])) * (Decimal(p[1])-Decimal(circle_up_right_center[1])) 
            dis = dis.sqrt()
            return float(dis - Decimal(7).sqrt() * Decimal(unit))

        # 创建一个移动对象，并将点对象与路径对象关联起来
        move_along_path = MoveAlongPath(moving_circle_center_dot, eclipse_path)
        
        moving_circle.add_updater(lambda m: m.become(Circle(arc_center = axes.i2gp(x_tracker.get_value(), eclipse_path),radius =  func_get_r(x_tracker.get_value(),eclipse_path),color = BLACK)))
        
        moving_circle_center_dot.add_updater(lambda m: m.become(Dot(color = '#259630').move_to(axes.i2gp(x_tracker.get_value(), eclipse_path))))
        
        
        # def modify_circle(cir_obj):
            
        #     print(moving_circle_center_dot.get_center())
        #     cir_obj.radius = func_get_r(moving_circle_center_dot.get_center()[0],eclipse_path)
        #     cir_obj.move_to(moving_circle_center_dot.get_center())
        #     print(cir_obj.radius)
        
        # moving_circle.add_updater(modify_circle)
        self.play(DrawBorderThenFill(moving_circle),run_time=0.01)

        circle_center_tracer = TracedPath(moving_circle.get_center,stroke_color = '#259630',stroke_width=5)
        

        self.play(x_tracker.animate.set_value(-0.62 * unit  ), 
               
                ShowCreation(circle_center_tracer),
                  run_time=2)
        self.play(x_tracker.animate.set_value(2 * unit ), run_time=1)
        self.play(x_tracker.animate.set_value(1.5 * unit ), run_time=0.45)




        
        self.play(
            self.camera.frame.animate.move_to(np.array([self.Scene_config['start_x'] ,\
                                                        self.Scene_config['start_y'],\
                                                        self.Scene_config['start_z']])),
            run_time = 0.2
        )
        self.play(
            self.camera.frame.animate.set_width(self.Scene_config['default_width']*0.9), # 旋转缩放相机帧
            run_time = 0.2 
        )
        self.play(
            FadeIn(e),
            run_time=0.9
        )
        self.play(
            Uncreate(circle_center_tracer),
            run_time=0.1
        )
        
        
        self.play(x_tracker.animate.set_value(-0.62 * unit  ),
                
                  run_time=1)
        self.play(x_tracker.animate.set_value(0.3 * unit ), run_time=1)

        self.play(x_tracker.animate.set_value(0.129 * unit ), run_time=1)
        self.emphasize_dot(moving_circle.get_center(),size = 1.2,run_time=0.5)
        self.wait(0.5)
        # r_logo_circle = 1.4374718483411222 / 2 * unit
        r_logo_circle = 1.437 / 2 * unit

        #  取一个unit length的长度
        self.set_compass(ORIGIN,ORIGIN+RIGHT*2*unit)

        line_ = Line(start=ORIGIN, end=ORIGIN+RIGHT*2*unit,**self.line_config)
        brace = Brace(line_,**self.brace_config)
        
        self.play(ShowCreationThenFadeOut(brace))
        self.wait(0.2)

        self.set_compass(moving_circle.get_center(),moving_circle.get_center()+RIGHT*2*unit)

        determine_right_center_arc = Arc(arc_center = moving_circle.get_center(),\
                                        start_angle= -0.02 * PI,angle = 0.04*PI,\
                                        radius = unit*2,\
                                        emphasize_dot=False,color = BLACK)
        self.set_compass_to_draw_arc_(determine_right_center_arc, start = None,adjust_angle= - PI, emphasize_dot=True,run_time = 1.4)
        self.draw_arc_by_compass(determine_right_center_arc)
        right_logo_circle_Dot = Dot(moving_circle.get_center()+RIGHT*2*unit,**self.dot_config).set_color('#259630')
        self.play(FadeIn(right_logo_circle_Dot))


        self.set_compass(moving_circle.get_center(),moving_circle.get_center()+RIGHT*r_logo_circle)
        self.wait()
        logo_circle_right = Circle(start_angle =  0 ,arc_center=moving_circle.get_center() + 2 * unit * RIGHT,\
                                    radius=r_logo_circle, \
                                        **self.line_config)
        
        self.set_compass_to_draw_arc_(logo_circle_right, start = None,adjust_angle= - PI, emphasize_dot=True,run_time = 1.4)
        self.draw_arc_by_compass(logo_circle_right)
        self.wait(0.5)
        self.put_aside_compass(RIGHT * 3)
        self.wait()

        self.init_yy_logo_outline(stroke_width=20)
        self.draw_logo_outline(3)
        self.play(
            # display filled logo 
            FadeIn(self._left_triangle_path),
            FadeIn(self._right_triangle_path),
            FadeIn(self._left_circle),
            FadeIn(self._right_circle),

            # remove logo outlines
            FadeOut(self._outline_left_triangle_path),
            FadeOut(self._outline_right_triangle_path),
            FadeOut(self._outline_left_circle),
            FadeOut(self._outline_right_circle),

            # remove support lines
            FadeOut(e),
            FadeOut(support_arc_1),
            FadeOut(support_arc_0),
            FadeOut(support_arc_2),
            FadeOut(support_arc_3),
            FadeOut(determine_right_center_arc),
            FadeOut(right_logo_circle_Dot),


            FadeOut(l),
            FadeOut(l_hori),
            FadeOut(l3),
            FadeOut(l4),
            
            FadeOut(arc_circle_l),
            FadeOut(arc_circle_m),
            FadeOut(arc_circle_r),

            FadeOut(arc_circle_up_left),
            FadeOut(arc_circle_up_right),

            FadeOut(moving_circle),
            FadeOut(logo_circle_right),

            Uncreate(moving_circle_center_dot),
            # Uncreate(circle_center_tracer),

            # self.camera.frame.animate.set_width(15),
            self.camera.frame.animate.move_to(np.array([3.6,-2,0])),

            
            run_time = 3
        )
        self.camera.background_rgba = list(color_to_rgba('#2aa570', 1))
        self.wait(2)

        pass

class ValueTrackerExample(Scene):
    def construct(self):
        tracker = ValueTracker(0)
        label = Dot(radius=3).add_updater(lambda x : x.set_x(tracker.get_value()))
        label.add_updater(lambda x : x.set_width(tracker.get_value()+1))
        self.add(label)
        self.add(tracker)
        tracker.add_updater(lambda mobject, dt: mobject.increment_value(dt))
        self.wait(2)

class GraphExample(Scene):
    def construct(self):
        axes = Axes((-3, 10), (-1, 8))
        axes.add_coordinate_labels()

        # self.play(Write(axes, lag_ratio=0.01, run_time=1))


        parabola = axes.get_graph(lambda x: 0.25 * x**2)
        parabola.set_stroke(BLUE)
        self.play(
           
            ShowCreation(parabola)
        )
        self.wait()

        # You can use axes.input_to_graph_point, abbreviated
        # to axes.i2gp, to find a particular point on a graph
        dot = Dot(color=RED)
        dot.move_to(axes.i2gp(2, parabola))
        self.play(FadeIn(dot, scale=0.5))

        # A value tracker lets us animate a parameter, usually
        # with the intent of having other mobjects update based
        # on the parameter
        x_tracker = ValueTracker(2)
        f_always(
            dot.move_to,
            lambda: axes.i2gp(x_tracker.get_value(), parabola)
        )


        self.play(x_tracker.animate.set_value(4), run_time=3)
        self.play(x_tracker.animate.set_value(-2), run_time=3)
        self.wait()

class ParametricCircleDemo(Scene):
    @staticmethod
    def circle(t):
        x = sqrt(6) * np.cos(t) + 1
        y =  sqrt(5) * np.sin(t)
        return np.array([x, y, 0.0])
 
    def construct(self):
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-3, 3, 1],
            width=8,
            height=6,
            axis_config={
                "include_tip": True,
            }
        )
 
        param_curve = ParametricCurve(
            t_func=self.circle,
            t_range=[0,  np.pi, 0.05],
            color=GREEN,
        )
 
        # self.play(Write(axes), run_time=1)
        self.play(Write(param_curve))

        self.wait()

        dot = Dot(color=RED)
        start = axes.i2gp(1, param_curve)
        print(start)
        dot.move_to(start)
        self.play(FadeIn(dot, scale=0.5))

        self.wait(1)

        x_tracker = ValueTracker(1)
        f_always(
            dot.move_to,
            lambda: axes.i2gp(x_tracker.get_value(), param_curve)
        )

        # self.play(x_tracker.animate.set_value(3), run_time=3)
        self.play(x_tracker.animate.set_value(0), run_time=3)
        self.play(x_tracker.animate.set_value(2), run_time=3)
        self.wait()
        

class MovePointAlongPath(Scene):
    @staticmethod
    def eclipse(t):
        x = sqrt(7) * np.cos(t) * Draw_YY.UNIT_lEN + Draw_YY.UNIT_lEN * 2
        y =  sqrt(6) * np.sin(t) * Draw_YY.UNIT_lEN
        return np.array([x, y, 0.0])
    def construct(self):
        # 创建一个路径对象
        path = Circle(radius=2)

        eclipse_path = ParametricCurve(
            t_func=self.eclipse,
            t_range=[PI,  3/2 * PI,1e-4],
            color=GREEN,
        )

        # 创建一个点对象
        point = Dot(color=RED)

        # 创建一个移动对象，并将点对象与路径对象关联起来
        move_along_path = MoveAlongPath(point, eclipse_path)

        # 将点对象和路径对象添加到场景中
        self.add(path, point)

        # 播放移动动画
        self.play(move_along_path, run_time=5)

        self.wait()
