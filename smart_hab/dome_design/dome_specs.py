"""
Makes the dome specs system with all its design parameters.

"""


__all__ = ["make_dome_specs"]

import math

from cdcm import *



def make_dome_specs():
    """
    Make a dome specs system.

    Arguments

    """

    with System(name="dome_specs", description="The dome_specs system") as dome_specs:
        dome_radius = Parameter(
            name="dome_radius",
            value=2.9,
            units="m",
            description="radius of dome of the habitat"
        )

        dome_surface_area = Parameter(
            name="dome_surface_area",
            value=math.pi * dome_radius.value **2,
            units="m^2",
            description="surface area of dome of the habitat"
        )

    return dome_specs