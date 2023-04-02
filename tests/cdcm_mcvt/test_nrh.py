#~ovn!
"""A CDCM model of MCVT-NRH

Author:
    R Murali Krishnan

Date:
    03.30.2023

"""

from cdcm import *
from cdcm_abstractions import *
from cdcm_mcvt import *
from cdcm_utils import *

import numpy as np

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

with System(name="mcvt_nrh") as mcvt_nrh:
    
    clock = make_clock(dt=1.0, units="hr")

    hab1 = make_hab(
        "hab1", 
        clock.dt, 
        num_zones=2, 
        spl_properties=segment_properties,
        sml_properties=segment_properties
    )


print(mcvt_nrh)
print("~ovn!")

print("MCVT level nodes: ", len(hab1.nodes))
print("Number of Status: ", len(hab1.get_nodes_of_type(HealthStatus)))
print("Number of Tests: ", len(hab1.get_nodes_of_type(Test)))

print("Nodes of MCVT ECLSS: ", len(hab1.eclss.nodes))
# print("Nodes of MCVT Power systems: ", len(hab1.power.nodes))
print("Nodes of MCVT dome: ", len(hab1.dome.nodes))

mcvt_nrh_interactive = make_pyvis_graph(mcvt_nrh, "test_nrh.html")