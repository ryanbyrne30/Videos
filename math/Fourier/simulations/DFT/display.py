import cmath
from math import sqrt
import pygame
import numpy as np

def dft(cpoints):
    X = []
    N = len(cpoints)
    for k in range(N):
        sum = 0
        for n in range(N):
            phi = -2*cmath.pi*k*n/N
            sum += cpoints[n] * cmath.exp(phi*1j)

        avg = sum / N
        freq = k
        amp = np.linalg.norm(avg)


        phase = np.arctan2(avg.imag, avg.real)


        X.append([avg, freq, amp, phase])
    return X


def epicycles(screen, c, rotation, fourier, t):
    for avg, freq, amp, phase in fourier:
        prevC = c
        phi = freq*t+phase+rotation
        c += cmath.rect(amp, phi)
        pygame.draw.circle(screen, (75,75,75,255), (prevC.real, prevC.imag), amp, 1)
        pygame.draw.line(screen, (150,150,150, 255), (prevC.real, prevC.imag), (c.real, c.imag), 1)
    return c
