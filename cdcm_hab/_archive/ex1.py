"""This is a version one of the power system.

Author:
    Rashi

Date:
    7/20/2022

Notes:
    - Read PEP8.
    - Read about context managers.
"""

import numpy as np
from cdcm import *

with System(name="everything",
    description="A system that contains everything.") as everything:

    clock = make_clock(dt=0.5, units="hrs")

    with System(name="moon",
        description = "Most lunar characteristics.") as moon:

        lunar_day = Parameter(
            value=655.7208,
            units="hrs",
            name="lunar_day",
            track=False,
            description=
                "The length of a day (sunlight + darkness) on the lunar surface."
        )

        solar_irradiance_constant = Parameter(
            value=1361.0,
            units="W/m^2",
            name="solar_irradiance_constant",
            track=False,
            description="solar irradiance constant"
        )

        solar_irradiance = Variable(
            value=0.0,
            units="W/m^2",
            name="solar_irradiance",
            track=True,
            description="The solar irradiance at a time instant."
        )

        @make_function(solar_irradiance)
        def calculate_solar_irradiance(t=clock.t,
                                       Imax=solar_irradiance_constant,
                                       T=lunar_day):
            half_T = T / 2
            if int(t / half_T) % 2 == 0:
                # It is day
                return Imax * np.sin(2 * np.pi * t / T)
            else:
                return 0.0

    with System(name="power", description="write me") as power:
        with System(name="pv") as pv:
            pass
            # You write code here

        with System(name="nuclear") as nc:
            pass

print(everything)

for i in range(50):
    everything.forward()
    print(f"t = {everything.clock.t.value:1.1f}, I(t) = {everything.moon.solar_irradiance.value:1.2f}")
    everything.transition()

quit()

########################### Describing Moon ####################################
#moon = Node(name = "moon", description = "most lunar characteristics")

# Source: nssdc.gfsc.nasa.gov/planetary/factsheet/moonfact.html

lunar_day = Variable(value = 655.7208,
                     units = "hrs",
                     name = "lunar_day",
                     track = False,
                     description = "the length of a day (sunlight + darkness) on the lunar surface")


solar_irradiance_constant = Variable(value = 1361.0,
                                     units = "W", # The code does not recognize W/m2 as a unit.
                                     name = "solar_irradiance_constant",
                                     track = False,
                                     description = "solar irradiance constant")

moon.add_children([lunar_day, solar_irradiance_constant])

######################### Defining Time ########################################

# How do I connect t -> time to clock
# t = np.arange(0, round(lunar_day.value), 1).tolist()

######################### Crew ################################################
"""
crew = Node(name = "crew", description = "characteristics to the crew")

crew1 = Variable(name = "Rashi Jain",
                 description = "Mission Specialist",
                 track = True)
"""
######################## Power Loads ############################################

# Input from crew, systems, and contigency loads.
total_habitat_power_load = Variable(value = 9.5,# This value would be an addition of several values.
                                    units = 'kW',
                                    name = "total_habitat_power_required",
                                    track = True,
                                    description = "currently the approximate power load of one crew")


# It might make better sense to put
#total_habitat_power_required = Variable(value = power_required,
                                        #units = '',
                                        #name = "total_habitat_power_required",
                                        #true = True,
                                        #description = "calculated from total_habitat_power_load that needs to be catered for over a period of time")


######################### Power Systems ########################################
power_systems = Node(name = "power_systems", description = "build-up of power systems")

####################### Power Generation #######################################
power_generation = Node(name = "power_generation", description = "all power generation systems")
power_systems.add_child(power_generation)

####################### Solar Power System #####################################
solar_power = Node(name = "solar_power", description = "includes all examples of solar power (and further components of examples)")
power_generation.add_child(solar_power)

############ Solar Power System Example I
solar_arrays = Node(name = "solar_Arrays", description = "photo voltaic arrays")
solar_power.add_child(solar_arrays);

dummy = 1.0
power_density = Variable(value = dummy,
                         units = "", # W/m3 not a viable unit
                         name = "power_density",
                         track = True,
                         description = "power desnsity of the solar array system")

energy_density = Variable(value = dummy,
                          units = "", #Wh/m3 not a viable unit
                          name = "energy_density",
                          track = True,
                          description = "energy density of the solar power arrays")

specific_energy = Variable(value = dummy,
                           units = "",
                           name = "specific_energy",
                           track = True,
                           description = "specific energy of the solar power arrays");

# These are the examples where I talk of applicability for different node cases.
# Other variables: Reliability, Efficiency, Beginning of LIfe, End of Life, Degradation (Aging Context), etc.
# We'd need to develop a database for the same.

###################### Power Distribution ######################################
power_distribution = Node(name = "power_distribution", description = "all power distriution elements")

sequential_shunt_unit = Node(name = "sequential_shunt_unit", description = "regulates output to an acceptable 160 VdC")
direct_current_switching_unit = Node(name = "direct_current_switching_unit", description = "connectivity between power source and battery systems as well as distributing power to loads.")
battery_charge_discharge_unit = Node(name = "regulates charge rate of battery and maintains bus voltage of 151 VdC during an eclipse by discharging batteries")

power_distribution.add_children([sequential_shunt_unit, direct_current_switching_unit, battery_charge_discharge_unit])
