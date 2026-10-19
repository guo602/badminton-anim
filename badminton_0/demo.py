from manimlib import *


class badminton(ThreeDScene):
    # CONFIG = {
    #     "camera_class": ThreeDCamera,
    # }
    def __init__(self,  **kwargs):
        super().__init__(**kwargs)
        self.look_down_x = 0
        self.look_down_y = 0
        self.look_down_z = 0
        self.court_length_brace_stroke_width = 0.2
        self.mnemonic_d = 0.4
    def construct(self):
        COURT_line_width = 5
        print('camera height:',self.camera.get_frame_height())
        print('camera width:',self.camera.get_frame_width())

        # 获取相机帧的引用
        frame = self.camera.frame
        self.play(
          
            frame.animate.set_height(15).move_to(np.array([0,0,8])), # 旋转缩放相机帧
            run_time=0
        )
        axes = ThreeDAxes(rotation = PI/3)
        self.wait()
        green_bg = Rectangle(7.2,15)
        green_bg.set_fill('#2aa570', opacity=1)
        green_bg.set_stroke('#2aa570', width=0)
        self.play(FadeIn(green_bg)) 
        self.wait(0.1) 

        white_rec = Rectangle(6.1,13.4)
        white_rec.set_stroke('#ffffff', width=COURT_line_width)
        self.play(ShowCreation(white_rec)) 
        self.wait(0.2)

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

        longbrace_134 = BraceLabel(
            Line([-3.5,-6.7,0],[-3.5,6.7,0]),
            brace_direction = LEFT,
            color = BLACK,
            stroke_width = self.court_length_brace_stroke_width,
            text = "13.4m"


            )

        longbrace_076 = BraceLabel(
            Line([3.5,-6.7,0],[3.5, -6.7 + 0.76,0]),
            brace_direction = RIGHT,
            color = BLACK,
            stroke_width = self.court_length_brace_stroke_width,
            text = "0.76m"
            )
        longbrace_396 = BraceLabel(
            Line([3.5,-6.7 + 0.76,0],[3.5, -6.7 + 0.76 +3.96,0]),
            brace_direction = RIGHT,
            color = BLACK,
            stroke_width = self.court_length_brace_stroke_width,
            text = "3.96m"
            )

        brace_61 = BraceLabel(
            Line([-3.05,6.8,0],[3.05,6.8,0]),
            brace_direction = UP,
            color = BLACK,
            stroke_width = self.court_length_brace_stroke_width,
            text = "6.1m"


            )
        longbrace_26 =  BraceLabel(
            Line([-2.6,-6.7,0],[0,-6.7,0]),
            color = BLACK,
            stroke_width = self.court_length_brace_stroke_width,
            width = 20,
            text = "2.6m"
        )
        vertical_brace =  BraceLabel(
            Line([3.05,0,1.55],[3.05,0,0]),
            brace_direction = IN + RIGHT,
            color = BLACK,
            stroke_width = self.court_length_brace_stroke_width,
            text = "1.55m"
        ).rotate(PI/2,axis=RIGHT)

        arrow3D_155_0 = Arrow(start=np.array([3.4,0,1.35]), 
                                end=np.array([3.4,0,1.25]), 
                                thickness=0.02, height=0.3, 
                                base_radius=0.08, 
                                color=BLACK
                                )
        text_155 = Text('1.55m',
                        color = BLACK,
                        font_color=BLACK,
                        fill_color = BLACK,
                        
                        # stroke_width = 20,
                        font_size = 30,
                        ).rotate(PI/2,axis=RIGHT).move_to(np.array([3.4,0,1.55/2])).rotate(- PI/6,axis = IN).set_fill(color = BLACK)
        arrow3D_155_1 = Arrow(start=np.array([3.4,0,0.2]), 
                                end=np.array([3.4,0,0.3]), 
                                thickness=0.02, height=0.3, 
                                base_radius=0.08, 
                                color=BLACK
                                )


        self.play(
            FadeIn(longbrace_134),
            FadeIn(longbrace_26),
            ShowCreation(longbrace_076),
            ShowCreation(longbrace_396),
            ShowCreation(brace_61),
            # ShowCreation(longbrace_26),
            run_time = 2
            ) 

        self.wait(1)


        self.play(
            frame.animate.set_phi(70*DEGREES).move_to(np.array([2,-6,2])).set_width(13).set_theta(30*DEGREES),
            FadeOut(longbrace_134),
            FadeOut(longbrace_26),
            FadeOut(longbrace_076),
            FadeOut(longbrace_396),
            FadeOut(brace_61),
        )
        self.play(
            # ShowCreation(vertical_brace) ,
            ShowCreation(arrow3D_155_0) ,
            ShowCreation(text_155) ,
            ShowCreation(arrow3D_155_1) ,
            
        )
        self.wait(1)

        self.play(
            FadeOut(arrow3D_155_0) ,
            FadeOut(text_155) ,
            FadeOut(arrow3D_155_1) ,
            frame.animate.set_height(15).set_phi(0*DEGREES).move_to(np.array([0,0,8])).set_theta(-30*DEGREES), # 旋转缩放相机帧

        )

        single_court_rec = Polygon(
            [-3.05 + 0.42,6.7,0],
            [3.05 - 0.42,6.7,0],
            [3.05 - 0.42,-6.7,0],
            [-3.05+ 0.42,-6.7,0],
            color = GREY_B,
            fill_opacity = 0.5,
            stroke_width = 10,
            stroke_color = GREY_B,
            )
        double_court_rec = Polygon(
            [-3.05 ,6.7,0],
            [3.05 ,6.7,0],
            [3.05 ,-6.7,0],
            [-3.05,-6.7,0],
            color = GREY_B,
            fill_opacity = 0.5,
            stroke_width = 10,
            stroke_color = GREY_B,
            )
        
        self.play(
          
            FlashyFadeIn(single_court_rec)
        )
        self.play(  ShowPassingFlashAround(single_court_rec))
        self.wait()

        

        self.play(
            Transform(single_court_rec,double_court_rec)
        )
        self.play(  ShowPassingFlashAround(double_court_rec))
        self.wait()

        self.remove(double_court_rec)
        self.play(  FadeOut(single_court_rec))
       
        self.wait()

        

        # self.play(
        #     frame.animate.set_phi(70*DEGREES).move_to(np.array([0,-10,4])).set_width(12),
        #     run_time=1
        # )
        # self.play(
        #     frame.animate.set_height(15).set_phi(0*DEGREES).move_to(np.array([0,0,8])), # 旋转缩放相机帧
        # )
        # self.play(
        #     frame.animate.set_phi(70*DEGREES).move_to(np.array([0,-10,4])).set_width(12)
        # )
        # self.play(
        #     frame.animate.set_phi(70*DEGREES).move_to(np.array([1,-10,4])).set_width(12).set_theta(30*DEGREES)
        # )
        # self.play(
        #     frame.animate.set_phi(70*DEGREES).move_to(np.array([0,-10,4])).set_width(12).set_theta(0*DEGREES)
        # )

        

        start_rec_r_vertices = [
            np.array([0, -1.98, 0]),
            np.array([0 , -6.7, 0]),
            np.array([3.05 - 0.42  , -6.7, 0]),
            np.array([3.05 - 0.42 , -1.98, 0]),

        ]

        end_rec_r_vertices = [
            np.array([ - 3.05 + 0.42 , 1.98, 0]),
            
            np.array([ - 3.05 + 0.42  , 6.7, 0]),
            np.array([0 , 6.7, 0]),
            
            np.array([0, 1.98, 0]),
           

        ]
        start_rec_l_vertices = [
            
            np.array([- 3.05 + 0.42  , -6.7, 0]),
            np.array([ - 3.05 + 0.42 , -1.98, 0]),
            np.array([0, -1.98, 0]),
            np.array([0 , -6.7, 0]),
        ]

        end_rec_l_vertices = [
            np.array([0 , 6.7, 0]),
            np.array([0, 1.98, 0]),
            np.array([ 3.05 - 0.42 , 1.98, 0]),
            
            np.array([  3.05 - 0.42  , 6.7, 0]),
           

        ]
        # start_rec = Polygon(*start_rec_vertices)
        start_rec_r = Polygon(
            *start_rec_r_vertices,
            color = YELLOW,
            fill_opacity = 0.3,
            stroke_width = 10,
            stroke_color = YELLOW,

        )

        end_rec_r = Polygon(
            *end_rec_r_vertices,
            color = YELLOW,
            fill_opacity = 0.3,
            stroke_width = 10,
            stroke_color = YELLOW,

        )
        start_rec_l = Polygon(
            *start_rec_l_vertices,
            color = YELLOW,
            fill_opacity = 0.3,
            stroke_width = 10,
            stroke_color = YELLOW,

        )

        end_rec_l = Polygon(
            *end_rec_l_vertices,
            color = YELLOW,
            fill_opacity = 0.3,
            stroke_width = 10,
            stroke_color = YELLOW,

        )


        
        
        
        
        self.play(
            frame.animate.set_phi(70*DEGREES).move_to(np.array([0,-10,4])).set_width(12),
            run_time=1
        )

        ball_graph_on_line = axes.get_parametric_curve(
            lambda t: 3.2 * np.array([0.63 * np.cos(t) - 0.2,- 1.8 * np.cos(t) + 0.1, 0.5 * (t+0.1) *np.sin(t)]),
            t_range = [0.18 *  PI, 1 * PI],
            color = YELLOW,
            
        )

        ball_graph_on_line.set_stroke( width=7)

        # self.add(ball_graph_on_line)
        self.play(ShowCreation(ball_graph_on_line),
            run_time=1.2
        )
        self.play(FadeOut(ball_graph_on_line),
            run_time=0.8
        )

        on_line_point = Circle(
            arc_center = 3.2 * np.array([0.63 * np.cos(PI) - 0.2,- 1.8 * np.cos(PI) + 0.1, 0.5 * (PI+0.1) *np.sin(PI)]),
            radius = 0.01,
            stroke_width = 0,
            width = 0
        )
        on_line_point.set_fill(GREY_C,opacity = 0.7)
        self.add(on_line_point)

        self.play(
            frame.animate.move_to(np.array([-3.05 + 0.42, 3.2 * (1.8 + 0.1),0.1])), # 旋转缩放相机帧
            ShowCreation(ball_graph_on_line),
            run_time=2
        )
        self.play(
            frame.animate.set_phi(0*DEGREES), # 旋转缩放相机帧
            FadeOut(ball_graph_on_line),

        )
        self.play(
            frame.animate.set_height(0.5) # 旋转缩放相机帧
        )

        in_text =  Text('IN',font="Arial",shadow = 0.5,gloss = 0.5,reflectiveness = 0.5,).scale(0.08).move_to(np.array([-3.05 + 0.42, 3.2 * (1.8 + 0.1) - 0.13,0.1]))
        in_rectangle_bg = SurroundingRectangle(
                                                in_text,
                                                fill_opacity = 1,
                                                color = GREY_D,
                                                stroke_opacity = 0,
                                                stroke_width = 0,
                                                # gloss = 0.5,
                                                # reflectiveness = 0.5,

                                            ).set_height(in_text.get_height()+0.04,stretch=True).set_width(in_text.get_width()+0.2,stretch=True)

        self.play(
            FadeIn(in_rectangle_bg),
            FadeIn(in_text),
         run_time=1)
        
        self.wait(1)  # 等待1秒

        self.play(
            FadeOut(in_rectangle_bg),
            FadeOut(in_text),
            FadeOut(on_line_point),)

        self.play(

            frame.animate.set_phi(70*DEGREES).move_to(np.array([0,-10,4])).set_width(12),   
            run_time=3     
            )
        self.wait()
        
        start_text_1 = Text('1.赢者发球',
                        color = "#005436",
                        font="Apple LiGothic",
                        font_color=BLACK,
                        fill_color = BLACK,
                        
                        # stroke_width = 20,
                        font_size = 75,
                        ).rotate(70*DEGREES,axis=RIGHT).move_to(np.array([7,4,3])).set_fill(color = "#005436")
        start_text_2 = Text('2.左单右双',
                        color = BLACK,
                        font="Apple LiGothic",
                        font_color=BLACK,
                        fill_color = BLACK,
                        
                        # stroke_width = 20,
                        font_size = 75,
                        ).rotate(70*DEGREES,axis=RIGHT).move_to(np.array([7,4 - 1* self.mnemonic_d ,3 - 1 * self.mnemonic_d  * np.tan( 70*PI/180 ) ])).set_fill(color = "#005436")

        start_text_3 = Text('3.发对角线',
                        font="Apple LiGothic",
                        color = BLACK,
                        font_color=BLACK,
                        fill_color = BLACK,
                        
                        # stroke_width = 20,
                        font_size = 75,
                        ).rotate(70*DEGREES,axis=RIGHT).move_to(np.array([7,4 - 2 *self.mnemonic_d  ,3 - 2 *self.mnemonic_d * np.tan( 70*PI/180 ) ])).set_fill(color = "#005436")
        start_text_4 = Text('4.连发不换人(双打)',
                        color = GREY,
                        font="Arial",
                        font_color=GREY,
                        fill_color = GREY,
                        
                        # stroke_width = 20,
                        font_size = 75,
                        ).rotate(70*DEGREES,axis=RIGHT).move_to(np.array([8.3,4 - 3*self.mnemonic_d ,3 - 3*self.mnemonic_d  * np.tan( 70*PI/180 ) ])).set_fill(color = GREY)


        self.play(
            Write(start_text_1),
        )
        self.wait(0.2)
        self.play(
            Write(start_text_2),
        )
        self.wait(0.2)
        self.play(
            Write(start_text_3),
        )
        self.wait(0.2)

        self.play(
            Indicate(start_text_1,color = "#00a86b"),
            run_time=2)
        self.wait(1)
        self.play(
            Indicate(start_text_2,color = "#00a86b"),
            run_time=2
        )

        self.wait(1)

        ball_graph_r_normal = axes.get_parametric_curve(
            lambda t: 3.2 * np.array([0.4 * np.cos(t),- 1.6 * np.cos(t) + 0.1, 0.5 * (t+0.1) *np.sin(t)]),
            t_range = [0.18 *  PI, 1 * PI],
            color = YELLOW,
        )
        ball_graph_r_normal.set_stroke( width=8)

        ball_graph_l_normal = axes.get_parametric_curve(
            lambda t: 3.2 * np.array([-0.4 * np.cos(t),- 1.6 * np.cos(t) + 0.1, 0.5 * (t+0.1) *np.sin(t)]),
            t_range = [0.18 *  PI, 1 * PI],
            color = YELLOW,
        )
        ball_graph_l_normal.set_stroke( width=8)

        ball_graph_l_back = axes.get_parametric_curve(
            lambda t: 3.2 * np.array([0.4 * np.cos(t),1.8 * np.cos(t) - 0.12, 0.45 * (t+0.09) *np.sin(t)]),
            t_range = [0.18 *  PI, 1 * PI],
            color = YELLOW,
        )
        ball_graph_l_back.set_stroke( width=8)

        ball_graph_r_back = axes.get_parametric_curve(
            lambda t: 3.3 * np.array([0.41 * np.cos(t), - 1.8 * np.cos(t) - 0.12, 0.4 * (t+0.09) *np.sin(t)]),
            t_range = [0.18 *  PI, 1 * PI],
            color = YELLOW,
        )
        ball_graph_r_back.set_stroke( width=8)

        ball_graph_r_fault = axes.get_parametric_curve(
            lambda t: 3.2 * np.array([0.4 * 0.8,- 1.6 * np.cos(t) + 0.1, 0.5 * (t+0.1) *np.sin(t)]),
            t_range = [0.18 *  PI, 1 * PI],
            color = GREY_B,
            
        )
        ball_graph_r_fault.set_stroke( width=8)

        
        

       


        self.play(DrawBorderThenFill(start_rec_l),run_time=0.5)
        self.play(start_rec_l.animate.scale(1.1),
        run_time=0.2
        )
        self.play(start_rec_l.animate.scale(0.909),
        run_time=0.2
        )
        self.wait()

        self.play(ShowCreation(ball_graph_l_normal),
            run_time=1
        )
        self.wait(1)  #
        self.play(FadeOut(ball_graph_l_normal),
            FadeOut(start_rec_l),
            run_time=1
        )

        self.wait()
        self.play(DrawBorderThenFill(start_rec_r),run_time=0.5)
        self.play(start_rec_r.animate.scale(1.1),
        run_time=0.2
        )
        self.play(start_rec_r.animate.scale(0.909),
        run_time=0.2
        )

        self.wait()

        

        self.play(
            ShowCreation(ball_graph_r_normal),
            run_time=1
        )
        self.wait(1)  #
        self.play(FadeOut(ball_graph_r_normal),
            FadeOut(start_rec_r),
        
            run_time=1
        )


        self.play(
            Indicate(start_text_3,color = "#00a86b"),
            run_time=2
        )

        self.play(
            FadeOut(start_text_1),
            FadeOut(start_text_2),
            FadeOut(start_text_3),
            frame.animate.set_height(15).set_phi(0*DEGREES).move_to(np.array([0,0,8])), #正俯视
        )

        self.wait()

        self.play(
            FadeInFromPoint(start_rec_l,[ - 3.05/2,-6.7/2,0]),
        )
        self.wait()
        self.play(
            # DrawBorderThenFill(end_rec_l),
            FadeInFromPoint(end_rec_l,[ 3.05/2,6.7/2,0]),
        )
        self.wait()
        self.play(
            frame.animate.set_phi(70*DEGREES).move_to(np.array([0,-10,4])).set_width(12),
        )
        self.play(
            ShowCreation(ball_graph_l_normal),
        )
        self.play(
            frame.animate.set_phi(70*DEGREES).move_to(np.array([2,-6,2])).set_width(13).set_theta(30*DEGREES),
        )


        self.play(
            FadeOut(start_rec_l),
            FadeOut(ball_graph_l_normal),
            FadeOut(end_rec_l),
            frame.animate.set_phi(70*DEGREES).move_to(np.array([0,-10,4])).set_width(12).set_theta(0*DEGREES), # 旋转缩放相机帧

        )

        self.wait(0.2)
        self.play(
            FadeInFromPoint(start_rec_r,[3.05/2,-6.7/2,0]),
        )
        self.wait()
        self.play(
            frame.animate.set_height(15).set_phi(0*DEGREES).move_to(np.array([0,0,8])), #正俯视
        )
        self.play(
            # DrawBorderThenFill(end_rec_r),
            FadeInFromPoint(end_rec_r,[-3.05/2,6.7/2,0]),
        )
        self.wait()
        self.play(            
            frame.animate.set_phi(70*DEGREES).move_to(np.array([0,-10,4])).set_width(12)
            )
        self.play(
            ShowCreation(ball_graph_r_normal)
        )
        self.wait()
        self.play(
            FadeOut(ball_graph_r_normal)
        )
        self.wait()

        self.play(
            ShowCreation(ball_graph_r_fault)
        )

        cross_line0 = Line(
            start = [0,0,0],
            end = [1,-1,0],
            color = RED,
            stroke_width = 20,
        ).rotate(70*DEGREES,axis=RIGHT).move_to(np.array([5,2,1]))
        cross_line1 = Line(
            start = [1,0,0],
            end = [0,-1,0],
            color = RED,
            stroke_width= 20,
        ).rotate(70*DEGREES,axis=RIGHT).move_to(np.array([5,2,1]))


        self.play(
            FadeIn(cross_line0),
            FadeIn(cross_line1),
        )
        self.wait()

        self.play(
            FadeOut(cross_line0),
            FadeOut(cross_line1),
            FadeOut(ball_graph_r_fault),
            FadeOut(start_rec_r),
            FadeOut(end_rec_r),
        )

        self.play(
            frame.animate.set_height(12).move_to(np.array([0,0,0])), #正俯视

        )
        # Add ambient rotation
        camerra_rotate_updater = lambda m, dt: m.increment_theta(-0.5 * dt)
        frame.add_updater(camerra_rotate_updater)

        self.wait(1)


        for i in range(2):
            self.play(ShowCreationThenDestruction(ball_graph_l_normal),run_time=1.5)
            self.wait(0.1)
            self.play(ShowCreationThenDestruction(ball_graph_l_back),run_time=1.5)
            self.wait(0.1)
            self.play(ShowCreationThenDestruction(ball_graph_r_normal),run_time=1.5)
            self.wait(0.1)
            self.play(ShowCreationThenDestruction(ball_graph_r_back),run_time=1.5)
            self.wait(0.1)
        
        
        self.play(
            FadeOut(green_bg),
            FadeOut(white_rec),
            FadeOut(line1),
            FadeOut(line2),
            FadeOut(line3),
            FadeOut(line4),
            FadeOut(line5),
            FadeOut(line6),
            FadeOut(line7),
            FadeOut(line8),
            FadeOut(line9),
            FadeOut(line10),
            FadeOut(line11),
            FadeOut(line12),

            FadeOut(lines_group),
            FadeOut(lines_group_ver),
            FadeOut(line_grid_vgoup),
            run_time = 0.6,
        )
        frame.remove_updater(camerra_rotate_updater)

        self.wait(0.6)


    

        print('camera height:',self.camera.get_frame_height())
        print('camera width:',self.camera.get_frame_width())
        print('camera center:',self.camera.get_frame_center())
        print('camera location:',self.camera.get_location()) 






        
        # self.play(
        #     Write(start_text_4),
        # )

        # self.embed()

        # self.play(
        #      frame.animate.set_height(15).set_phi(0*DEGREES).move_to(np.array([0,0,8])), #正俯视
        # )
        
         


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


