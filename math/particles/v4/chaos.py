import os
import matplotlib.pyplot as plt 
import numpy as np
from anim import *
import numba as nb
from numba import jit
import random
import subprocess

class Chaos(object):
    def __init__(self, nextState, dt=100, iterations=20):
        self.nextState = nextState
        self.dt = dt
        self.iterations = iterations+1
    
    def genPoints(self, x0, y0):
        x1, y1 = self.nextState((x0, y0))
        x0s = np.linspace(x0, x1, self.dt)
        y0s = np.linspace(y0, y1, self.dt)
        states = [ [(x0s[i], y0s[i])] for i in range(self.dt) ]

        for i in range(1, self.iterations):
            for j in range(self.dt):
                states[j].append(self.nextState(states[j][i-1]))
        
        states = np.array(states)[:,1:]

        xs = [
            states[i][j][0] 
            for j in range(states.shape[1])
            for i in range(states.shape[0])
        ]

        ys = [
            states[i][j][1] 
            for j in range(states.shape[1])
            for i in range(states.shape[0])
        ]

        return xs, ys        
  

def randomCoef():
    c = round(random.random() * 3, 6)
    return random.choice([-c, 0, 0, c])

def HenonMap(state):
    x, y = state 
    x1 = 1 - 1.4*x**2 + y
    y1 = 0.3 * x 
    return x1, y1

for _ in range(10):
    xcoefs = [ randomCoef() for _ in range(5) ]
    while np.sum(xcoefs) == 0:
        xcoefs = [ randomCoef() for _ in range(5) ]

    ycoefs = [ randomCoef() for _ in range(5) ]
    while np.sum(ycoefs) == 0:
        ycoefs = [ randomCoef() for _ in range(5) ]

    # xcoefs = [ 0.934454, -1.623027, -0.987192, -0.117695, 2.619829 ]
    # ycoefs = [ 0, -2.489101, -2.794233, 0, -2.878025 ]

    with open('log.log', 'a') as f:
        f.write(f"""
        dx = {xcoefs[0]}x^2 + {xcoefs[1]}y^2 + {xcoefs[2]}x + {xcoefs[3]}y + {xcoefs[4]}
        xcoefs = {", ".join([ str(c) for c in xcoefs ])}
        dy = {ycoefs[0]}x^2 + {ycoefs[1]}y^2 + {ycoefs[2]}x + {ycoefs[3]}y + {ycoefs[4]}
        ycoefs = {", ".join([ str(c) for c in ycoefs ])}
        --------------------------------------------------
        """)

    dx = lambda state: xcoefs[0]*state[0]**2 \
            + xcoefs[1]*state[1]**2 \
            + xcoefs[2]*state[0] \
            + xcoefs[3]*state[1] \
            + xcoefs[4]

    dy = lambda state: ycoefs[0]*state[0]**2 \
            + ycoefs[1]*state[1]**2 \
            + ycoefs[2]*state[0] \
            + ycoefs[3]*state[1] \
            + ycoefs[4]

    nextPoint = lambda state: (dx(state), dy(state))
    sceneSize = 1000
    sceneRange = 20

    state0s = [ (x, y) 
        for x in np.arange(-1.5, 1.5, 0.05) 
        for y in np.arange(-1.5, 1.5, 0.05) ] 
    print("Num particles:", len(state0s))

    chaos = Chaos(nextPoint, dt=100, iterations=5)
    states = []
    for i in range(len(state0s)):
        x0, y0 = state0s[i]
        xs, ys = chaos.genPoints(x0, y0)
        states.append(list(zip(xs, ys)))

    states = np.array(states)
    print("States:", states.shape)

    scene = Scene(sceneSize, sceneSize, (-sceneRange, sceneRange), (-sceneRange, sceneRange), BLACK)
    scene.createPartials(states)

    gifNum = 0
    for i in range(1000):
        if not os.path.isfile(f"chaos{i}.gif"):
            gifNum = i
            break 

    subprocess.run(["./pngToGif.sh", "partials/", f"chaos{i}.gif"])