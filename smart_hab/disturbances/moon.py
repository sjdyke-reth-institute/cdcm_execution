"""
Makes the moon system with all its properties.

"""


__all__ = ["make_moon"]


from cdcm import *
from . import make_radiation_env_0
from . import make_thermal_env_0


def make_moon(
    clock,
    make_radiation_env=make_radiation_env_0,
    make_thermal_env=make_thermal_env_0
    ):
    """
    Make a moon system.

    Arguments
    clock -- A clock object measuring time in seconds.
             TODO: Clock should be in Julian time.

    """

    with System(name="moon", description="The moon system") as moon:
        half_day_light = Parameter(
            name="half_day_light",
            value=29.5306 * 3600 * 12,
            units="sec",
            description="The period of time during which the sun is shining"
        )

        # I would love to have things depend on these:
        # longitude =
        # latitude =
        # height =

        radiation  = make_radiation_env(clock, moon)

        thermal = make_thermal_env(clock, moon)

    return moon