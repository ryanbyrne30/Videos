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
# scene.graph((1, 7, 4), trailLength=100, t_step=0.01, frame_skip=10)
scene.graphRandomParticles(10, t_start=20, trailLength=10, t_end=26, t_step=0.002, frame_skip=40, color=None, radii_max=3, radii_min=0.75)
scene.saveGif('gifs/lorenz.gif')
