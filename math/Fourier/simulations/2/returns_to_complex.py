from typing_extensions import runtime
from manim import *
import numpy as np
import cmath
from pandas_datareader import data as pdr
import yfinance as yf
yf.pdr_override()

SAMPLE = 10
FREQ = SAMPLE

def getStockSample(ticker, sampleSize):
    returns = pdr.get_data_yahoo(ticker)['Adj Close'].pct_change()[1:]
    it = int(len(returns) / sampleSize)
    return returns[::it][:sampleSize]



class ShowGraph(Scene):
    def show_graph_returns(self, returns):
        ax = NumberPlane(
            x_range=[0,SAMPLE,1],
            y_range=[-0.05, 0.05, 0.01],
            x_length=10, y_length=6,
            y_axis_config={"include_numbers": True, "line_to_number_buff": -1},
            axis_config={
                "include_tip": False, 
                "tick_size":0.05, 
            },
            background_line_style={
                "stroke_color": DARK_GREY, 
                "stroke_width": 1
            }
        )


        axis_labels = ax.get_axis_labels(x_label="t", y_label="returns")
        
        dots = VGroup()
        lines = VGroup()
        for time, ret in enumerate(returns):
            dot = Dot(ax.c2p(time, ret), stroke_width=0, color=RED, fill_opacity=1, radius=0.1)
            dots.add(dot)

            if time > 0:
                line = Line(start=dots[time-1], end=dots[time], color=RED)
                lines.add(line)

        returns_graph = VGroup(ax, dots, lines, axis_labels)

        self.play(Create(ax), Write(axis_labels))
        self.play(Create(dots))
        self.play(Create(lines))
        self.wait(2)
        self.play(returns_graph.animate.shift(RIGHT*3).scale(0.5))

        return dots, returns_graph, ax



    def show_graph_returns_complex(self, returns, dots, returns_plane):
        returns_complex = [ ret * cmath.exp(-1j*2*cmath.pi*i/FREQ) for i, ret in enumerate(returns) ]

        complexPlane = ComplexPlane(
            x_range=[-0.05, 0.05, 0.01],
            y_range=[-0.05, 0.05, 0.01],
            x_length=10, y_length=10,
            axis_config={
                "include_tip": False,
                "tick_size": 0.05,
            },
            background_line_style={
                "stroke_color": DARK_GREY, 
                "stroke_width": 1
            }
        ).add_coordinates().shift(LEFT*3).scale(0.5)
        self.play(Create(complexPlane))

        cdots = VGroup()
        clines = VGroup()
        runtime = 1
        scale = 1.5
        ccenter = complexPlane.n2p(0+0*1j)
        for i, c in enumerate(returns_complex):
            cdot = Dot(complexPlane.n2p(c), color=YELLOW, radius=0.05*scale)
            cdots.add(cdot)
            
            if i > 0:
                cline = Line(cdots[i-1], cdot, color=RED)
                clines.add(cline)

            dotLine = DashedLine(returns_plane.c2p(i, 0), dots[i], color=PINK)
            arrow = Arrow(start=ccenter, end=cdot, buff=0, color=PINK)

            dottedLine = DashedLine(start=complexPlane.n2p(-1*c), end=cdot, buff=0, color=PINK)
            
            if i > 2:
                runtime = 0.25
            self.play(Create(dotLine), Create(dottedLine), run_time=runtime)
            self.play(Create(arrow), run_time=runtime)
            self.play(dots[i].animate.set_color(YELLOW).scale(scale), Create(cdot), run_time=runtime)
            self.play(dots[i].animate.set_color(RED).scale(1/scale), cdot.animate.set_color(RED).scale(1/scale), run_time=runtime)
            self.remove(arrow, dotLine, dottedLine)
        
        self.play(Create(clines))

        return complexPlane



    def construct(self):
        returns = getStockSample("MSFT", SAMPLE)
        dots, returns_graph, returns_plane = self.show_graph_returns(returns)
        returns_complex_graph = self.show_graph_returns_complex(returns, dots, returns_plane)

        
        self.wait(2)



