import pygame
import cmath
import numpy as np

from bg import harmonic, renderBg, renderPointsOnCSSurface, renderPointsOnMSSurface, renderPointsOnSSSurface, renderSurfaces
import config




def run(series=None, speed=1000):
    if not series is None:
        config.series = series

    screen = pygame.display.set_mode(config.ScreenSize)
    MSSurface = pygame.Surface(config.MSSize)
    CSSurface = pygame.Surface(config.CSSize)
    SSSurface = pygame.Surface(config.SSSize)
    clock = pygame.time.Clock()

    points = []
    time = 0
    running = True 
    isPaused = False

    renderBg(screen, MSSurface, CSSurface, SSSurface)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False 
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                isPaused = True if not isPaused else False 

        if not isPaused: 
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
            
            time += 0.003
            pygame.display.update()
            clock.tick(speed)

    pygame.quit()

if __name__ == "__main__":
    run()