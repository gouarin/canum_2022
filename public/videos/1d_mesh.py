import numpy as np
from manim import *
from interval import *

config.background_color = "#ffffff"
# config.background_color = "#000000"

center = [2, 3, 0]

stroke_width = 4
default_color = "#000001"

intervals_color = ["#f98a00", "#009a8e", "#750013"]

intervals = {
    0: [[0, 2], [5, 6]],
    1: [[4, 5], [6, 8], [9, 10]],
    2: [[10, 12], [16, 18]],
}

def init_mesh():
    mesh = []
    colors = []
    levels = []

    for k, v in intervals.items():
        mesh.append(VGroup())
        colors.append(intervals_color[k])
        levels.append(k)
        for i in v:
            mesh[-1].add(Interval(k, range=i,  stroke_width=stroke_width, color=default_color))

    return VGroup(*mesh), colors, levels

def init_axe():
    level_axe = NumberLine(x_range=[0, 3], unit_size=2, include_tip=True, tip_length=0.1, rotation=90*DEGREES, label_direction=LEFT, color=default_color)
    level_axe.add_numbers(font_size=34, color=default_color)
    level_axe.shift(LEFT + 3*UP)

    level_label = Text("level", font_size=20, color=default_color)
    level_label.next_to(level_axe, LEFT)

    return VGroup(level_axe, level_label)

class mesh_scene_1_light(MovingCameraScene):
    def construct(self):
        mesh, colors, levels = init_mesh()
        self.camera.frame.move_to(mesh)
        self.play(Create(mesh))#, run_time=2)

        self.play(*[m.animate.set_color(c) for m, c in zip(mesh, colors)], run_time=2)

class mesh_scene_2_light(MovingCameraScene):
    def construct(self):
        mesh, colors, levels = init_mesh()
        self.camera.frame.move_to(mesh)
        [m.set_color(c) for m, c in zip(mesh, colors)]
        self.add(mesh)

        self.wait(1)

        axe = init_axe()
        all = VGroup(axe, mesh)

        self.play(*[m.animate.shift(2*l*UP) for m, l in zip(mesh, levels)],
                  Create(axe),
                  self.camera.frame.animate.move_to(all)
        )

def init_dx(ug):
    dx = MathTex(r"\Delta x = 2^{-level}", font_size=20, color=default_color)
    dx.move_to([2, 1, 0])

    level_info = VGroup()
    for i in range(len(ug)):
        itext = MathTex(f"\\frac{{1}}{{ {1<<i} }}" if i != 0 else "1", font_size=16, color=default_color)
        itext.move_to(ug[i].get_center() - [0, .3, 0])
        l_text = MathTex(f"level \quad {i}", font_size=16, color=default_color)
        l_text.move_to([-1, i, 0])
        level_info.add(VGroup(l_text, itext))

    return dx, level_info
class mesh_scene_3_light(MovingCameraScene):
    def construct(self):
        mesh, colors, levels = init_mesh()
        [m.set_color(c) for m, c in zip(mesh, colors)]

        axe = init_axe()
        all = VGroup(axe, mesh)

        [m.shift(2*l*UP) for m, l in zip(mesh, levels)]
        self.camera.frame.move_to(all)
        self.add(all)

        self.wait(1)
        self.camera.frame.save_state()

        unit_mesh = [Interval(l, range=[0, 1], stroke_width=stroke_width*0.5, color=c) for m, l, c in zip(mesh, levels, colors)]
        [m.shift(l*UP) for m, l in zip(unit_mesh, levels)]

        ug = VGroup(*unit_mesh)
        g = VGroup(*mesh)
        g.save_state()
        self.play(axe.animate.set_opacity(0),
                  Transform(g, ug),
                  self.camera.frame.animate.scale(0.5).move_to(ug)
        )

        self.wait(1)

        dx, level_info = init_dx(ug)
        self.play(Create(dx))

        self.wait()

        self.play(Create(level_info[0]))
        self.play(Create(level_info[1]))
        self.play(Create(level_info[2]))

        self.wait()
        # self.play(*[m.animate.add_cell_numbers(font_size=24, color=default_color) for me in mesh for m in me])

        # self.camera.frame.save_state()

        # unit_mesh = [Interval(l, range=[0, 1], stroke_width=stroke_width, color=c) for m, l, c in zip(mesh, levels, colors)]
        # [m.shift(l*UP) for m, l in zip(unit_mesh, levels)]

        # ug = VGroup(*unit_mesh)
        # g = VGroup(*mesh)
        # g.save_state()
        # self.play(axe.animate.set_opacity(0),
        #           Transform(g, ug),
        #           self.camera.frame.animate.scale(0.5).move_to(ug)
        # )

        # self.wait(1)

        # self.play(axe.animate.set_opacity(1),
        #           Restore(g),
        #           Restore(self.camera.frame))

        self.wait()

