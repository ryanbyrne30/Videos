from anim.globals import *

class Point(object):
    def __init__(self, x, y, color=PINK, opacity=255, radius=2):
        self.x = x
        self.y = -y # flip y axis 
        self.color = color 
        self.opacity = opacity
        self.radius = radius