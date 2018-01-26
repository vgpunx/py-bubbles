import math, collections


Orientation = collections.namedtuple("Orientation", ["f0", "f1", "f2", "f3", "b0", "b1", "b2", "b3", "start_angle"])
Layout = collections.namedtuple("Layout", ["orientation", "size", "origin"])

layout_pointy = Orientation(
    math.sqrt(3.0), 
    math.sqrt(3.0) / 2.0, 
    0.0, 
    3.0 / 2.0, 
    math.sqrt(3.0) / 3.0, 
    -1.0 / 3.0, 
    0.0, 
    2.0 / 3.0, 
    0.5
)

layout_flat = Orientation(
    3.0 / 2.0, 
    0.0, 
    math.sqrt(3.0) / 2.0, 
    math.sqrt(3.0), 
    2.0 / 3.0, 
    0.0, 
    -1.0 / 3.0, 
    math.sqrt(3.0) / 3.0, 
    0.0
)
