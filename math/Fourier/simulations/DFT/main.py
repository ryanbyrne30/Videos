import pygame
import numpy as np
import cmath 
from display import *
import random
from random import randrange
random.seed(0)
import json
from time import sleep


WIDTH, HEIGHT = 1800, 1000
PI = cmath.pi
SCALE = 250

with open('pi.json', 'r') as f:
    svg = json.load(f)

# POINTS = np.array([ cmath.rect(i/2/cmath.pi, np.random.normal(0, 1)) for i in range(900) ]) * 2
POINTS = np.array([ p[0]+p[1]*1j for p in svg[::4] ]) * 0.4
FOURIER = dft(POINTS)

# colors
BLACK = 0,0,0

screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill(BLACK)
main = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
main.fill(BLACK)
screen.blit(main, (0,0))

#####################################################

path = []
t_timeout = 0.02
t = 0
clock = pygame.time.Clock()
running = True
isPaused = False
dt = cmath.pi*2/len(FOURIER)
while running:
    main.fill(BLACK)

    point = epicycles(main, WIDTH/4+HEIGHT/2*1j, 0, FOURIER, t)
    for p in POINTS:
        pygame.draw.circle(main, (255,0,0), (6*WIDTH/8+p.real, HEIGHT/2 + p.imag), 1)

    for p in path:
        pygame.draw.circle(main, (100, 100, 20), (p.real, p.imag), 2)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            isPaused = True if not isPaused else False 
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            t += dt
            path.insert(0, point)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            t -= dt
            path.pop(0)
        
    if len(path) > len(POINTS) * cmath.pi*2/len(FOURIER) / dt:
        path = []

    if not isPaused:
        t += dt
        path.insert(0, point)
        sleep(t_timeout)
        
    screen.blit(main, (0,0))
    pygame.display.update()
    clock.tick(1000)

pygame.quit()


