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
    
    def genPoints(self, x0, y0, z0):
        x1, y1, z1 = self.nextState((x0, y0, z0))
        x0s = np.linspace(x0, x1, self.dt)
        y0s = np.linspace(y0, y1, self.dt)
        z0s = np.linspace(z0, z1, self.dt)
        states = [ [(x0s[i], y0s[i], z0s[i])] for i in range(self.dt) ]

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

        zs = [
            states[i][j][2] 
            for j in range(states.shape[1])
            for i in range(states.shape[0])
        ]

        return xs, ys, zs    