import numpy as np
from manim import *
from interval import *

config.background_color = "#ffffff"
# config.background_color = "#000000"

center = [2, 3, 0]

stroke_width = 5
default_color = "#000001"

intervals_color = ["#f98a00", "#009a8e", "#750013"]

intervals = {
    0: [[0, 2], [5, 6]],
    1: [[4, 5], [6, 8], [9, 10]],
    2: [[10, 12], [16, 18]],
}

class mesh(MovingCameraScene):
    def construct(self):
        stroke_color = BLACK
        self.camera.frame_center = [2, 3, 0]
        self.camera.frame_width = 11
        self.camera.focal_distance = 50

        mesh = []
        colors = []
        levels = []

        for k, v in intervals.items():
            mesh.append(VGroup())
            colors.append(intervals_color[k])
            levels.append(k)
            for i in v:
                mesh[-1].add(Interval(k, range=i,  stroke_width=stroke_width, color=default_color))

        self.play(*[Create(m) for m in mesh])#, run_time=2)

        self.play(*[m.animate.set_color(c) for m, c in zip(mesh, colors)])#, run_time=3)

        level_axe = NumberLine(x_range=[0, 3], unit_size=2, include_tip=True, tip_length=0.1, rotation=90*DEGREES, label_direction=LEFT, color=default_color)
        level_axe.add_numbers(font_size=34, color=default_color)
        level_axe.shift(LEFT + 3*UP)

        level_label = Text("level", font_size=20, color=default_color)
        level_label.next_to(level_axe, LEFT)

        axe = VGroup(level_axe, level_label)

        self.play(*[m.animate.shift(2*l*UP) for m, l in zip(mesh, levels)],
                  Create(axe)
        )

        self.play(*[m.animate.add_cell_numbers(font_size=24, color=default_color) for me in mesh for m in me])

        self.camera.frame.save_state()

        unit_mesh = [Interval(l, range=[0, 1], stroke_width=stroke_width, color=c) for m, l, c in zip(mesh, levels, colors)]
        [m.shift(l*UP) for m, l in zip(unit_mesh, levels)]

        ug = VGroup(*unit_mesh)
        g = VGroup(*mesh)
        g.save_state()
        self.play(axe.animate.set_opacity(0),
                  Transform(g, ug),
                  self.camera.frame.animate.scale(0.5).move_to(ug)
        )

        self.wait(1)

        self.play(axe.animate.set_opacity(1),
                  Restore(g),
                  Restore(self.camera.frame))

        self.wait()