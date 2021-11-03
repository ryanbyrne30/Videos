import pygame
import numpy as np
import cmath

FOURIER_SERIES = [
    (lambda t: cmath.cos(t), lambda t: cmath.sin(t))
]

trail = 30
trailSpace = 2
dotsize = 5

size = width, height = 800, 800
center = width/2, height/2
bg = 0, 0, 0
gridColor = 25, 25, 25
speed = 1
xaxis = (-5, 5)
yaxis = (-5, 5)
xtick = int(width / (xaxis[1]-xaxis[0]))
ytick = int(height / (yaxis[1]-yaxis[0]))

screen = pygame.display.set_mode(size)

def renderGrid():
    for x in range(0, width, xtick):
        for y in range(0, height, ytick):
            rect = pygame.Rect(x, y, xtick, ytick)
            pygame.draw.rect(screen, gridColor, rect, 1) 

def render():
    screen.fill(bg)
    renderGrid()

def mapFunToScreen(originX, originY, funs, t):
    funX, funY = funs
    x = funX(t).real
    y = funY(t).real
    return originX+x*xtick, originY-y*ytick


def plotFourierSeries(t):
    for fun in FOURIER_SERIES:
        x, y = mapFunToScreen(center[0], center[1], fun, t)
        pygame.draw.circle(screen, (255, 0, 0), (x, y), 5)


dots = []
screen.fill(bg)
clock = pygame.time.Clock()
time = 0
count = 0
running = True 
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 
    render()
    
    newDot = mapFunToScreen(center[0], center[1], FOURIER_SERIES[0], time)
    dots = dots[-trail:]
    for i in range(len(dots)):
        circle = pygame.Surface(size, pygame.SRCALPHA)
        pygame.draw.circle(
            circle, 
            (255, 0, 0, i/len(dots)*200),
            dots[i],
            dotsize
        )
        screen.blit(circle, (0,0))

    pygame.draw.circle(
            screen, 
            (255, 0, 0),
            newDot,
            dotsize
        )

    if count >= trailSpace:
        dots.append(newDot)
        count = 0

    time += 0.00001
    count += 1
    pygame.display.update()
    clock.tick(100)

pygame.quit()
quit()