from manimlib import *


class badminton(Scene):
    def construct(self):
        COURT_line_width = 5
        print('camera height:',self.camera.get_frame_height())
        print('camera width:',self.camera.get_frame_width())

        # 获取相机帧的引用
        frame = self.camera.frame
        self.play(
          
            frame.animate.set_width(200).set_height(20), # 旋转缩放相机帧
            run_time=0
        )

        self.wait()
        green_bg = Rectangle(7.2,15)
        green_bg.set_fill('#2aa570', opacity=1)
        green_bg.set_stroke('#2aa570', width=0)
        self.play(DrawBorderThenFill(green_bg)) 
        self.wait(1) 

        white_rec = Rectangle(6.1,13.4)
        white_rec.set_stroke('#ffffff', width=COURT_line_width)
        self.play(ShowCreation(white_rec)) 
        self.wait(1)

        line1 = Line(start=[-3.05, 0, 0], end=[3.05, 0, 0])  # 创建一条起点为(-3, 0, 0)，终点为(3, 0, 0)的直线
        line1.set_fill('#ffffff', opacity=0)
        line1.set_stroke(width = COURT_line_width)

        line2 = Line(start=[-3.05, 1.98, 0], end=[3.05, 1.98, 0]) 
        line2.set_fill('#ffffff')
        line2.set_stroke(width = COURT_line_width)

        line3 = Line(start=[-3.05, -1.98, 0], end=[3.05, -1.98, 0]) 
        line3.set_fill('#ffffff')
        line3.set_stroke(width = COURT_line_width)

        line4 = Line(start=[0, -1.98, 0], end=[0, -6.7 , 0]) 
        line4.set_fill('#ffffff')
        line4.set_stroke(width = COURT_line_width)

        line5 = Line(start=[0, 1.98, 0], end=[0, 6.7 , 0]) 
        line5.set_fill('#ffffff')
        line5.set_stroke(width = COURT_line_width)

        line6 = Line(start=[-3.05, 6.7-0.72, 0], end=[3.05,6.7-0.72, 0]) 
        line6.set_fill('#ffffff')
        line6.set_stroke(width = COURT_line_width)

        line7 = Line(start=[-3.05, -6.7 + 0.72, 0], end=[3.05, -6.7 + 0.72, 0]) 
        line7.set_fill('#ffffff')
        line7.set_stroke(width = COURT_line_width)

        line8 = Line(start=[-3.05 + 0.42, 6.7, 0], end=[-3.05 + 0.42 , -6.7, 0]) 
        line8.set_fill('#ffffff')
        line8.set_stroke(width = COURT_line_width)

        line9 = Line(start=[3.05 - 0.42, 6.7, 0], end=[3.05 - 0.42 , -6.7, 0]) 
        line9.set_fill('#ffffff')
        line9.set_stroke(width = COURT_line_width)

        line10 = Line(start=[3.05 ,0, 0], end=[3.05 , 0, 1.55],color = BLUE) 
        line10.set_stroke(width = COURT_line_width)

        line11 = Line(start=[-3.05 , 0, 0], end=[-3.05 ,0 , 1.55],color = BLUE) 
        line11.set_stroke(width = COURT_line_width)

        line12 = Line(start=[3.05 , 0, 1.55], end=[-3.05 ,0 , 1.55]) 
        line12.set_fill('#ffffff')
        line12.set_stroke(width = COURT_line_width)

        line_grid_vgoup = VGroup()

        for i in range(0,760,20):
            line_height = 1.55 - 0.76 + i/1000
            grid_line = Line(start=[3.05 , 0, line_height], end=[-3.05 ,0 , line_height],color = '#333333') 
            grid_line.set_stroke(width = COURT_line_width/10)

            line_grid_vgoup.add(grid_line)






        lines_group = VGroup(line1, line2,line3,line4,line5,line6,line7,line8,line9)
        lines_group_ver  = VGroup(line11, line10,line12)

        self.play(ShowCreation(lines_group))  # 播放动画，绘制直线
        self.play(ShowCreation(lines_group_ver)) 
        self.play(ShowCreation(line_grid_vgoup)) 
      
       
       
      
        self.wait(1)  # 等待1秒


class InteractiveDevelopment(Scene):
    def construct(self):
        circle = Circle()
        circle.set_fill(BLUE, opacity=0.5)
        circle.set_stroke(BLUE_E, width=4)
        square = Square()

        self.play(ShowCreation(square))
        self.wait()

        # 这会打开一个iPython终端，你可以在其中继续写你想要执行的代码
        # 在这个例子中，square/circle/self都会成为终端中的实例
        self.embed()


class AnimatingMethods(Scene):
    def construct(self):
        grid = Tex(r"\pi").get_grid(10, 10, height=4)
        self.add(grid)

        # 你可以通过.animate语法来动画化物件变换方法
        self.play(grid.animate.shift(LEFT))

        # 或者你可以使用旧的语法，把方法和参数同时传给Scene.play
        self.play(grid.shift, LEFT)

        # 这两种方法都会在mobject的初始状态和应用该方法后的状态间进行插值
        # 在本例中，调用grid.shift(LEFT)会将grid向左移动一个单位

        # 这种用法可以用在任何方法上，包括设置颜色
        self.play(grid.animate.set_color(YELLOW))
        self.wait()
        self.play(grid.animate.set_submobject_colors_by_gradient(BLUE, GREEN))
        self.wait()
        self.play(grid.animate.set_height(TAU - MED_SMALL_BUFF))
        self.wait()

        # 方法Mobject.apply_complex_function允许应用任意的复函数
        # 将把Mobject的所有点的坐标看作复数

        self.play(grid.animate.apply_complex_function(np.exp), run_time=5)
        self.wait()

        # 更一般地说，你可以应用Mobject.apply方法，它接受从R^3到R^3的一个函数
        self.play(
            grid.animate.apply_function(
                lambda p: [
                    p[0] + 0.5 * math.sin(p[1]),
                    p[1] + 0.5 * math.sin(p[0]),
                    p[2]
                ]
            ),
            run_time=5,
        )
        self.wait()