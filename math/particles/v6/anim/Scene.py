from PIL import Image, ImageDraw
import numpy as np
from anim import *
import threading


class Scene(object):
    def __init__(self, width, height, xrange, yrange, color, trailLength):
        self.width = width 
        self.height = height
        self.xrange = xrange 
        self.yrange = yrange 
        self.color = color 
        self.trailLength = trailLength

    def createGif(self, states):
        """
        states: [
            [ (x,y), ... ], <- particle 1
            [ (x,y), ... ], <- particle 1
            ...
            [ (x,y), ... ] <- particle n
        ]
        """
        frames = []
        states = np.array(states)
        for p in range(states.shape[0]):
            frame = Frame(self.width, self.height, self.xrange, self.yrange, self.color)
            for s in range(states.shape[1]):
                x, y = states[p][s]
                frame.addPoint(x, y, color=WHITE, opacity=255, radius=0.75)
            frame.renderPoints()
            frames.append(frame.surface)
        frames[0].save('chaos.gif', save_all=True, append_images=frames[1:], optimize=False, duration=30, loop=0)
    
    def createPartials(self, states):
        numThreads = 10
        idxs = np.array_split(list(range(states.shape[1])), numThreads)
        threads = []

        for i in range(numThreads):
            thread = RenderThread(idxs[i], states, self.trailLength, self.width, self.height, self.xrange, self.yrange, self.color)
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()




class RenderThread(threading.Thread):
    def __init__(self, idxs, states, trailLength, width, height, xrange, yrange, color):
        threading.Thread.__init__(self)
        self.idxs = idxs 
        self.states = states
        self.trailLength = trailLength
        self.width = width 
        self.height = height 
        self.xrange = xrange 
        self.yrange = yrange 
        self.color = color
    
    def run(self):
        opacities = [ int(i/self.trailLength*255) for i in range(self.trailLength) ]
        for idx in self.idxs:
            idx0 = max(0, idx-self.trailLength)
            trail = self.states[:,idx0:idx]
            print(f"{idx}/{self.idxs[-1]}")
            frame = Frame(self.width, self.height, self.xrange, self.yrange, self.color)
            for i in range(trail.shape[1]):
                for p in range(trail.shape[0]):
                    x, y = trail[p][i]
                    frame.addPoint(x, y, opacity=opacities[i], radius=0.6)
            frame.renderPoints()
            padding = "".join(["0" for _ in range(9-len(str(idx)))])
            padded = padding+str(idx)
            frame.surface.save(f'partials/p{padded}.png')



