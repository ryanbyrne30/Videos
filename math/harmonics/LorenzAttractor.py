from anim import *
import numpy as np
from scipy.integrate import odeint
import random

class LorenzAttractor(Scene):
    def __init__(self, width, height, xrange, yrange, color=BLACK, 
            sigma=10, rho=28, beta=8/3):
        super().__init__(width, height, xrange, yrange, color)
        self.sigma = sigma 
        self.rho = rho
        self.beta = beta

    def deltaX(self, x, y, sigma):
        return sigma*y - sigma*x

    def deltaY(self, x, y, z, rho):
        return rho*x - x*z - y 

    def deltaZ(self, x, y, z, beta):
        return x*y - beta*z

    def nextPoint(self, state, t):
        x, y, z = state
        x1 = self.deltaX(x, y, self.sigma)
        y1 = self.deltaY(x, y, z, self.rho)
        z1 = self.deltaZ(x, y, z, self.beta)
        return x1, y1, z1

    def graph(self, state0, t_end=40, t_step=0.01, t_start=0, trailLength=100, frame_skip=40, radius=2, color=PINK, opacity=255):
        self.graphFunction(self.nextPoint, state0, t_end, t_step, t_start, trailLength, frame_skip, radius, color, opacity)

    def graphRandomParticles(self, particles, t_end=40, t_step=0.01, t_start=0, 
            trailLength=100, frame_skip=40, radii_min=0.5, radii_max=1.75, color=None, 
            opacity=255):
        self.graphFunctionWithRandomParticles(self.nextPoint, particles, t_end, t_step, t_start, 
            trailLength, frame_skip, radii_min, radii_max, color, 
            opacity)

    def saveGif(self, ofile):
        return super().saveGif(ofile)
