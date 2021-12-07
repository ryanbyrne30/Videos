import os
from scipy.integrate.odepack import odeint
from anim import Surface, config
from anim.globals import *
import numpy as np
import random
from PIL import Image, ImageDraw
import time
import shutil
import cv2
import imageio

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
        self.partials = []

    def __createFolderIfNotExist(self, path):
        if not os.path.exists(path):
            os.makedirs(path)

    def __partialPath(self, num):
        path = f"{config.partialsDir}/partial{num}"
        self.__createFolderIfNotExist(path)
        return path

    def graphFunction(self, fun, state0, t_end=40, t_step=0.01, t_start=0, 
            trailLength=100, frame_skip=40, radius=2, color=PINK, opacity=255,
            partialNumber=0): 
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
        print("Rendering graph...")
        startTime = time.time()
        t = np.arange(t_start, t_end, t_step)
        states = odeint(fun, state0, t)

        partialFolder = self.__partialPath(partialNumber)
        for i in range(0, len(states), frame_skip):
            i0 = i-trailLength if trailLength>0 and i-trailLength>0 else 0
            surface = Surface(self.width, self.height, self.xrange, self.yrange, self.color, 0)
            trail = states[i0:i]
            for j in range(len(trail)):
                state = trail[j]
                p_opacity = int(j/len(trail)*255) if trailLength>0 else opacity
                surface.addPoint(state[0], state[1], color, p_opacity, radius)
            surface.renderPoints()
            padding = "".join([ "0" for _ in range(config.partialImageNameLength-len(str(i))) ])
            surface.surface.save(f"{partialFolder}/{padding}{i}.png")
        self.partials.append(partialNumber)
        print(f"Rendered graph. {len(states)//frame_skip} frames [{round(time.time()-startTime, 4)}s]")

    def __getPrecision(self, num):
        num_str = str(num)
        return num_str[::-1].find('.')

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
        for i in range(particles):
            print(f"Creating graph for particle {i}")
            p_color = (random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255)) if color is None else color
            radius = random.randrange(radii_min*pow(10, radii_precision), radii_max*pow(10, radii_precision)) / pow(10, radii_precision)
            state0 = random.random()*10, random.random()*10, random.random()*10
            self.graphFunction(fun, state0, t_end, t_step, t_start, trailLength, frame_skip, radius, p_color, opacity, i)

    def __overlapPngs(self, ims1, ims2):
        for i in range(len(ims1)):
            ims1[i] = Image.alpha_composite(ims1[i], ims2[i])
        return ims1


    def __partialImages(self, partialPath):
        impaths = sorted([ partialPath+"/"+impath for impath in os.listdir(partialPath) ])
        return list([ 
            Image.open(ip).convert('RGBA')
            for ip in impaths
        ])


    def saveGif(self, ofile):
        print("Saving gif...")
        print("Partials:", self.partials)
        startTime = time.time()
        
        paths = [ self.__partialPath(self.partials[n]) for n in self.partials ]
        result = self.__partialImages(paths[0])
        print("Total frames:", len(result))

        for i in range(1, len(paths)):
            ims = self.__partialImages(paths[i])
            result = self.__overlapPngs(result, ims)

        result[0].save(ofile, save_all=True, append_images=result[1:], optimize=False, duration=50, loop=0)
        for p in paths:
            shutil.rmtree(p)
        print(f"Finished saving [{round(time.time()-startTime, 4)}s]")
        print("Cleaning up...")
        print("Done")

        
            

