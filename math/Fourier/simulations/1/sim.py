import cmath
import pygame
from config import Config
import numpy as np


def renderSurface(screen, surface, surfaceConfig):
    surface = pygame.Surface(surfaceConfig.size)
    surface.fill(surfaceConfig.color)
    renderSurfaceGrid(surface, surfaceConfig)
    screen.blit(surface, (surfaceConfig.x, surfaceConfig.y))

def renderSurfaceGrid(surface, s):
    for x in range(0, s.width, int(s.xtick)):
        for y in range(0, s.height, int(s.ytick)):
            rect = pygame.Rect(x, y, s.xtick, s.ytick)
            pygame.draw.rect(surface, s.gridColor, rect, 1)

def run(config):
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(config.screen.size)
    main = pygame.Surface(config.surfaces.main.size)
    screen.fill(config.screen.color)
    renderSurface(screen, main, config.surfaces.main)

    running = True
    isPaused = False 
    t = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False 
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                isPaused = True if not isPaused else False 
        
        c = cmath.exp(2*cmath.pi*1j*t)
        dot = pygame.Surface(config.surfaces.main.size, pygame.SRCALPHA)
        pygame.draw.circle(
            dot,
            config.dot.color,
            (c.imag, c.real),
            config.dot.radius
        )
        main.blit(dot, (0,0))

        t += 0.001
        pygame.display.update()
        clock.tick(config.speed)
    pygame.quit()




if __name__ == "__main__":
    config = Config()
    run(config)