from numba import cuda, jit, vectorize, uint32, uint8, f8, njit 
from matplotlib import pyplot as plt
import numpy as np 
import math 
from pylab import imshow, show 
from timeit import default_timer as timer 

@jit
def mandel(x, y, max_iters):
    c = complex(x, y)
    z = 0.0j 
    for i in range(max_iters):
        z = z*z+c 
        if (z.real*z.real + z.imag*z.imag) >= 4:
            return i 
    return max_iters

@jit
def create_fractal(min_x, max_x, min_y, max_y, image, iters):
    height = image.shape[0]
    width = image.shape[1]

    pixel_size_x = (max_x - min_x) / width 
    pixel_size_y = (max_y - min_y) / height 

    for x in range(width):
        real = min_x + x * pixel_size_x 
        for y in range(height):
            imag = min_y + y * pixel_size_y 
            color = mandel(real, imag, iters)
            image[y, x] = color 

mandel_gpu = cuda.jit(uint32(f8, f8, uint32), device=True)(mandel)
# mandel_gpu = cuda.jit(restype=uint32, argtypes=[f8, f8, uint32], device=True)(mandel)

@cuda.jit(f8, f8, f8, f8, uint8[:,:], uint32)
def mandel_kernel(min_x, max_x, min_y, max_y, image, iters):
    height = image.shape[0]
    width = image.shape[1]

    pixel_size_x = (max_x - min_x) / width 
    pixel_size_y = (max_y - min_y) / height 

    startX, startY = cuda.grid(2)
    gridX = cuda.gridDim.x * cuda.blockDim.x;
    gridY = cuda.gridDim.y * cuda.blockDim.y;

    for x in range(startX, width, gridX):
        real = min_x + x * pixel_size_x 
        for y in range(startY, height, gridY):
            imag = min_y + y * pixel_size_y
            image[y, x] = mandel_gpu(real, imag, iters)



image = np.zeros((1024, 1536), dtype=np.uint8)
start = timer()
create_fractal(-2.0, 1.0, -1.0, 1.0, image, 20)
dt = timer() - start 

print("Mandlebrot created in %f s" %dt) 
imshow(image)
show()