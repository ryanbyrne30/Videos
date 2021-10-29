import matplotlib
import matplotlib.pyplot as plt
import matplotlib.backends.backend_agg as agg
import pygame
import random 
from time import time
import pylab
pygame.init()
matplotlib.use("Agg")
# random.seed(0)

precision = 100
size = width, height = 1600, 800
unit = 300
black = 0,0,0
squareColor = 255, 255, 255
circleColor = (0, 0, 255, 25)
dotGoodColor = (0, 255, 0)
dotBadColor = 255, 0, 0
dotRadius = 3.5
bg = 192, 192, 192
plotRenderTime = 1
plotSaveTime = 0.1

screen = pygame.display.set_mode(size)

def renderBase(screen):
    screen.fill(bg)
    squareSize = sWidth, sHeight = 2*unit, 2*unit
    square = pygame.Surface(squareSize)
    square.fill(squareColor)
    circle = pygame.Surface(squareSize, pygame.SRCALPHA)
    pygame.draw.circle(
        circle, 
        circleColor,
        (sWidth/2, sHeight/2),
        unit
    )
    screen.blit(square, (width/4 - sWidth/2, height/2 - sHeight/2))
    screen.blit(circle, (width/4 - sWidth/2, height/2 - sHeight/2))

def randomPoint(xmin, xmax, ymin, ymax):
    x = random.randrange(xmin, xmax*precision)
    y = random.randrange(ymin, ymax*precision)
    return x/precision, y/precision

def renderRandomPoint(screen):
    isGoodPoint = 0
    squareSize = sWidth, sHeight = 2*unit, 2*unit
    x, y = randomPoint(0, sWidth, 0, sHeight)
    rad = pow(x-sWidth/2, 2) + pow(y-sHeight/2, 2)
    if rad <= pow(unit, 2):
        color = dotGoodColor
        isGoodPoint = 1
    else:
        color = dotBadColor
    dot = pygame.Surface(squareSize, pygame.SRCALPHA)
    pygame.draw.circle(
        dot,
        color,
        (x, y),
        dotRadius
    )
    screen.blit(dot, (width/4 - sWidth/2, height/2 - sHeight/2))
    return isGoodPoint

def showPlot(values, screen):
    fig = pylab.figure(figsize=(8,8))
    ax = fig.gca()
    ax.plot(values)
    canvas = agg.FigureCanvasAgg(fig)
    canvas.draw()
    renderer = canvas.get_renderer()
    raw_data = renderer.tostring_rgb()
    size = canvas.get_width_height()
    surf = pygame.image.fromstring(raw_data, size, 'RGB')
    screen.blit(surf, (width/2, 0))
    pygame.display.flip()

renderBase(screen)

clock = pygame.time.Clock()
running = True
stop = False
count = 0
inCircle = 0
piVals = []
plotRenderTimeStart = time()
plotSaveTimeStart = time()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                print("Space bar hit")
                stop = True if not stop else False 
    if not stop:
        count += 1 
        inCircle += renderRandomPoint(screen)
        pi = inCircle/count*4
        pi_str = "{:10.6f}".format(pi)
        if time() - plotSaveTimeStart >= plotSaveTime:
            piVals.append(pi)
            plotSaveTimeStart = time()
        if time() - plotRenderTimeStart >= plotRenderTime:
            showPlot(piVals, screen)
            plotRenderTimeStart = time()
        pygame.display.set_caption(f'{inCircle}/{count} in circle - PI ~ {pi_str}')
    pygame.display.update()
    clock.tick(1000)

pygame.quit()
quit()
