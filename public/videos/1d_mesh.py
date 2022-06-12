import numpy as np
from manim import *
from interval import *
from number_line import *

from manim.utils.tex_templates import _new_ams_template

oswald = _new_ams_template()
oswald.description = "Oswald"
oswald.add_to_preamble(
    r"""
\usepackage[T1]{fontenc}
\usepackage{Oswald}
\renewcommand{\familydefault}{\sfdefault}
\usepackage[frenchmath]{mathastext}
""",
)

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

with register_font("../theme/fonts/Oswald-Regular.ttf"):
    Text.set_default(font="Oswald")

MathTex.set_default(tex_template=oswald, font_size=30, color=default_color)

Interval.set_default(stroke_width=stroke_width, color=default_color, tick_size=0.1)

def init_mesh():
    mesh = []
    colors = []
    levels = []

    for k, v in intervals.items():
        mesh.append(VGroup())
        colors.append(intervals_color[k])
        levels.append(k)
        for i in v:
            mesh[-1].add(Interval(k, range=i))

    return VGroup(*mesh), colors, levels

def init_axe():
    level_axe = MyNumberLine(x_range=[0, 2.5], unit_size=2, include_tip=True, tip_length=0.1, rotation=90*DEGREES, label_direction=LEFT, color=default_color)
    level_axe.add_numbers()
    level_axe.shift(LEFT + 2.5*UP)

    level_label = MathTex("Level")
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
        self.wait(1)

def init_dx(ug):
    dx = MathTex(r"\Delta x = 2^{-level}", font_size=20)
    dx.move_to([2, 1, 0])

    level_info = VGroup()
    for i in range(len(ug)):
        itext = MathTex(f"\\frac{{1}}{{ {1<<i} }}" if i != 0 else "1", font_size=16)
        itext.move_to(ug[i].get_center() - [0, .3, 0])
        l_text = MathTex(f"level \quad {i}", font_size=16)
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

        unit_mesh = [Interval(l, range=[0, 1], stroke_width=stroke_width*0.5, color=c, tick_size=0.05) for m, l, c in zip(mesh, levels, colors)]
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

        center = MathTex("c_i^l = \\left(i +\\frac{1}{2}\\right)\Delta x", font_size=36)
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

class interval_scene_1_light(MovingCameraScene):
    def construct(self):
        mesh, colors, levels = init_mesh()
        [m.set_color(c) for m, c in zip(mesh, colors)]

        axe = init_axe()
        all = VGroup(axe, mesh)

        [m.shift(2*l*UP) for m, l in zip(mesh, levels)]

        level_tex = VGroup()
        for i in range(3):
            level_tex.add(MathTex(f"Level \\, {i} \\rightarrow ", font_size=36, color=intervals_color[i]))
            level_tex[-1].move_to([0, -1.5 - 0.75*i, 0])

        all_all = VGroup(all, level_tex)
        self.camera.frame.move_to(all_all)
        self.camera.frame.scale(1.1)

        [m.add_cell_numbers(font_size=24, color=default_color) for me in mesh for m in me]

        self.add(all_all)
        self.wait(1)

        r = []
        for k, v in intervals.items():
            dx = 1./(1<<k)
            for i, e in enumerate(v):
                r.append(Rectangle(width=dx*(e[1] - e[0]), height=0.3, color=intervals_color[k], fill_opacity=0.5))
                r[-1].move_to([0.5*dx*(e[1] + e[0]), 2*k, 0])
                self.play(Create(r[-1]))
                self.wait(1)

                t = MathTex(f"[{e[0]}, {e[1]}[", font_size=36, color=intervals_color[k])
                if i==0:
                    t.next_to(level_tex[k], RIGHT)
                else:
                    t.next_to(r[-2], RIGHT)
                self.play(Transform(r[-1], t))
                self.wait()

        self.wait()


class interval_scene_2_light(MovingCameraScene):
    def construct(self):
        mesh, colors, levels = init_mesh()
        [m.set_color(c) for m, c in zip(mesh, colors)]

        axe = init_axe()
        all = VGroup(axe, mesh)

        [m.shift(2*l*UP) for m, l in zip(mesh, levels)]

        level_tex = VGroup()
        for i in range(3):
            level_tex.add(MathTex(f"Level \\, {i} \\rightarrow ", font_size=36, color=intervals_color[i]))
            level_tex[-1].move_to([0, -1.5 - 0.75*i, 0])

        all_all = VGroup(all, level_tex)
        self.camera.frame.move_to(all_all)
        self.camera.frame.scale(1.1)

        [m.add_cell_numbers(font_size=24) for me in mesh for m in me]

        index = 0
        for k, v in intervals.items():
            for ie, e in enumerate(v):
                for i in range(e[1]-e[0]):
                    center = mesh[k][ie].cell_numbers[i] .get_center()
                    mesh[k][ie].cell_numbers[i] = MathTex(index, font_size=24)
                    mesh[k][ie].cell_numbers[i].move_to(center)
                    index += 1

        self.add(all_all)

        index = 0
        for k, v in intervals.items():
            dx = 1./(1<<k)
            for i, e in enumerate(v):
                t1 = MathTex(f"[{e[0]}, {e[1]}[@{index - e[0]}", font_size=36, color=intervals_color[k])
                if i==0:
                    t1.next_to(level_tex[k], RIGHT)
                else:
                    t1.next_to(t0, RIGHT)
                t0 = t1
                index += e[1] - e[0]
                self.add(t0)

        self.wait()
