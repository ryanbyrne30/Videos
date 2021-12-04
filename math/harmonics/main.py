from PIL import Image, ImageDraw
import numpy as np
from LorenzAttractor import LorenzAttractor
from anim import *
import random





width = 800
height = 800
xrange = [-30, 30]
yrange = [-30, 30]

scene = LorenzAttractor(width, height, xrange, yrange)
# scene.graph((1, 7, 4), trailLength=100, t_start=20, t_end=24, t_step=0.0005, frame_skip=40)
scene.graphRandomParticles(30, t_start=20, trailLength=200, t_end=26, t_step=0.001, frame_skip=40, color=None, radii_max=1.5, radii_min=1)
scene.saveGif('gifs/lorenz2.gif')