class SurfaceExample(Scene):
    CONFIG = {
        "camera_class": ThreeDCamera,
    }

    def construct(self):
        surface_text = Text("For 3d scenes, try using surfaces")
        surface_text.fix_in_frame()
        surface_text.to_edge(UP)
        self.add(surface_text)
        self.wait(0.1)

        torus1 = Torus(r1=1, r2=1)
        torus2 = Torus(r1=3, r2=1)
        sphere = Sphere(radius=3, resolution=torus1.resolution)
        # You can texture a surface with up to two images, which will
        # be interpreted as the side towards the light, and away from
        # the light.  These can be either urls, or paths to a local file
        # in whatever you've set as the image directory in
        # the custom_config.yml file

        day_texture = "/Users/burger/Documents/videos/manim/projects/startup/images/badminton.png"
        night_texture = "/Users/burger/Documents/videos/manim/projects/startup/images/InteractiveDevelopment.png"
        # day_texture = "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4d/Whole_world_-_land_and_oceans.jpg/1280px-Whole_world_-_land_and_oceans.jpg"
        # night_texture = "https://upload.wikimedia.org/wikipedia/commons/thumb/b/ba/The_earth_at_night.jpg/1280px-The_earth_at_night.jpg"

        surfaces = [
            TexturedSurface(surface, day_texture, night_texture)
            # TexturedSurface(surface)
            for surface in [sphere, torus1, torus2]
        ]

        for mob in surfaces:
            mob.shift(IN)
            mob.mesh = SurfaceMesh(mob)
            mob.mesh.set_stroke("#005436" , 1, opacity=0.5)

        # Set perspective
        frame = self.camera.frame
        frame.set_euler_angles(
            theta=-30 * DEGREES,
            phi=70 * DEGREES,
        )

        surface = surfaces[0]

        self.play(
            FadeIn(surface),
            ShowCreation(surface.mesh, lag_ratio=0.01, run_time=3),
        )
        for mob in surfaces:
            mob.add(mob.mesh)
        surface.save_state()
        self.play(Rotate(surface, PI / 2), run_time=2)
        for mob in surfaces[1:]:
            mob.rotate(PI / 2)

        self.play(
            Transform(surface, surfaces[1]),
            run_time=3
        )

        self.play(
            Transform(surface, surfaces[2]),
            # Move camera frame during the transition
            frame.animate.increment_phi(-10 * DEGREES),
            frame.animate.increment_theta(-20 * DEGREES),
            run_time=3
        )
        # Add ambient rotation
        frame.add_updater(lambda m, dt: m.increment_theta(-0.1 * dt))

        # Play around with where the light is
        light_text = Text("You can move around the light source")
        light_text.move_to(surface_text)
        light_text.fix_in_frame()

        self.play(FadeTransform(surface_text, light_text))
        light = self.camera.light_source
        self.add(light)
        light.save_state()
        self.play(light.animate.move_to(3 * IN), run_time=5)
        self.play(light.animate.shift(10 * OUT), run_time=5)

        drag_text = Text("Try moving the mouse while pressing d or s")
        drag_text.move_to(light_text)
        drag_text.fix_in_frame()

        self.play(FadeTransform(light_text, drag_text))
        self.wait()

