import pygame
import numpy as np
import cmath 
from display import *
from random import randrange

WIDTH, HEIGHT = 1800, 1000
PI = cmath.pi
SCALE = 250

# POINTS = [ randrange(0, SCALE)+randrange(0, SCALE)*1j for _ in range(4) ]
POINTS = [ i+i*1j for i in range(0, 150, 10) ]
FOURIER = dft(POINTS)

print(FOURIER)

# colors
BLACK = 0,0,0

screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill(BLACK)

#####################################################


path = []

t = 0
clock = pygame.time.Clock()
running = True
isPaused = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            isPaused = True if not isPaused else False 
    screen.fill(BLACK)

    for p in POINTS:
        pygame.draw.circle(screen, (255,0,0), (WIDTH/2+p.real, HEIGHT/2-p.imag), 4)
        pygame.draw.circle(screen, (255,0,0), (WIDTH/8, HEIGHT/2-p.imag), 4)
        pygame.draw.circle(screen, (255,0,0), (WIDTH/2+p.real, HEIGHT/8), 4)

    # circCos_center = drawEpicenter(screen, (WIDTH/2, HEIGHT/8), FOURIER[0][2], FOURIER[0][1], FOURIER[0][3], t)
    circSine_center = drawEpicenter(screen, (WIDTH/8, HEIGHT/2), FOURIER[0][2], FOURIER[0][1], FOURIER[0][3], t)
    for avg, freq, amp, phase in FOURIER[1:]:
        # circCos_center = drawEpicenter(screen, circCos_center, amp, freq, phase, t)
        circSine_center = drawEpicenter(screen, circSine_center, amp, freq, phase, t)

    pathStart = WIDTH/2, HEIGHT/2
    # point = circCos_center[0], circSine_center[1]
    point = WIDTH/2, circSine_center[1]
    path.insert(0, point)
    for i in range(len(path)):
    # for x, y in path:
        pygame.draw.circle(screen, (100, 100, 20), (WIDTH/2+i, path[i][1]), 2)
        # pygame.draw.circle(screen, (100, 100, 20), x, y), 2)
    pygame.draw.line(screen, (255,255,255), circSine_center, point)
    # pygame.draw.line(screen, (255,255,255), circCos_center, point)

    path = path[:int(WIDTH/2)]

    # dt = cmath.pi*2/len(FOURIER)
    # t += dt / 2
    t += 0.01
    pygame.display.update()
    clock.tick(100)

pygame.quit()


