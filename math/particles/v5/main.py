import os
import subprocess
from Chaos import Chaos
import random
import numpy as np
from anim import *
from numba import njit, jit
from functools import partial

OUTPUT_DIR = "gifs"

class Main(object):
    def __init__(self, trailLength=10, dt=100, totalTime=3):
        self.dir = self.outDir()
        sceneSize = 1000
        sceneRange = 20
        
        numCoefs = 10
        self.xcoefs = self.randomCoefs(numCoefs)
        self.ycoefs = self.randomCoefs(numCoefs)
        self.zcoefs = self.randomCoefs(numCoefs)
        
        self.log()
        
        dx = self.dfun(self.xcoefs)
        dy = self.dfun(self.ycoefs)
        dz = self.dfun(self.zcoefs)
        
        self.state0s = self.initStates()
        print("Num particles:", len(self.state0s))
        
        nextState = lambda state: (dx(state), dy(state), dz(state))
        self.chaos = Chaos(nextState, dt=dt, iterations=totalTime)
        states = self.genStates()
        
        scene = Scene(sceneSize, sceneSize, (-sceneRange, sceneRange), (-sceneRange, sceneRange), BLACK, trailLength)
        scene.createPartials(states)
        self.createGif()

    def randomCoef(self):
        c = round(random.random() * 3, 6)
        return random.choice([ -c, c, 0, 0, 0 ])
    
    def randomCoefs(self, num):
        return [ self.randomCoef() for _ in range(num) ]

    def genCoefs(self):
        xcoefs = [ self.randomCoef() for _ in range(self.numCoefs) ]
        while np.sum(xcoefs) == 0:
            xcoefs = [ self.randomCoef() for _ in range(self.numCoefs) ]

    def outDir(self):
        dirNum = 0
        while os.path.isdir(OUTPUT_DIR+f"/{dirNum}"):
            dirNum += 1
        os.mkdir(OUTPUT_DIR+f"/{dirNum}")
        return OUTPUT_DIR+f"/{dirNum}"

    def log(self):
        with open(self.dir+'/log.log', 'a') as f:
            f.write(f"""
            dx = {self.xcoefs[0]}x^2 + {self.xcoefs[1]}y^2 + {self.xcoefs[2]}z^2 + {self.xcoefs[3]}xy + {self.xcoefs[4]}xz + {self.xcoefs[5]}yz + {self.xcoefs[6]}x + {self.xcoefs[7]}y + {self.xcoefs[8]}z + {self.xcoefs[9]}
            xcoefs = {", ".join([ str(c) for c in self.xcoefs ])}
            dy = {self.ycoefs[0]}x^2 + {self.ycoefs[1]}y^2 + {self.ycoefs[2]}z^2 + {self.ycoefs[3]}xy + {self.ycoefs[4]}xz + {self.ycoefs[5]}yz + {self.ycoefs[6]}x + {self.ycoefs[7]}y + {self.ycoefs[8]}z + {self.ycoefs[9]}
            ycoefs = {", ".join([ str(c) for c in self.ycoefs ])}
            dz = {self.zcoefs[0]}x^2 + {self.zcoefs[1]}y^2 + {self.zcoefs[2]}z^2 + {self.zcoefs[3]}xy + {self.zcoefs[4]}xz + {self.zcoefs[5]}yz + {self.zcoefs[6]}x + {self.zcoefs[7]}y + {self.zcoefs[8]}z + {self.zcoefs[9]}
            zcoefs = {", ".join([ str(c) for c in self.zcoefs ])}
            --------------------------------------------------
            """)
        
    def dfunPart(self, coefs, state):
        n = coefs[0]*state[0]**2 \
            + coefs[1]*state[1]**2 \
            + coefs[2]*state[2]**2 \
            + coefs[3]*state[0]*state[1] \
            + coefs[4]*state[0]*state[2] \
            + coefs[5]*state[1]*state[2] \
            + coefs[6]*state[0] \
            + coefs[7]*state[1] \
            + coefs[8]*state[2] \
            + coefs[9]
        sign = 1 if n > 0 else -1
        return n if abs(n) < 1e10 and not np.isnan(n) else 1e10*sign

    def dfun(self, coefs):
        return partial(self.dfunPart, coefs)

    def initStates(self):
        return [ (x, y, z) 
        for x in np.arange(-1.5, 1.5, 0.1) 
        for y in np.arange(-1.5, 1.5, 0.1) 
        for z in np.arange(-1.5, 1.5, 1) 
    ] 

    def genStates(self):
        states = []
        for i in range(len(self.state0s)):
            x0, y0, z0 = self.state0s[i]
            xs, ys, zs = self.chaos.genPoints(x0, y0, z0)
            states.append(list(zip(xs, ys)))
        states = np.array(states)
        print("States:", states.shape)
        return states[:,:,:2]

    def createGif(self):
        gifNum = 0
        for i in range(1000):
            if not os.path.isfile(f"chaos{i}.gif"):
                gifNum = i
                break 
        subprocess.run(["./pngToGif.sh", "partials/", f"{self.dir}/chaos{gifNum}.gif"])


if __name__ == "__main__":
    Main(dt=1, totalTime=100)