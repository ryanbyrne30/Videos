import numpy as np
from numba import jit
import random
from functools import partial


def randomCoef():
    c = round(random.random() * 3, 6)
    return random.choice([ -c, c, 0, 0, 0 ])

def genCoefs(numCoefs):
    coefs = [ randomCoef() for _ in range(numCoefs) ]
    while np.sum(coefs) == 0:
        coefs = [ randomCoef() for _ in range(numCoefs) ]
    return coefs

def dfun(coefs, x, y, z):
    return coefs[0]*x**2 \
        + coefs[1]*y**2 \
        + coefs[2]*z**2 \
        + coefs[3]*x*y \
        + coefs[4]*x*z \
        + coefs[5]*y*z \
        + coefs[6]*x \
        + coefs[7]*y \
        + coefs[8]*z \
        + coefs[9]


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
def fillFirstStates(states, dt, dx, dy, dz):
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
def fillAllStates(states, dt, dx, dy, dz):
    states = fillFirstStates(states, dt, dx, dy, dz)
    for i in range(dt, states.shape[1]):
        fillNextState(states, i, dt-1)
    return states


if __name__ == "__main__":
    numParts = 3
    dt = 5
    t = 2

    states = np.zeros((numParts, t*dt+dt, 3))
    states[:,0] = np.array([ (random.random(), random.random(), random.random()) for _ in range(numParts) ])

    xcoefs = genCoefs(10)
    ycoefs = genCoefs(10)
    zcoefs = genCoefs(10)

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

    dx = partial(dfun, xcoefs)
    dy = partial(dfun, ycoefs)
    dz = partial(dfun, zcoefs)

    # states = fillFirstStates(states, dt)
    states = fillAllStates(states, dt, dx, dy, dz)
    print(states)
    print(states.shape)
    print('Done')
