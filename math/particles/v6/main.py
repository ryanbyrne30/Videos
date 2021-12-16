import os
import subprocess
from Chaos import Chaos
import random
from numba.core.decorators import jit
import numpy as np
from anim import *
from numba import njit
from functools import partial

OUTPUT_DIR = "gifs"

def randomCoef():
    c = round(random.random() * 3, 6)
    return random.choice([ -c, c, 0, 0, 0 ])

def genCoefs(numCoefs):
    coefs = [ randomCoef() for _ in range(numCoefs) ]
    while np.sum(coefs) == 0:
        coefs = [ randomCoef() for _ in range(numCoefs) ]
    return coefs

xcoefs = genCoefs(10)
ycoefs = genCoefs(10)
zcoefs = genCoefs(10)

# @jit
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

# @jit
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

# @jit
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

# @jit
def fillNextState(states, idx, dt):
    for i in range(states.shape[0]):
        prev = max(0, idx-dt)
        x = states[i][prev][0]
        y = states[i][prev][1]
        z = states[i][prev][2]
        x1 = dx(x, y, z)
        y1 = dy(x, y, z)
        z1 = dz(x, y, z)
        # if np.isnan(x1) or abs(x1) > 1e100:
        #     x1 = 1e100 if x1 > 0 else -1e100
        # if np.isnan(y1) or abs(y1) > 1e100:
        #     y1 = 1e100 if x1 > 0 else -1e100
        # if np.isnan(z1) or abs(z1) > 1e100:
        #     z1 = 1e100 if x1 > 0 else -1e100
        states[i][idx] = (x1, y1, z1)
    return states

# @jit 
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

# @jit
def fillAllStates(states, dt):
    states = fillFirstStates(states, dt)
    for i in range(dt, states.shape[1]):
        fillNextState(states, i, dt-1)
    return states




class Main(object):
    def __init__(self, sceneSize=1000, sceneRange=20, trailLength=10):
        self.dir = self.outDir() 
        self.scene = Scene(sceneSize, sceneSize, (-sceneRange, sceneRange), (-sceneRange, sceneRange), BLACK, trailLength)
        # scene.createPartials(states)
        # self.createGif()

    def outDir(self):
        dirNum = 0
        while os.path.isdir(OUTPUT_DIR+f"/{dirNum}"):
            dirNum += 1
        os.mkdir(OUTPUT_DIR+f"/{dirNum}")
        return OUTPUT_DIR+f"/{dirNum}"

    def log(self, xcoefs, ycoefs, zcoefs):
        with open(self.dir+'/log.log', 'a') as f:
            f.write(f"""
            dx = {xcoefs[0]}x^2 + {xcoefs[1]}y^2 + {xcoefs[2]}z^2 + {xcoefs[3]}xy + {xcoefs[4]}xz + {xcoefs[5]}yz + {xcoefs[6]}x + {xcoefs[7]}y + {xcoefs[8]}z + {xcoefs[9]}
            xcoefs = {", ".join([ str(c) for c in xcoefs ])}
            dy = {ycoefs[0]}x^2 + {ycoefs[1]}y^2 + {ycoefs[2]}z^2 + {ycoefs[3]}xy + {ycoefs[4]}xz + {ycoefs[5]}yz + {ycoefs[6]}x + {ycoefs[7]}y + {ycoefs[8]}z + {ycoefs[9]}
            ycoefs = {", ".join([ str(c) for c in ycoefs ])}
            dz = {zcoefs[0]}x^2 + {zcoefs[1]}y^2 + {zcoefs[2]}z^2 + {zcoefs[3]}xy + {zcoefs[4]}xz + {zcoefs[5]}yz + {zcoefs[6]}x + {zcoefs[7]}y + {zcoefs[8]}z + {zcoefs[9]}
            zcoefs = {", ".join([ str(c) for c in zcoefs ])}
            --------------------------------------------------
            """)

    def run(self, numParts, dt, t):
        self.log(xcoefs, ycoefs, zcoefs)
        states = np.zeros((numParts, t*dt+dt, 3))
        print("States:", states.shape)
        states[:,0] = np.array([ 
            (round(1.5*random.random(), 6), round(1.5*random.random(), 6), round(1.5*random.random(), 6))
            for _ in range(numParts)
        ])
        states = fillAllStates(states, dt)
        return states

    

    # def initStates(self):
    #     return [ (x, y, z) 
    #     for x in np.arange(-1.5, 1.5, 0.1) 
    #     for y in np.arange(-1.5, 1.5, 0.1) 
    #     for z in np.arange(-1.5, 1.5, 1) 
    # ] 

    # def setupStates(self):
    #     states = np.empty((len(self.state0s), self.dt*self.totalTime, 3))
    #     states[:,1] = self.state0s
    #     return states

    # @jit
    # def genStates(self, states, numParts, duration):
    #     for i in range(1, numParts):
    #         for p in range(duration):
    #             states[p][i][0] = self.dx(states[p][i-1][0])
    #             states[p][i][1] = self.dx(states[p][i-1][1])
    #             states[p][i][2] = self.dx(states[p][i-1][2])
    #     return states

    # def createGif(self):
    #     gifNum = 0
    #     for i in range(1000):
    #         if not os.path.isfile(f"chaos{i}.gif"):
    #             gifNum = i
    #             break 
    #     subprocess.run(["./pngToGif.sh", "partials/", f"{self.dir}/chaos{i}.gif"])


if __name__ == "__main__":
    states = Main().run(1000, 100, 10)
    print(states)
    print(states.shape)