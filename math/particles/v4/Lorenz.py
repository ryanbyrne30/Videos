import numpy as np
from scipy.integrate.odepack import odeint
import random
import matplotlib.pyplot as plt
from anim import *
from anim.globals import *


class Lorenz(object):
    def __init__(self, sigma=10, rho=28, beta=8/3):
        self.sigma = sigma 
        self.rho = rho 
        self.beta = beta 

    def dx(self, x, y, z, t):
        return 1-self.sigma*x**2 + y
        # return y + 0.5 * self.sigma * x**2 + 1/4*self.beta*x**4
    
    def dy(self, x, y, z, t):
        return self.beta*x
        # return -0.5*y**2 + self.sigma*x + self.beta*x**3

    def dz(self, x, y, z, t):
        return z

    def deltaX(self, x, y, sigma):
        return sigma*y - sigma*x

    def deltaY(self, x, y, z, rho):
        return rho*x - x*z - y 

    def deltaZ(self, x, y, z, beta):
        return x*y - beta*z

    def nextState(self, state, t):
        x, y, z = state
        dx = self.dx(x, y, z, t)
        dy = self.dy(x, y, z, t)
        dz = self.dz(x, y, z, t)
        # dx = self.deltaX(x, y, self.sigma)
        # dy = self.deltaY(x, y, z, self.rho)
        # dz = self.deltaZ(x, y, z, self.beta)
        return dx, dy, dz

    def initStates(self, particles):
        maxPos = 5
        return [ 
            (
                maxPos*random.random()*random.choice([-1, 1]), 
                maxPos*random.random()*random.choice([-1, 1]), 
                maxPos*random.random()*random.choice([-1, 1])
            ) for _ in range(particles)
        ]

    def getStates(self, particles):
        state0 = self.initStates(particles)
        print("Initial states:", state0)
        t0 = 1
        t1 = 7
        dt = 0.001
        t = np.arange(t0, t1, dt)
        print("T:", t)
        allStates = []

        for i in range(particles):
            states = odeint(self.nextState, state0[i], t)
            allStates.append([states])
        return np.array(allStates).reshape((particles, -1, 3))





l = Lorenz(sigma=1.4, beta=0.3, rho=0.3)
states = l.getStates(20)
print("States shape:", states.shape)
print(states[:,:10])

size = 10
scene = Scene(800, 800, (-size, size), (-size, size), BLACK)
scene.createPartials(states, 300, 80)
