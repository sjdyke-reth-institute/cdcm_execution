#!ovn!
"""Test the structure model

Author:
    R Murali Krishnan

Date:
    03.28.2023

"""


import numpy as np


from cdcm import *
from cdcm_mcvt import *


POS_INF = np.finfo(np.float32).max
# Normalize a vector
hat = lambda vec: np.array(vec) / np.linalg.norm(np.array(vec))

# Degree to Radians
deg2rad = lambda deg: deg * np.pi / 180.

# Behavior of segment health state properties
SEGMENT_C = np.array([[0.0, 0.50, 1.00],
                      [0.0, 0.25, 0.75],
                      [0.0, 0.00, 1.00]])

SEGMENT_W = np.array([[    10.0,   20.0, 20.0],
                      [POS_INF,     1.0, 10.0],
                      [POS_INF, POS_INF, 00.0]])


segment_properties = {
        "r0": 40 * 5.,
        "theta0": deg2rad(120.),
        "n_hat": hat([0., 0., 1.]),
        "x_width": 4 * 5,
        "y_width": 10 * 5,
        "E": 1.0,
        "C": SEGMENT_C,
        "W": SEGMENT_W, 
}

with System(name="sys") as sys:
    # clock system
    clock = make_clock(dt=1., units="hr")
    # Segment system
    segment = make_segment("segment", segment_properties)

    # Make structure system
    # dome = make_dome_structure("dome", segment_properties, segment_properties)

sys.forward()
print("!0vn!")


sys_interactive = show_interactive_graph(sys, "test_structure.html")