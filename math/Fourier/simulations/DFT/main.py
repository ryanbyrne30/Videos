import pygame
import numpy as np
import cmath 
from display import *

WIDTH, HEIGHT = 1800, 1000
PI = cmath.pi

SINE_FREQS = [ 1, 3, 5, 7 ]
COS_FREQS = [ 2, 2, 3, 4 ]
SINE_RADS = np.array([ 4/PI, 4/(3*PI), 4/(5*PI), 4/(7*PI) ]) * 30
COS_RADS = np.array([ 4/PI, 4/(3*PI), 4/(5*PI), 4/(7*PI) ]) * 30

# colors
BLACK = 0,0,0

screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill(BLACK)

#####################################################


path = []

t = 0
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            isPaused = True if not isPaused else False 
    screen.fill(BLACK)

    circSine_center = drawEpicenter(screen, (WIDTH/8, HEIGHT/2), SINE_RADS[0], SINE_FREQS[0], t)
    circCos_center = drawEpicenter(screen, (WIDTH/2, HEIGHT/8), COS_RADS[0], COS_FREQS[0], t)
    for i in range(1, len(SINE_FREQS)):
        circCos_center = drawEpicenter(screen, circCos_center, SINE_RADS[i], SINE_FREQS[i], t)
        circSine_center = drawEpicenter(screen, circSine_center, SINE_RADS[i], SINE_FREQS[i], t)

    pathStart = WIDTH/2, HEIGHT/2
    point = circCos_center[0], circSine_center[1]
    path.insert(0, point)
    for x, y in path:
        pygame.draw.circle(screen, (100, 100, 20), (x, y), 2)
    pygame.draw.line(screen, (255,255,255), circSine_center, point)
    pygame.draw.line(screen, (255,255,255), circCos_center, point)

    path = path[:int(WIDTH/2)]
    t += 0.01
    pygame.display.update()
    clock.tick(100)

pygame.quit()


