import cmath
import pygame

def drawEpicenter(screen, center, radius, freq, t):
    surface = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
    circ_center = radius, radius
    pygame.draw.circle(surface, (255,255,255, 15), circ_center, radius, 0)
    
    c = cmath.rect(radius, t*freq)
    point = c.real+radius, -c.imag+radius 
    pygame.draw.line(surface, (255, 255, 255, 100), circ_center, point)

    screen.blit(surface, (center[0]-radius, center[1]-radius))

    return point[0]+center[0]-radius, point[1]+center[1]-radius
