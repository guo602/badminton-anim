from manimlib import *
from math import sqrt

# from manimlib.utils.space_ops import line_intersects_path


def Range(in_val,end_val,step=1):
    return list(np.arange(in_val,end_val+step,step))

def line_intersects_path(
    start,
    end,
    path,
) -> bool:
    """
    Tests whether the line (start, end) intersects
    a polygonal path defined by its vertices
    """
    n = len(path) - 1
    p1 = np.empty((n, 2))
    q1 = np.empty((n, 2))
    p1[:] = start[:2]
    q1[:] = end[:2]
    p2 = path[:-1, :2]
    q2 = path[1:, :2]

    v1 = q1 - p1
    v2 = q2 - p2

    mis1 = cross2d(v1, p2 - p1) * cross2d(v1, q2 - p1) < 0
    mis2 = cross2d(v2, p1 - p2) * cross2d(v2, q1 - p2) < 0
    return bool((mis1 * mis2).any())

class yylogo_svg(Scene):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.white_0 = None

    def generate_curve(str):
        pass

    def construct(self):
        COURT_line_width = 5
        print('camera height:',self.camera.get_frame_height())
        print('camera width:',self.camera.get_frame_width())

        # 获取相机帧的引用
        frame = self.camera.frame
        self.play(
          
            frame.animate.set_width(1024).set_height(285), # 旋转缩放相机帧
            run_time=0
        )

        c1 = Circle(arc_center = [0,0,0])
        c1.set_fill(BLUE, opacity=0.5)
        c1.set_stroke(BLUE_E, width=4)

        self.play(ShowCreation(c1))

        c2 = Circle(arc_center = [143.445,-27.414,0])
        c2.set_fill(BLUE, opacity=0.5)
        c2.set_stroke(BLUE_E, width=4)

        self.play(ShowCreation(c2))

        self.wait()

        # paint green 
        path2 = VMobject()
        start_point = np.array([0,-27.208,0])
        path_point = start_point
        path2.start_new_path(path_point)


        path_point += np.array([130.044,0,0])
        path2.add_line_to(path_point)

        path_point += np.array([0,12.137,0])
        path2.add_line_to(path_point)

        path_point += np.array([13.401,-25.352,0])
        path2.add_line_to(path_point)

        path_point += np.array([0,13.215,0])
        path2.add_line_to(path_point)

        path_point += np.array([62.065,0,0])
        path2.add_line_to(path_point)

        path_point += np.array([0,-27.607,0])
        path2.add_line_to(path_point)

        path_point += np.array([-205.51,0,0])
        path2.add_line_to(path_point)

        path_point += np.array([0,27.607,0])
        path2.add_line_to(path_point)

        path2.add_line_to(start_point)

        path2.set_fill('#1d9533',opacity=1)
        self.play(DrawBorderThenFill(path2),run_time=2) 

        

        blue_block = VMobject()
        blue_block_start_point = np.array([143.445,-27.414,0])
        blue_block_path_point = blue_block_start_point
        blue_block.start_new_path(blue_block_path_point)

        blue_block_path_point += np.array([62.065,0,0])
        blue_block.add_line_to(blue_block_path_point)

        blue_block.add_line_to(np.array([205.51,0,0]))

        blue_block.add_line_to(np.array([0,0,0]))

        # blue_block.add_line_to(np.array([0,-27.414,0]))

        blue_block_path_point = np.array([0,0,0]) + np.array([0,-27.414,0])
        blue_block.add_line_to(blue_block_path_point)

        blue_block_path_point += np.array([130.044,0,0])
        blue_block.add_line_to(blue_block_path_point)

        blue_block_path_point += np.array([0,12.135,0])
        blue_block.add_line_to(blue_block_path_point)

        blue_block_path_point += np.array([13.401,-25.349,0])
        blue_block.add_line_to(blue_block_path_point)

        blue_block_path_point += np.array([0,13.214,0])
        blue_block.add_line_to(blue_block_path_point)

        blue_block.add_line_to(blue_block_start_point)

        blue_block.set_fill('#0b50a1',opacity=1)
        self.play(DrawBorderThenFill(blue_block),run_time=2) 
        

        white_0 = VMobject()
        white_0_start_point = np.array([46.481,-44.493,0])
        white_0.start_new_path(white_0_start_point)

        white_0.add_cubic_bezier_curve_to(np.array([51.696, -44.493,0]),
                                                   np.array([56.964, -40.249,0]),
                                                    np.array([56.964, -34.99,0]))

        white_0.add_cubic_bezier_curve_to(np.array([56.964, -29.751,0]),
                                                    np.array([52.696, -25.509,0]),
                                                   np.array( [47.481, -25.509,0]))

        white_0.add_cubic_bezier_curve_to(np.array([42.2225, -25.509,0]),
                                                    np.array([37.0037, -29.752,0]),
                                                   np.array( [37.0037, -34.99,0]))

        white_0.add_cubic_bezier_curve_to(np.array([37.0037, -40.249,0]),
                                                   np.array( [41.2225, -44.493,0]),
                                                   np.array( [46.481, -44.493,0]))

        # white_0.add_cubic_bezier_curve_to(np.array([5.215,0,0]),
        #                                            np.array([9.483,4.244,0]),
        #                                             np.array([9.483,9.503,0]))

        # white_0.add_cubic_bezier_curve_to(np.array([0,-5.239,0]),
        #                                             np.array([-4.268,9.482,0]),
        #                                            np.array( [-9.483,9.482,0]))

        # white_0.add_cubic_bezier_curve_to(np.array([-5.2585,0,0]),
        #                                             np.array([-9.4773,-4.243,0]),
        #                                            np.array( [-9.4773,-9.482,0]))

        # white_0.add_cubic_bezier_curve_to(np.array([0,5.259,0]),
        #                                            np.array( [4.2188,-9.503,0]),
        #                                            np.array( [9.4773,-9.503,0]))
        
        
        
        white_0.set_fill('#feffff',opacity=1)
        self.play(DrawBorderThenFill(white_0),run_time=2) 

        
        self.wait()

