from Scene import Scene
from Surface import Surface
from globals import *
import numpy as np
from scipy.integrate import odeint
import random

class LorenzAttractor(Scene):
    def __init__(self, width, height, xrange, yrange, color=BLACK):
        super().__init__(width, height, xrange, yrange, color)
        self.sigma = None 
        self.rho = None 
        self.beta = None

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

    def plot2d(self, x0, y0, z0, sigma, rho, beta, frames, trailLength=1000):
        self.sigma = sigma 
        self.rho = rho 
        self.beta = beta

        start = 0.0
        end = 40.0
        iter = 0.001
        frame_skip = 40
        t = np.arange(start, end, iter)
        print("Num frames:", (end-start)/iter/frame_skip)
        particles = 20
        max_pos = 20

        radii = [
            random.randrange(1, 4) / 2
            for _ in range(particles)
        ]
        colors = [
            (random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255))
            for _ in range(particles)
        ]
        all_states = [ 
            odeint(self.nextPoint, 
                (random.random()*max_pos, random.random()*max_pos, random.random()*max_pos), 
                t)
            for _ in range(particles)
        ]

        for i in range(0, len(all_states[0]), frame_skip):
            i_start = i-trailLength if i-trailLength > 0 else 0
            surface = Surface(self.width, self.height, self.xrange, self.yrange)
            for j in range(particles):
                state = all_states[j]
                trail = state[i_start: i]
                points = [ (t[0], t[1]) for t in trail ]
                surface.plotPoints(points, radius=radii[j], trail=True, color=colors[j])
            surface.renderPoints()
            self.images.append(surface.im)


        # states = odeint(self.nextPoint, state0, t)
        # states2 = odeint(self.nextPoint, (0.5, 1.5, 2), t)
        # states3 = odeint(self.nextPoint, (1, 3, 1.75), t)
        # states4 = odeint(self.nextPoint, (7, 4, 0.5), t)

        # for i in range(0, len(states), 40):
        #     i_start = i-trailLength if i-trailLength > 0 else 0
        #     trail = states[i_start: i]
        #     trail2 = states2[i_start: i]
        #     trail3 = states3[i_start: i]
        #     trail4 = states4[i_start: i]
        #     points = [ (t[0], t[1]) for t in trail ]
        #     points2 = [ (t[0], t[1]) for t in trail2 ]
        #     points3 = [ (t[0], t[1]) for t in trail3 ]
        #     points4 = [ (t[0], t[1]) for t in trail4 ]
        #     surface = Surface(self.width, self.height, self.xrange, self.yrange)
        #     surface.plotPoints(points, radius=1, trail=True)
        #     surface.plotPoints(points2, radius=1, trail=True)
        #     surface.plotPoints(points3, radius=1, trail=True)
        #     surface.plotPoints(points4, radius=1, trail=True)
        #     surface.renderPoints()
        #     self.images.append(surface.im)

