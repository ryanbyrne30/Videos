# Estimating PI Using Monte Carlo Method

This simulation will be determining the probability that a random point on a square also lies within a circle fitted to that square. The expected probability of the point lying within the circle is equivalent to the area of the circle divided by the area of all possible points, the square. 

>P(Circle) = &Pi;r<sup>2</sup> / 4r<sup>2</sup>

We can use this notion to then get the value of PI:

>&Pi; = (4r<sup>2</sup> * P(Circle)) / r<sup>2</sup>

We can estimate P(Circle) using the Monte Carlo method by calculating the amount of points that lie within the circle compared to the total amount of points generated. Using this our equation then becomes:

>&Pi; = (4r<sup>2</sup> * points in circle) / (r<sup>2</sup> * total points)

Assuming a circle with radius = 1 we can simplify this further:

>&Pi; = 4 * points in circle / total points

## Running the simulation
Install the dependences

`pip3 install matplotlib pygame`

Run it

`python3 pi.py`

You can freeze the simulation at any point by pressing the SPACE bar

## About estimating PI
To calculate the exact value of PI, infinite storage and time would be required. Unfortunately we do not have that, however we can adjust the precision to which we would like to make these estimates. 

In order to pick a random point, the simulation picks an X coordinate within the square width (800 by default) and the a Y coordinate within the square height (also 800). This means that the precision of our estimate will be limited to a max dataset of size 800x800 = 640000.

To increase our precision we can increase the size of the square. If we have an increase of 200 to our height and width, the max size of our dataset will be 1000x1000 = 1000000. However visually we may not be able to see the full size of the square when it gets big enough (a 1080p monitors will only be able to see squares up to 1080 pixels in height/width). Therefore we can adjust the precision of the simulation by changing the parameter `precision` within the script.

What the parameter `precision` does is expand the scope of possible random coordinates by including floats, not just integers, to be used. For example, with `precision=100` the coordinates of all possible random points with range from 0.00-800.00. This means that instead of the size of our dataset being 800x800 = 6400000, our dataset now spans to 80000x80000 = 6400000000 or a 100<sup>2</sup> increase.

By adjusting the size of the square and range of possible coordinates, we can achieve better estimates.