class yylogo(Scene):
    
    def construct(self):
         # 获取相机帧的引用
        frame = self.camera.frame
        self.play(
          
            frame.animate.set_width(280).set_height(150), # 旋转缩放相机帧
            run_time=0
        )

        path2 = VMobject()
        start_point = np.array([0,0,0])
        path_point = start_point
        path2.start_new_path(np.array([0,0,0]))
        path2.add_line_to(np.array([36,0,0]))
        path2.add_line_to(np.array([18,-18*1.73,0]))

        arc = ArcBetweenPoints(np.array([0,0,0]),np.array([18,-18*1.73,0]),angle = -PI/3)
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
        path3.add_line_to(np.array([18,-18*1.73,0])+start_point)

        arc2 = ArcBetweenPoints(np.array([0,0,0])+start_point,np.array([18,-18*1.73,0])+start_point,angle = -PI/3)
        path3.add_subpath(arc2.get_points()[::-1])
        # self.play(ShowCreation(path3))

        path2.set_fill(color='#feffff',opacity=1)
        path3.set_fill(color='#feffff',opacity=1)

        self.play(DrawBorderThenFill(path2),
        DrawBorderThenFill(path3))


        circle_l = Circle(radius = 12.5,arc_center = [2,-32,0])
        circle_l.set_fill(color = '#feffff',opacity=1)
        circle_l.set_stroke(color='#feffff')
        self.play(ShowCreation(circle_l))

        circle_r = Circle(radius = 12.5,arc_center = [38,-32,0])
        circle_r.set_fill(color = '#feffff',opacity=1)
        circle_r.set_stroke(color='#feffff')
        self.play(ShowCreation(circle_r))

        circle3 = Circle(radius = 36,arc_center = [-18,-18*1.732,0])
        self.play(ShowCreation(circle3))
        circle4 = Circle(radius = 36,arc_center = [18,-18*1.732,0])
        self.play(ShowCreation(circle3))




        


        

        

       


        

        





