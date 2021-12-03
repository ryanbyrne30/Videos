from PIL import Image, ImageDraw
from globals import *

class Surface(object):
    def __init__(self, width, height, xrange, yrange, color=BLACK):
        # constants
        self.width = width
        self.height = height
        self.xrange = xrange 
        self.yrange = yrange

        # variables
        self.centerUnit = (xrange[1]+xrange[0])/2, (yrange[1]+yrange[0])/2
        self.center = width//2, height//2
        self.ppu = width/(xrange[1]-xrange[0]), height/(yrange[1]-yrange[0])
        self.im = Image.new('RGBA', (width, height), color)
        self.draw = ImageDraw.Draw(self.im)
        self.surface = Image.new('RGBA', (self.width, self.height), (0,0,0,0))

    def plot(self, x, y, color=PINK, radius=3, opacity=255):
        self.__plotHelper([(x, y)], color, radius, opacity, trail=False)

    def plotPoints(self, points, color=PINK, radius=3, opacity=255, trail=False):
        self.__plotHelper(points, color, radius, opacity, trail)

    def __plotHelper(self, points, color, radius, opacity, trail):
        # surface = Image.new('RGBA', (self.width, self.height), (0,0,0,0))
        opacities = [ int(i/len(points)*255) if trail else opacity for i in range(len(points)) ]
        for i in range(len(points)):
            point = points[i]
            px = (point[0] - self.centerUnit[0]) * self.ppu[0] + self.center[0]
            py = (point[1] - self.centerUnit[1]) * self.ppu[1] + self.center[1]
            draw = ImageDraw.Draw(self.surface)
            draw.ellipse((px-radius, py-radius, px+radius, py+radius), color+(opacities[i],))
        # self.im = Image.alpha_composite(self.im, surface)
    
    def renderPoints(self):
        self.im = Image.alpha_composite(self.im, self.surface)