class SurfaceExample2(Scene):
    CONFIG = {
        "camera_class": ThreeDCamera,
    }

    def construct(self):
        surface_text = Text("For 3d scenes, try using surfaces")
        surface_text.fix_in_frame()
        surface_text.to_edge(UP)
        self.add(surface_text)
        self.wait(0.1)
        green_bg = Rectangle(7.2,15)
        green_bg.set_fill('#2aa570', opacity=1)
        green_bg.set_stroke('#2aa570', width=0)
        # self.play(FadeIn(green_bg)) 

        torus1 = Torus(r1=1, r2=1)
        torus2 = Torus(r1=3, r2=1)
        sphere = Sphere(radius=3, resolution=torus1.resolution)
        # You can texture a surface with up to two images, which will
        # be interpreted as the side towards the light, and away from
        # the light.  These can be either urls, or paths to a local file
        # in whatever you've set as the image directory in
        # the custom_config.yml file

        day_texture = "/Users/burger/Documents/videos/manim/projects/startup/images/badminton.png"
        night_texture = "/Users/burger/Documents/videos/manim/projects/startup/images/InteractiveDevelopment.png"
        # day_texture = "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4d/Whole_world_-_land_and_oceans.jpg/1280px-Whole_world_-_land_and_oceans.jpg"
        # night_texture = "https://upload.wikimedia.org/wikipedia/commons/thumb/b/ba/The_earth_at_night.jpg/1280px-The_earth_at_night.jpg"

        surfaces = [
            TexturedSurface(surface, day_texture, night_texture)
            # TexturedSurface(surface)
            for surface in [sphere, torus1, torus2]
        ]

        for mob in surfaces:
            mob.shift(IN)
            mob.mesh = SurfaceMesh(mob)
            mob.mesh.set_stroke("#005436" , 1, opacity=0.5)

        # Set perspective
        frame = self.camera.frame
        frame.set_euler_angles(
            theta=-30 * DEGREES,
            phi=70 * DEGREES,
        )

        surface = surfaces[0]

        self.play(
            FadeIn(surface),
            ShowCreation(surface.mesh, lag_ratio=0.01, run_time=3),
        )
        for mob in surfaces:
            mob.add(mob.mesh)
        surface.save_state()
        self.play(Rotate(surface, PI / 2), run_time=2)
        for mob in surfaces[1:]:
            mob.rotate(PI / 2)

        self.play(
            Transform(surface, surfaces[1]),
            run_time=3
        )

        self.play(
            # Transform(surface, green_bg),
            FadeOut(surface),
            FadeOut(surfaces[1]),
            ShowCreation(green_bg) ,
            # Move camera frame during the transition
            frame.animate.increment_phi(-10 * DEGREES),
            frame.animate.increment_theta(-20 * DEGREES),
            run_time=3
        )
        print('camera height:',self.camera.get_frame_height())
        print('camera width:',self.camera.get_frame_width())
        print('camera center:',self.camera.get_frame_center())
        print('camera location:',self.camera.get_location()) 

        # Add ambient rotation
        camerra_rotate_updater = lambda m, dt: m.increment_theta(-0.1 * dt)

        frame.add_updater(camerra_rotate_updater)

        # Play around with where the light is
        light_text = Text("You can move around the light source")
        light_text.move_to(surface_text)
        light_text.fix_in_frame()

        self.play(FadeTransform(surface_text, light_text))
        light = self.camera.light_source
        self.add(light)
        light.save_state()
        self.play(light.animate.move_to(3 * IN), run_time=5)
        self.play(light.animate.shift(10 * OUT), run_time=5)

        drag_text = Text("Try moving the mouse while pressing d or s")
        drag_text.move_to(light_text)
        drag_text.fix_in_frame()

        self.play(FadeTransform(light_text, drag_text))
        self.wait()

        frame.remove_updater(camerra_rotate_updater)


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