class yylogo_rc(Scene):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.TRIANGLE_SIDE_LENGTH = 36 #三角形边长

    def get_coord_from_proportion(self,vmob,proportion):
        return vmob.point_from_proportion(proportion)

    def get_points_from_curve(self, vmob, dx=0.005):
        coords = []
        for point in Range(0, 1, dx):
            dot = Dot(self.get_coord_from_proportion(vmob,point))
            coords.append(dot.get_center())
        return coords

    def get_intersections_between_two_vmobs(self, vmob1, vmob2,
                                            tolerance=0.05,
                                            radius_error=0.2,
                                            use_average=True,
                                            use_first_vmob_reference=False):
        coords_1 = self.get_points_from_curve(vmob1)
        coords_2 = self.get_points_from_curve(vmob2)
        intersections = []
        for coord_1 in coords_1:
            for coord_2 in coords_2:
                distance_between_points = get_norm(coord_1 - coord_2)
                if use_average:
                    coord_3 = (coord_2 - coord_1) / 2
                    average_point = coord_1 + coord_3
                else:
                    if use_first_vmob_reference:
                        average_point = coord_1
                    else:
                        average_point = coord_2
                if len(intersections) > 0 and distance_between_points < tolerance:
                    last_intersection=intersections[-1]
                    distance_between_previus_point = get_norm(average_point - last_intersection)
                    if distance_between_previus_point > radius_error:
                        intersections.append(average_point)
                if len(intersections) == 0 and distance_between_points < tolerance:
                    intersections.append(average_point)
        return intersections

    def construct(self):
        frame = self.camera.frame
        self.play(
          
            frame.animate.set_width(280).set_height(150), # 旋转缩放相机帧
            run_time=0
        )

        path2 = VMobject()
        start_point = np.array([0,0,0])
        path_point = start_point
        path2.start_new_path(np.array([0,0,0]))
        path2.add_line_to(np.array([36,0,0]))
        path2.add_line_to(np.array([18,-18*1.73,0]))

        arc = ArcBetweenPoints(np.array([0,0,0]),np.array([18,-18*1.73,0]),angle = -PI/3)
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
        path3.add_line_to(np.array([18,-18*1.73,0])+start_point)

        arc2 = ArcBetweenPoints(np.array([0,0,0])+start_point,np.array([18,-18*1.73,0])+start_point,angle = -PI/3)
        path3.add_subpath(arc2.get_points()[::-1])
        # self.play(ShowCreation(path3))

        path2.set_fill(color='#feffff',opacity=1)
        path3.set_fill(color='#feffff',opacity=1)

        self.play(DrawBorderThenFill(path2),
        DrawBorderThenFill(path3))


        # circle_l = Circle(radius = 12.5,arc_center = [2,-32,0])
        # circle_l.set_fill(color = '#feffff',opacity=1)
        # circle_l.set_stroke(color='#feffff')
        # self.play(ShowCreation(circle_l))

        # circle_r = Circle(radius = 12.5,arc_center = [38,-32,0])
        # circle_r.set_fill(color = '#feffff',opacity=1)
        # circle_r.set_stroke(color='#feffff')
        # self.play(ShowCreation(circle_r))

        circle3 = Circle(radius = 36,arc_center = [-18,-18*sqrt(3),0])
        circle4 = Circle(radius = 36,arc_center = [18,-18*sqrt(3),0])
        H_line = DashedLine(start = np.array([-20,-18*sqrt(3),0]),end =  np.array([60,-18*sqrt(3),0]))
        

        distance = np.linalg.norm(np.array([18,0,0]) - np.array([54,-18*sqrt(3),0]))
        r5 = distance
        circle5 = Circle(radius = r5,arc_center = np.array([18,0,0]))

        r7 = 54
        circle7 = Circle(radius = r7,arc_center = np.array([72,0,0]))



        self.play(ShowCreation(circle4),
                    ShowCreation(circle3),
                    ShowCreation(H_line),
                     ShowCreation(circle5),
                     ShowCreation(circle7),

                )
        # intersection_points_2cicle = circle5.get_intersection_points(circle7)  # 获取两个圆的交点
        # intersection_points_cl = self.get_intersections_between_two_vmobs(circle5, circle7)
        # intersection_points_cl = line_intersects_path(np.array([-20,-18*sqrt(3),0]),np.array([60,-18*sqrt(3),0]),circle5)
       
        print(circle5.get_points())
        # print(len(circle7.get_points()))
        # print(len(H_line.get_points()))
        # self.play(
        # #     # ShowCreation(intersection_points_2cicle),
        #             ShowCreation(),
        # )
        for point in circle5.get_points():
            self.play(ShowCreation(Circle(arc_center = np.array(point))))
        print(self.TRIANGLE_SIDE_LENGTH)
        self.wait(1)





