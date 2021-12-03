from PIL import Image, ImageDraw
from anim.Point import Point
from anim.globals import *

class Surface(object):
    def __init__(self, width, height, xrange, yrange, color=BLACK, opacity=255):
        # constants
        self.width = width
        self.height = height
        self.xrange = xrange 
        self.yrange = yrange
        self.color = color
        self.centerUnit = (xrange[1]+xrange[0])/2, (yrange[1]+yrange[0])/2
        self.center = width//2, height//2
        self.ppu = width/(xrange[1]-xrange[0]), height/(yrange[1]-yrange[0])
        self.surface = Image.new('RGBA', (width, height), color+(opacity,))
        self.tsurface = Image.new('RGBA', (width, height), (0,0,0,0))
        self.draw = ImageDraw.Draw(self.tsurface)

        # variables
        self.points = []

    def addPoint(self, x, y, color=PINK, opacity=255, radius=2):
        self.points.append(Point(x, y, color, opacity, radius))

    def __renderPoint(self, point):
        renderX = (point.x - self.centerUnit[0]) * self.ppu[0] + self.center[0]
        renderY = (point.y - self.centerUnit[1]) * self.ppu[1] + self.center[1]
        return renderX, renderY

    def renderPoints(self):
        for p in self.points:
            rX, rY = self.__renderPoint(p)
            self.draw.ellipse(
                (rX-p.radius, rY-p.radius, rX+p.radius, rY+p.radius),
                p.color+(p.opacity,)
            )
        self.surface = Image.alpha_composite(self.surface, self.tsurface)

    
    