class mesh_scene_4_light(MovingCameraScene):
    def construct(self):
        mesh, colors, levels = init_mesh()
        [m.shift(2*l*UP) for m, l in zip(mesh, levels)]

        [m.set_color(c) for m, c in zip(mesh, colors)]
        axe = init_axe()
        all = VGroup(axe, mesh)

        unit_mesh = VGroup(*[Interval(l, range=[0, 1], stroke_width=stroke_width*0.5, color=c) for m, l, c in zip(mesh, levels, colors)])
        [m.shift(l*UP) for m, l in zip(unit_mesh, levels)]

        dx, level_info = init_dx(unit_mesh)

        old = VGroup(unit_mesh, dx, level_info)
        self.camera.frame.scale(0.5).move_to(unit_mesh)
        self.add(old)

        self.play(
                  Transform(old, all),
                  self.camera.frame.animate.scale(2).move_to(all)
        )

        self.play(*[m.animate.add_cell_numbers(font_size=24, color=default_color) for me in mesh for m in me])

        center = MathTex("c_i^l = \\left(i +\\frac{1}{2}\\right)\Delta x", font_size=36, color=BLUE)
        center.move_to([7, 5, 0])

        self.play(Create(center))
        self.wait(1)

        r0 = Rectangle(width=1, height=0.5, stroke_color=default_color)
        r0.move_to([0.5, 0.3, 0])
        r1 = Rectangle(width=.5, height=0.5, stroke_color=default_color)
        r1.move_to([2.25, 2.3, 0])

        c0 = MathTex("0.5", font_size=20, color=default_color)
        c0.move_to([0.5, 0.3, 0])
        c1 = MathTex("1.5", font_size=20, color=default_color)
        c1.move_to([1.5, 0.3, 0])
        c2 = MathTex("5.5", font_size=20, color=default_color)
        c2.move_to([5.5, 0.3, 0])
        c3 = MathTex("2.25", font_size=20, color=default_color)
        c3.move_to([2.25, 2.3, 0])
        c4 = MathTex("0.25", font_size=20, color=default_color)
        c4.move_to([0.25, 2.3, 0])

        self.play(Create(r0), Create(c0))
        self.wait()

        self.play(r0.animate.move_to([1.5, 0.3, 0]), Transform(c0, c1))
        self.wait()

        self.play(r0.animate.move_to([5.5, 0.3, 0]), Transform(c0, c2))
        self.wait()
        self.play(Transform(r0, r1), Transform(c0, c3))
        self.wait()

        i = Interval(1, range=[0, 4],  stroke_width=stroke_width, color=intervals_color[1])
        i.set_opacity(0.25)
        i.add_cell_numbers(font_size=24, color=default_color)
        i.shift(2*UP)
        self.play(Create(i))
        self.wait(1)

        self.play(r0.animate.move_to([0.25, 2.3, 0]), Transform(c0, c4))
        self.wait()
