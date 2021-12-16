import numpy as np
from numba import jit
import random

@jit
def randomCoef():
    c = round(random.random() * 3, 6)
    return random.choice([ -c, c, 0, 0, 0 ])

@jit
def genCoefs(numCoefs):
    coefs = [ randomCoef() for _ in range(numCoefs) ]
    while np.sum(coefs) == 0:
        coefs = [ randomCoef() for _ in range(numCoefs) ]
    return coefs

xcoefs = genCoefs(10)
ycoefs = genCoefs(10)
zcoefs = genCoefs(10)

@jit
def dx(x, y, z):
    return xcoefs[0]*x**2 \
        + xcoefs[1]*y**2 \
        + xcoefs[2]*z**2 \
        + xcoefs[3]*x*y \
        + xcoefs[4]*x*z \
        + xcoefs[5]*y*z \
        + xcoefs[6]*x \
        + xcoefs[7]*y \
        + xcoefs[8]*z \
        + xcoefs[9]

@jit
def dy(x, y, z):
    return ycoefs[0]*x**2 \
        + ycoefs[1]*y**2 \
        + ycoefs[2]*z**2 \
        + ycoefs[3]*x*y \
        + ycoefs[4]*x*z \
        + ycoefs[5]*y*z \
        + ycoefs[6]*x \
        + ycoefs[7]*y \
        + ycoefs[8]*z \
        + ycoefs[9]

@jit
def dz(x, y, z):
    return zcoefs[0]*x**2 \
        + zcoefs[1]*y**2 \
        + zcoefs[2]*z**2 \
        + zcoefs[3]*x*y \
        + zcoefs[4]*x*z \
        + zcoefs[5]*y*z \
        + zcoefs[6]*x \
        + zcoefs[7]*y \
        + zcoefs[8]*z \
        + zcoefs[9]

@jit
def fillNextState(states, idx, dt):
    for i in range(states.shape[0]):
        prev = max(0, idx-dt)
        x = states[i][prev][0]
        y = states[i][prev][1]
        z = states[i][prev][2]
        x1 = dx(x, y, z)
        y1 = dy(x, y, z)
        z1 = dz(x, y, z)
        states[i][idx] = (x1, y1, z1)
    return states

@jit 
def fillFirstStates(states, dt):
    for i in range(states.shape[0]):
        x0 = states[i][0][0]
        y0 = states[i][0][1]
        z0 = states[i][0][2]
        x1 = dx(x0, y0, z0)
        y1 = dy(x0, y0, z0)
        z1 = dz(x0, y0, z0)
        xs = np.linspace(x0, x1, dt)
        ys = np.linspace(y0, y1, dt)
        zs = np.linspace(z0, z1, dt)
        for j in range(xs.shape[0]):
            states[i][j] = np.array([ xs[j], ys[j], zs[j] ])
    return states

@jit
def fillAllStates(states, dt):
    states = fillFirstStates(states, dt)
    for i in range(dt, states.shape[1]):
        fillNextState(states, i, dt-1)
    return states




if __name__ == "__main__":
    numParts = 3
    dt = 5
    t = 2
    states = np.zeros((numParts, t*dt+dt, 3))
    states[:,0] = np.array([ (random.random(), random.random(), random.random()) for _ in range(numParts) ])

    # states = fillFirstStates(states, dt)
    states = fillAllStates(states, dt)
    print(states)
    print(states.shape)
    print('Done')