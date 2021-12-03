from PIL import Image, ImageDraw
import numpy as np
from LorenzAttractor import LorenzAttractor
from Surface import Surface
from Scene import Scene
import random
from globals import *

images = []
points = []

width = 800
height = 800
center = width // 2
white = (255, 255, 255)
radius = 2
fps = 500
duration = 3
frames = duration * fps

xrange = -25, 25
yrange = -25, 25

def funX(t):
    return np.cos(t*2*PI)+np.cos(8*t*PI)

def funY(t):
    return np.sin(t*2*PI)+np.sin(8*t*PI)

# ts = [ 2*i/frames for i in range(frames) ]
# scene = Scene(width, height, xrange, yrange)
# scene.plotParametric(funX, funY, ts, trail=True)
scene = LorenzAttractor(width, height, xrange, yrange)
scene.plot2d(1, 1, 1, 10, 28, 8/3, 10)
scene.saveGif('temp.gif')