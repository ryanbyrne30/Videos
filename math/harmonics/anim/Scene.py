from scipy.integrate.odepack import odeint
from anim.Surface import Surface
from anim.globals import *
import numpy as np
import random
from PIL import Image, ImageDraw
import time

DELTA_T = 0.001

class Scene(object):
    def __init__(self, width, height, xrange, yrange, color=BLACK):
        # constants
        self.width = width 
        self.height = height 
        self.xrange = xrange 
        self.yrange = yrange 
        self.color = color

        # variables
        self.images = []

    def graphFunction(self, fun, state0, t_end=40, t_step=0.01, t_start=0, 
            trailLength=100, frame_skip=40, radius=2, color=PINK, opacity=255): 
        """
        fun: function(state, t)
        state0: initial state
        t_end: time end
        t_step: interval length for each step between t_start and t_end
        t_start: time start
        trail: 0-continuous, >0-trail length
        radius: radius of point
        color: color of graph
        frame_skip: number of frames to skip for each frame render
        """
        startTime = time.time()
        t = np.arange(t_start, t_end, t_step)
        states = odeint(fun, state0, t)

        for i in range(0, len(states), frame_skip):
            i0 = i-trailLength if trailLength>0 and i-trailLength>0 else 0
            surface = Surface(self.width, self.height, self.xrange, self.yrange, self.color, 0)
            trail = states[i0:i]
            for j in range(len(trail)):
                state = trail[j]
                p_opacity = int(j/len(trail)*255) if trailLength>0 else opacity
                surface.addPoint(state[0], state[1], color, p_opacity, radius)
            surface.renderPoints()
            self.images.append(surface.surface)
        print(f"Rendered graph. {len(self.images)} frames [{round(time.time()-startTime, 4)}s]")

    def __getPrecision(self, num):
        num_str = str(num)
        return num_str[::-1].find('.')

    def __combineFrameGroup(self, frameGroup):
        frame = frameGroup[0]
        for i in range(1, len(frameGroup)):
            frame = Image.alpha_composite(frame, frameGroup[i])
        return frame

    def graphFunctionWithRandomParticles(self, fun, particles, t_end=40, t_step=0.01, t_start=0, 
            trailLength=100, frame_skip=40, radii_min=0.5, radii_max=1.75, color=None, 
            opacity=255): 
        """
        fun: function(state, t)
        state0: initial state
        t_end: time end
        t_step: interval length for each step between t_start and t_end
        t_start: time start
        trail: 0-continuous, >0-trail length
        radius: radius of point
        color: color of graph
        frame_skip: number of frames to skip for each frame render
        """
        radii_precision = max(self.__getPrecision(radii_min), self.__getPrecision(radii_max))
        particle_imageGroups = []
        for i in range(particles):
            print(f"Creating graph for particle {i}")
            p_color = (random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255)) if color is None else color
            radius = random.randrange(radii_min*pow(10, radii_precision), radii_max*pow(10, radii_precision)) / pow(10, radii_precision)
            state0 = random.random()*10, random.random()*10, random.random()*10
            self.graphFunction(fun, state0, t_end, t_step, t_start, trailLength, frame_skip, radius, p_color, opacity)
            particle_imageGroups.append(self.images.copy())
            self.images = []
        
        print("Rendering all graphs...")
        startTime = time.time()
        particle_frameGroups = list(zip(*particle_imageGroups))
        self.images = list(map(self.__combineFrameGroup, particle_frameGroups))
        print(f"Finished full render [{round(time.time()-startTime, 4)}s]")


    def saveGif(self, ofile):
        print("Saving gif...")
        startTime = time.time()
        self.images[0].save(ofile, save_all=True, append_images=self.images[1:], optimize=True, duration=20, loop=0)
        print(f"Finished saving [{round(time.time()-startTime, 4)}s]")

        
            

