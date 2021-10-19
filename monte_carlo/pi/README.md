# Estimating PI Using Monte Carlo Method

This simulation will be determining the probability that a random point on a square also lies within a circle fitted to that square. The expected probability of the point lying within the circle is equivalent to the area of the circle divided by the area of all possible points, the square. 

>P(Circle) = &Pi;r<sup>2</sup> / 4r<sup>2</sup>

We can use this notion to then get the value of pi:

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
