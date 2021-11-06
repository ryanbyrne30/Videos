from typing_extensions import runtime
from manim import *
import numpy as np
import cmath
import random
from pandas_datareader import data as pdr
import yfinance as yf
yf.pdr_override()

POINTS = 11
FREQ = 1 / 7

def rectToComplex(ys, freq):
    return [ y * cmath.exp(-1j*2*cmath.pi*i*freq) for i, y in enumerate(ys) ]


class Fseries(Scene):
    def show_complex_plane(self):
        cplane = ComplexPlane(
            x_range=[-1, 1, 0.25],
            y_range=[-1, 1, 0.25],
            x_length=5, y_length=5,
            axis_config={
                "include_tip": False, 
                "font_size": 18
            },
            background_line_style={
                "stroke_color": DARK_GREY, 
                "stroke_width": 1
            }
        ).add_coordinates()

        self.play(Create(cplane))
        self.wait(1)
        return cplane

    def plotCns(self, cns, cplane):
        dots = VGroup()
        for cn in cns:
            dot = Dot(cplane.n2p(cn), radius=0.05)
            dots.add(dot)
        self.play(Create(dots))

    def genSeries(self, cns):
        return [
            lambda t: cns[i]*cmath.exp(2j*cmath.pi*i*t)
            for i in range(-int(len(cns)/2), int(len(cns)/2)+1)
        ]


    def construct(self):
        ys = [ random.random() for _ in range(POINTS) ]
        cns = rectToComplex(ys[:2], FREQ)
        # cns_freq = list(range(-int(len(ys)/2), int(len(ys)/2)+1))
        print("Ys:", len(ys), "CNs:", len(cns))
        cplane = self.show_complex_plane()

        self.plotCns(cns, cplane)

        

        series = self.genSeries(cns)
        zeroth = int(len(series)/2) + 1

        cplane_center = cplane.n2p(0)
        print(cplane_center)


        for i, cn in enumerate(cns):
            if i > 0:
                circ = Circle(np.linalg.norm(cplane.n2p(cn-cns[i-1])), color=RED)
                prev_vec = cplane.n2p(cns[i-1])
                circ.set_x(prev_vec[0])
                circ.set_y(prev_vec[1])
                arrow = Arrow(start=prev_vec, end=cplane.n2p(cn), buff=0, max_stroke_width_to_length_ratio=3, max_tip_length_to_length_ratio=0.15)
            else:
                circ = Circle(np.linalg.norm(cplane.n2p(cn)), color=RED)
                arrow = Arrow(start=cplane_center, end=cplane.n2p(cn), buff=0, max_stroke_width_to_length_ratio=3, max_tip_length_to_length_ratio=0.15)

            group1 = VGroup(circ, arrow)
            self.play(Create(group1))




        # dots = VGroup()
        # for t in np.arange(0, 1, 0.01):
        #     dot = Dot(cplane.n2p(series[zeroth](t)), radius=0.05, color=RED)
        #     dots.add(dot)

        # self.play(Create(dots))


        # self.play(cplane.animate.apply_complex_function(lambda t: cmath.exp(t*1j)))



        

        




