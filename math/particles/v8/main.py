import os
import subprocess
import random
import numpy as np
from anim import *
from functools import partial
from scipy.integrate.odepack import odeint

OUTPUT_DIR = "gifs"

class Main(object):
    def __init__(self, particles=10, xcoefs=None, ycoefs=None):
        self.dir = self.outDir()
        xcoefs = self.genCoefs(10) if xcoefs is None else xcoefs
        ycoefs = self.genCoefs(10) if ycoefs is None else ycoefs
        self.log(xcoefs, ycoefs)

        dx = partial(self.delta, xcoefs)
        dy = partial(self.delta, ycoefs)

        self.initialStates = self.initialStates(particles)
        self.nextState = partial(self.nextState, dx, dy)

    def randomCoef(self):
        # return random.choice([ -1, 1, 0.5, -0.5, 1.5, -1.5, 0, 0, 0, 0, 0, 0, 0 ])
        c = round(random.random() * 100, 6)
        return random.choice([ -c, c, 0, 0, 0 ])
    
    def genCoefs(self, numCoefs):
        coefs = [ self.randomCoef() for _ in range(numCoefs) ]
        while np.sum(coefs) == 0:
            coefs = [ self.randomCoef() for _ in range(numCoefs) ]
        return coefs

    def delta(self, coefs, state, t):
        x, y = state
        return coefs[0]*x**2 \
        + coefs[1]*y**2 \
        + coefs[2]*t**2 \
        + coefs[3]*x*y \
        + coefs[4]*x*t \
        + coefs[5]*y*t \
        + coefs[6]*x \
        + coefs[7]*y \
        + coefs[8]*t \
        + coefs[9]

    def nextState(self, dx, dy, state, t):
        return dx(state, t), dy(state, t)

    def initialState(self):
        max = 1
        return random.random()*max*random.choice([-1,  1]), random.random()*max*random.choice([-1,  1])

    def initialStates(self, particles):
        return [
            self.initialState()
            for _ in range(particles)
        ]

    def genStates(self, t0, t1, dt):
        particles = len(self.initialStates)
        t = np.arange(t0, t1, dt)
        states = np.zeros((particles, len(t), 2))
        for i in range(len(self.initialStates)):
            s = odeint(self.nextState, self.initialStates[i], t)
            states[i,:,:] = s
        return states

    def outDir(self):
        dirNum = 0
        while os.path.isdir(OUTPUT_DIR+f"/{dirNum}"):
            dirNum += 1
        os.mkdir(OUTPUT_DIR+f"/{dirNum}")
        return OUTPUT_DIR+f"/{dirNum}"

    def log(self, xcoefs, ycoefs):
        with open(self.dir+'/log.log', 'a') as f:
            f.write(f"""
            dx = {xcoefs[0]}x^2 + {xcoefs[1]}y^2 + {xcoefs[2]}t^2 + {xcoefs[3]}xy + {xcoefs[4]}xt + {xcoefs[5]}yt + {xcoefs[6]}x + {xcoefs[7]}y + {xcoefs[8]}t + {xcoefs[9]}
            xcoefs = {", ".join([ str(c) for c in xcoefs ])}
            dy = {ycoefs[0]}x^2 + {ycoefs[1]}y^2 + {ycoefs[2]}t^2 + {ycoefs[3]}xy + {ycoefs[4]}xt + {ycoefs[5]}yt + {ycoefs[6]}x + {ycoefs[7]}y + {ycoefs[8]}t + {ycoefs[9]}
            ycoefs = {", ".join([ str(c) for c in ycoefs ])}
            --------------------------------------------------
            """)

    def createGif(self, states, width, height, xrange, yrange, color, trailLength):
        scene = Scene(width, height, xrange, yrange, color, trailLength)
        scene.createPartials(states)
        gifNum = 0
        for i in range(1000):
            if not os.path.isfile(f"chaos{i}.gif"):
                gifNum = i
                break 
        subprocess.run(["./pngToGif.sh", "partials/", f"{self.dir}/chaos{gifNum}.gif"])



if __name__ == "__main__":
    # xc = [ 1, 0, 0, 0, -1, 1, -1, 0, 0, 0 ]
    # yc = [ 0, -1, -1, -1, -1, -1, 0, -1, 0, 0 ]
    for _ in range(10):
        m = Main(particles=100, xcoefs=None, ycoefs=None)
        states = m.genStates(0, 8, 0.05)
        print("States:", states.shape)
        crange = 5
        m.createGif(states, 1500, 1500, (-crange, crange), (-crange, crange), PINK, 100)