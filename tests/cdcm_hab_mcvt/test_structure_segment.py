#!ovn!
"""Make structural segment

Author:
    R Murali Krishnan
    
Date:
    03.27.2023
    
"""


from cdcm import *
from cdcm_hab_mcvt import *
POS_INF = np.finfo(np.float32).max

deg2rad = lambda deg: deg * np.pi / 180.

dome_radius = 4 * 5
# Behavior of segment health state properties
SEGMENT_C = np.array([[0.0, 0.50, 1.00],
                      [0.0, 0.25, 0.75],
                      [0.0, 0.00, 1.00]])

SEGMENT_W = np.array([[    10.0,   20.0, 20.0],
                      [POS_INF,     1.0, 10.0],
                      [POS_INF, POS_INF, 00.0]])
simple_segment = {
    "r0": 0.,
    "theta0": deg2rad(0.),
    "n_hat": hat([0., 0., 1.]),
    "x_width": 2 * dome_radius,
    "y_width": 2 * dome_radius,
    "E": 1.0,
    "C": SEGMENT_C,
    "W": SEGMENT_W,
}

with System(name="sys") as sys:
    segment = make_segment(
        name="segment",
        segment_properties=simple_segment
    )

print(sys)
print("fin.")