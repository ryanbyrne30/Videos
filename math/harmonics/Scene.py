from Surface import Surface
from globals import *
import numpy as np

DELTA_T = 0.001

class Scene(object):
    def __init__(self, width, height, xrange, yrange, color=BLACK):
        self.width = width 
        self.height = height 
        self.xrange = xrange 
        self.yrange = yrange 
        self.color = color
        self.images = []

    def plotParametric(self, funcX, funcY, ts, radius=3, color=PINK, opacity=255, trail=False, trailLength=500):
        images = []
        for t in ts:
            t_span = np.linspace(t-DELTA_T*trailLength, t, trailLength)
            points = list(map(lambda t_: (funcX(t_), funcY(t_)), t_span)) if trail else [t]
            surface = Surface(self.width, self.height, 
                self.xrange, self.yrange, self.color)
            surface.plotPoints(points, color, radius, opacity, trail)
            images.append(surface.im)
        self.images = images 


    def saveGif(self, ofile):
        self.images[0].save(ofile, save_all=True, append_images=self.images[1:], optimize=True, duration=20, loop=0)

        
            

