import pygame
import cmath
import numpy as np

from bg import harmonic, renderBg, renderCompGrids, renderPointsOnCSSurface, renderPointsOnMSSurface, renderPointsOnSSSurface, renderSurfaces
import config

# Display sine and cosine graphs - SLOW
screen = pygame.display.set_mode(config.ScreenSize)
MSSurface = pygame.Surface(config.MSSize)
CSSurface = pygame.Surface(config.CSSize)
SSSurface = pygame.Surface(config.SSSize)
clock = pygame.time.Clock()




points = []
time = 0

running = True 

renderBg(screen, MSSurface, CSSurface, SSSurface)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 
    
    harmonics = np.array(list(map(lambda n: harmonic(n, time), config.series)))
    x = harmonics[:,0].sum()
    y = harmonics[:,1].sum()
    points.append((x,y))
    points = points[-config.tail:]
    if config.RENDER_ALL:
        renderBg(screen, MSSurface, CSSurface, SSSurface)
        renderPointsOnCSSurface(points, CSSurface)
        renderPointsOnSSSurface(points, SSSurface)
    renderPointsOnMSSurface(points, MSSurface, config.MSWidth, config.MSHeight,
        config.MSXTick, config.MSYTick, config.MSSize)
    renderSurfaces(screen, MSSurface, CSSurface, SSSurface)
    
    time += 0.007
    pygame.display.update()
    clock.tick(5000)

pygame.quit()
quit()
