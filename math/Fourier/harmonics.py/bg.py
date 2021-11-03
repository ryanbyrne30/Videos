import config
import pygame
import cmath

def renderBg(screen, MSSurface, CSSurface, SSSurface):
    screen.fill(config.ScreenBGColor)
    MSSurface.fill(config.MSBGColor)
    CSSurface.fill(config.CSBGColor)
    SSSurface.fill(config.SSBGColor)
    renderGrid(MSSurface, config.MSWidth, config.MSHeight, config.MSXTick, config.MSYTick)
    renderGrid(CSSurface, config.CSWidth, config.CSHeight, config.CSXTick, config.CSYTick)
    renderGrid(SSSurface, config.SSWidth, config.SSHeight, config.SSXTick, config.SSYTick)

def renderGrid(surface, width, height, xtick, ytick):
    for x in range(0, int(width), int(xtick)):
        for y in range(0, int(height), int(ytick)):
            rect = pygame.Rect(x, y, xtick, ytick)
            pygame.draw.rect(surface, config.gridColor, rect, 1)

def renderSurfaces(screen, MSSurface, CSSurface, SSSurface):
    screen.blit(MSSurface, config.MSOrigin)
    screen.blit(CSSurface, config.CSOrigin)
    screen.blit(SSSurface, config.SSOrigin)


def harmonic(f, t):
    c, n = f
    r = c*cmath.exp(2*cmath.pi*1j*n*t)
    return r.real, r.imag

def mapPointToSurface(x, y, originX, originY, xtick, ytick):
    x = originX + x * xtick
    y = originY + y * ytick
    return x, y

def renderPointsOnMSSurface(points, surface, width, height, xtick, ytick, size):
    # x, y = mapPointToSurface(points[0], points[1], width/2, height/2, xtick, ytick)
    # plotPointsOnSurface((x, y), surface, config.MSSize)
    mappedPoints = list(map(lambda p: mapPointToSurface(p[0], p[1], width/2, height/2, 
        xtick, ytick), points))
    dot = pygame.Surface(size, pygame.SRCALPHA)
    for i in range(len(mappedPoints)):
        x, y = mappedPoints[i]
        pygame.draw.circle(
            dot,
            config.dotColor+[i/len(mappedPoints)*255],
            (x, y),
            config.dotSize
        )
    surface.blit(dot, (0,0))

def renderPointsOnCSSurface(points, surface):
    xs = [ p[0] for p in points ]
    ys = list(range(-len(points)+1, 1))
    ps = list(map(lambda p: mapPointToSurface(p[0], p[1], config.CSWidth/2, config.CSHeight/2,
        config.CSXTick, config.CSYTick), list(zip(xs, ys))))
    plotPointsOnSurface(ps, surface, config.CSSize)
    # x, y = mapPointToSurface(points[0], points[1], config.CSWidth/2, config.CSHeight/2,
    #     config.CSXTick, config.CSYTick)
    # plotPointsOnSurface((x, y), surface, config.CSSize)

def renderPointsOnSSSurface(points, surface):
    xs = [ p[1] for p in points ]
    ys = list(range(-len(points)+1, 1))
    ps = list(map(lambda p: mapPointToSurface(p[1], p[0], config.SSWidth/2, config.SSHeight/2,
        config.SSXTick, config.SSYTick), list(zip(xs, ys))))
    plotPointsOnSurface(ps, surface, config.SSSize)

    # x, y = mapPointToSurface(points[0], points[1], config.SSWidth/2, config.SSHeight/2,
    #     config.SSXTick, config.SSYTick)
    # plotPointsOnSurface((x, y), surface, config.SSSize)



def plotPointsOnSurface(points, surface, size):
    # x, y = points
    # pygame.draw.circle(
    #     surface,
    #     config.dotColor,
    #     (x, y),
    #     config.dotSize
    # )
    dot = pygame.Surface(size, pygame.SRCALPHA)
    for i in range(len(points)):
        x, y = points[i]
        pygame.draw.circle(
            dot,
            config.dotColor+[i/len(points)*255],
            (x, y),
            config.dotSize
        )
    surface.blit(dot, (0,0))