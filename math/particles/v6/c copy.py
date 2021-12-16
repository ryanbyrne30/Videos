import numpy as np
from numba import jit
import random

@jit
def dx(x, y, z):
    return x+1

@jit
def dy(x, y, z):
    return y+1

@jit
def dz(x, y, z):
    return z+1

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