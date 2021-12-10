from PIL import Image, ImageDraw
import numpy as np
from anim import *
import threading


class Scene(object):
    def __init__(self, width, height, xrange, yrange, color):
        self.width = width 
        self.height = height
        self.xrange = xrange 
        self.yrange = yrange 
        self.color = color 

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



    
    # def createGif(self, states, trailLength, stateSkip):
    #     opacities = np.linspace(0, 255, trailLength).astype(int)
    #     frames = []
    #     for i in range(0, states.shape[1], stateSkip):
    #         i0 = max(0, i-trailLength)
    #         trail = states[:,i0:i]
    #         print(f"{i}/{states.shape[1]}")
    #         # print("Trail shape:", trail.shape)
    #         frame = Frame(self.width, self.height, self.xrange, self.yrange, self.color)
    #         for j in range(trail.shape[0]):
    #             for k in range(trail.shape[1]):
    #                 state = trail[j][k]
    #                 # print(f"State[{j}][{k}] =", state)
    #                 frame.addPoint(state[0], state[1], opacity=opacities[k], radius=1)
    #         frame.renderPoints()

    #         # padding = "".join(["0" for _ in range(9-len(str(i)))])
    #         # padded = padding+str(i)
    #         # frame.surface.save(f'partials/p{padded}.png')
    #         frames.append(frame.surface)
    #     frames[0].save('lorenz.gif', save_all=True, append_images=frames[1:], optimize=False, duration=30, loop=0)

    # def createPartials(self, states, trailLength, stateSkip):
    #     numThreads = 40
    #     idxs = list(range(0, states.shape[1], stateSkip))
    #     idxs = np.array_split(idxs, numThreads)
    #     threads = []

    #     for i in range(numThreads):
    #         thread = RenderThread(idxs[i], states, trailLength, self.width, self.height, self.xrange, self.yrange, self.color)
    #         threads.append(thread)
    #         thread.start()

    #     for thread in threads:
    #         thread.join()

    
    def createPartials(self, states):
        numThreads = 10
        idxs = np.array_split(list(range(states.shape[1])), numThreads)
        threads = []

        for i in range(numThreads):
            thread = RenderThread(idxs[i], states, self.width, self.height, self.xrange, self.yrange, self.color)
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()




class RenderThread(threading.Thread):
    def __init__(self, idxs, states, width, height, xrange, yrange, color):
        threading.Thread.__init__(self)
        self.idxs = idxs 
        self.states = states
        self.width = width 
        self.height = height 
        self.xrange = xrange 
        self.yrange = yrange 
        self.color = color

    # def run(self):
    #     opacities = np.linspace(0, 255, self.trailLength).astype(int)
    #     for idx in self.idxs:
    #         i0 = max(0, idx-self.trailLength)
    #         trail = self.states[:,i0:idx]
    #         print(f"{idx}/{self.idxs[-1]}")
    #         frame = Frame(self.width, self.height, self.xrange, self.yrange, self.color)
    #         for j in range(trail.shape[0]):
    #             for k in range(trail.shape[1]):
    #                 state = trail[j][k]
    #                 frame.addPoint(state[0], state[1], opacity=opacities[k], radius=0.6)
    #         frame.renderPoints()
    #         padding = "".join(["0" for _ in range(9-len(str(idx)))])
    #         padded = padding+str(idx)
    #         frame.surface.save(f'partials/p{padded}.png')

    
    def run(self):
        for idx in self.idxs:
            print(f"{idx}/{self.idxs[-1]}")
            frame = Frame(self.width, self.height, self.xrange, self.yrange, self.color)
            for p in range(self.states.shape[0]):
                x, y = self.states[p][idx]
                frame.addPoint(x, y, opacity=255, radius=0.6)
            frame.renderPoints()
            padding = "".join(["0" for _ in range(9-len(str(idx)))])
            padded = padding+str(idx)
            frame.surface.save(f'partials/p{padded}.png')



