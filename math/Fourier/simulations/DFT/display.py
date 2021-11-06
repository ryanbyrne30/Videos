import cmath
import pygame
import numpy as np

def drawEpicenter(screen, center, radius, freq, phase, t):
    surface = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
    circ_center = radius, radius
    pygame.draw.circle(surface, (255,255,255, 15), circ_center, radius, 0)
    c = cmath.rect(radius, (t*freq)+phase)
    point = c.real+radius, -c.imag+radius 
    pygame.draw.line(surface, (255, 255, 255, 100), circ_center, point)

    screen.blit(surface, (center[0]-radius, center[1]-radius))

    return point[0]+center[0]-radius, point[1]+center[1]-radius

def dft(cpoints):
    X = []
    N = len(cpoints)
    for k in range(N):
        sum = 0
        for n in range(N):
            sum += cpoints[n] * cmath.exp(-2j*cmath.pi*k*n/N)

        avg = sum / N
        freq = k 
        amp = np.linalg.norm(avg)
        phase = np.arctan(avg.imag/avg.real)

        X.append([avg, freq, amp, phase])
    return X

# def drawEpicenter(screen, center, freq, amp, phase, t):
#     surface = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
#     circ_center = radius, radius
#     pygame.draw.circle(surface, (255,255,255, 15), circ_center, radius, 0)
    
#     c = cmath.rect(radius, t*freq)
#     point = c.real+radius, -c.imag+radius 
#     pygame.draw.line(surface, (255, 255, 255, 100), circ_center, point)

#     screen.blit(surface, (center[0]-radius, center[1]-radius))

#     return point[0]+center[0]-radius, point[1]+center[1]-radius