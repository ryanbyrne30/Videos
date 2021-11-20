import cmath
import numpy as np

RENDER_ALL = True
dt = 0.003
# dt = 0.0005

# Data
series = [ 
    (cmath.rect(1, 1), 1), 
    (cmath.rect(0.2, 2), -2), 
    (cmath.rect(0.6, 0.4), 3),
    (cmath.rect(5, 0.776), 3.4),
    (cmath.rect(3, 0.2), -7),
    (cmath.rect(1, 1), 9),
]

# series = [
#     (cmath.rect(1, 0), 0),
#     (cmath.rect(1, 0), 0),
#     (cmath.rect(1, 0), 0),
#     (cmath.rect(1, 0), 0),
#     (cmath.rect(1, 0), 0),
#     (cmath.rect(1, 0), 3.01),
#     (cmath.rect(0.5, 0.12314), 5),
#     (cmath.rect(0.5, 0.12314), 7),
# ]

nfs = np.sum([ cmath.polar(f[0])[0] for f in series ])
span = nfs
domain = (-span, span)
range = (-span, span)

# grid
gridColor = (25, 25, 25)
dotColor = [255,0,0]
dotSize = 1.5

# visuals
tail = 1000
compScale = 100

# Screen
ScreenSize = ScreenWidth, ScreenHeight = 1000, 1000
ScreenBGColor = (0,0,0)

# Main Surface
MSSize = MSWidth, MSHeight = 0.8 * ScreenWidth, 0.8*ScreenHeight
MSOrigin = MSX, MSY = 0, 0
MSBGColor = (0,0,0)
MSXTick = MSWidth / (domain[1]-domain[0])
MSYTick = MSHeight / (range[1]-range[0])


# Cos Surface
CSSize = CSWidth, CSHeight = ScreenWidth-MSWidth, MSHeight
CSOrigin = CSX, CSY = MSWidth, MSY
CSBGColor = (10,10,10)
CSXTick = CSWidth / (domain[1]-domain[0])
CSYTick = CSHeight / (range[1]-range[0]) / min(tail, CSHeight/(range[1]-range[0]))


# Sin Surface
SSSize = SSWidth, SSHeight = MSWidth, ScreenHeight-MSHeight
SSXScale = 10
SSOrigin = SSX, SSY = MSX, MSHeight
SSBGColor = (10,10,10)
SSXTick = SSWidth / (domain[1]-domain[0]) / min(tail, SSWidth/(domain[1]-domain[0]))
SSYTick = SSHeight / (range[1]-range[0])
