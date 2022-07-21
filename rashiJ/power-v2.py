"""
This is version 2 of the power system.

Author:
    Rashi Jain

Date:
    07/21/2022

Notes:

Code Comment:
    Code begins on Line 21.
"""

## Installing dictionaries
from cdcm import *
import numpy as np

# Code Begins
with System(name="everything",
    description="A system that contains everything.") as everything:

    # Initiating Clock
    clock = make_clock(dt=0.5, units="hrs")

    # Moon Enviornment
    with System (name="moon",
        description="Houses most lunar characteristics.") as moon:

            # Parameters
            lunar_day=Parameter(
                value=655.7208,
                units="hrs",
                name="lunar_day",
                track=False,
                description=
                "The length of a day (sunlight + darkness) on the lunar surface"
            )

            solar_irradiance_constant=Parameter(
                value=1361.0,
                units='W/m^2',
                name='solar_irradiance_constant',
                track=False,
                description="Solar irradiance received by the moon."
            )

            # Variables
            solar_irradiance = Variable(
                value = 0.0,
                units = "W/m^2",
                name = "solar_irradiance",
                track = True,
                description = "The solar irradiance at a time instant"
            )

            # Functions
            @make_function(solar_irradiance)
            def calculated_solar_irradiance(t = clock.t,
                                            Imax = solar_irradiance_constant,
                                            T = lunar_day):
                half_T = T / 2
                if int(t / half_T) % 2 == 0: #It's a day
                    return Imax*np.sin(2*np.si*t/T)
                else: #It's a night
                    return 0.0

    # Habitat Initiation


#Testing the Sanity of the Code
print(everything)
