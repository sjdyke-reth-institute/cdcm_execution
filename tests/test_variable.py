"""Tests quantities using pytest.

Author:
    Roman Ibrahimov

Date:
    3/11/2022
"""


import numpy as np
from cdcm import *
import yaml


# Testing floating point value
q = Quantity(
    value=43.658123,
    units="m",
    name="random_name",
    track=True,
    description="Some description.")
print(yaml.dump(q.to_yaml(), sort_keys=False))

# Testing integer value
q = Quantity(
    value=1,
    units="km",
    name="random_name",
    track=False,
    description="description"
)
print(yaml.dump(q.to_yaml(), sort_keys=False))

# It tests Quantity class with arrays
arr_float = np.array([1.12, 2.2332, 3.34, 4.5326, 5.67])
q = Quantity(
    value=arr_float,
    units="m",
    name="random_name",
    track=False,
    description="description"
)
print(yaml.dump(q.to_yaml(), sort_keys=False))
