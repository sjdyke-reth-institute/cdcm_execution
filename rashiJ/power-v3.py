"""
This is version 2 of the power system.

Author:
    Rashi Jain

Date:
    07/22/2022

Notes:

Code Comment:
    Code begins on Line 21.
    This is the version 2 of Power Systems.
    A more complete model following this shall be ready by Monday.
    Adding some abstractions.
"""

## Installing dictionaries
from cdcm import *
import numpy as np

from physical_object import *

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
                description="Solar irradiance received by the moon"
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
    with System (name="habitat",
        description="Houses the habitat.") as habitat:

        # Defining Power Systems
        with System (name="power",
            description="Houses habitat's power systems") as power:

            # Power Generation System: power, energy, power_density, energy_density,
            # specific energy
            with System (name="power_generation",
                description="Different power generation options") as power_generation:

                power=Variable(
                    value=0.0,
                    units="W",
                    name="power",
                    track=True,
                    description="Power produced by the power generation system/systems"
                )

                energy=Variable(
                    value=0.0,
                    units="Wh",
                    name="energy",
                    track=True,
                    description="Energy produced by the power generation system/systems"
                )

                power_density=Variable(
                    value=0.0,
                    units="W/m^3",
                    name="power_density",
                    track=True,
                    description="Power density of the input power generation system/systems"
                )

                energy_denstiy=Variable(
                    value=0.0,
                    units="Wh/m^3",
                    name="energy_denstiy",
                    track=True,
                    description="Energy density of the input power generation system/systems"
                )

                specific_energy=Variable(
                    value=0.0,
                    units="Wh/kg",
                    name="specific_energy",
                    track=True,
                    description="Specific energy of the input power generation system/systems"
                )

                # Solar Power Generation Options
                with System(name="solar",
                    description="Solar power generation options") as solar:

                    # Specific power generation options: Solar Arrays
                    # While solar arrays could be further divided into solar panels and inverters
                    # this code only considers solar arrays as the object.
                    # defined by: x, y, z, lenght, width, height, surface_area, effective_surface_area
                    # volume, mass, aging_factor, reliability, and efficiency, power, energy
                    # power_density, energy_density and specific_energy

                    with System(name="solar_arrays",
                        description="Solar arrays assembly") as solar_arrays:

                        x=Variable(
                            value=0.0,
                            units="m",
                            name="x",
                            track=False,
                            description="x coordinate of solar arrays"
                        )

                        y=Variable(
                            value=0.0,
                            units="m",
                            name="y",
                            track=False,
                            description="y coordinate of solar arrays"
                        )

                        z=Variable(
                            value=0.0,
                            units="m",
                            name="z",
                            track=False,
                            description="z coordinate of solar arrays"
                        )

                        length=Parameter(
                            value=0.0,
                            units="m",
                            name="length",
                            track=False,
                            description="Ground length 1 of the solar arrays"
                        )

                        width=Parameter(
                            value=0.0,
                            units="m",
                            name="width",
                            track=False,
                            description="Ground length 2 of the solar arrays"
                        )

                        height=Parameter(
                            value=0.0,
                            units="m",
                            name="height",
                            track=False,
                            description="Vertical dimension of the solar arrays"
                        )

                        surface_area=Parameter(
                            value=0.0,
                            units="m^2",
                            name="surface_area",
                            track=False,
                            description="Surface area occupied by the solar arrays"
                        )

                        effective_surface_area=Variable(
                            value=0.0,
                            units="m^2",
                            name="effective_surface_area",
                            track=True,
                            description="Effective surface area occupied by solar arrays"
                        )

                        volume=Parameter(
                            value=0.0,
                            units="m^3",
                            name="volume",
                            track=False,
                            description="Volume occupied by the solar arrays"
                        )

                        mass=Variable(
                            value=0.0,
                            units="kg",
                            name="mass",
                            track=True,
                            description="Mass of the solar arrays"
                        )

                        aging_factor=Variable(
                            value=0.0,
                            units="na",
                            name="aging_factor",
                            track=True,
                            description="Aging factor is the percentage/year"
                        )

                        reliability=Parameter(
                            value=0.0,
                            units="na",
                            name="reliability",
                            track=False,
                            description="Reliability of the solar arrays"
                        )

                        efficiency=Parameter(
                            value=0.0,
                            units="na",
                            name="efficiency",
                            track=False,
                            description="Efficiency of the solar arrays"
                        )

                        power=Variable(
                            value=0.0,
                            units="W",
                            name="power",
                            track=True,
                            description="Power generated by solar panels"
                        )

                        energy=Variable(
                            value=0.0,
                            units="Wh",
                            name="energy",
                            track=True,
                            description="Energy generated by solar panels"
                        )

                        power_density=Variable(
                            value=0.0,
                            units="W/m^3",
                            name="power_density",
                            track=True,
                            description="Power density of the solar arrays"
                        )

                        energy_density=Variable(
                            value=0.0,
                            units="Wh/m^3",
                            name="energy_density",
                            track=True,
                            description="Energy density of the solar arrays"
                        )

                        specific_energy=Variable(
                            value=0.0,
                            units="Wh/kg",
                            name="specific_energy",
                            track=True,
                            description="Specific energy of the solar arrays"
                        )

                        @make_function(volume)
                        def calculate_volume(l = length, w = width, h = height):
                            return l*w*h

                        @make_function(surface_area)
                        def calculate_surface_area(l = length, w = width):
                            return l*w

                # Nuclear Power Generation Options
                with System (name="nuclear",
                    description="Nuclear power generation options") as nuclear:
                    pass

                # Chemical Power Generation Options.
                with System (name="chemical",
                    description="Chemical power generation options") as chemical:
                    pass

            # Power Distribution Options
            with System (name="power_distribution",
                description="Different power distribution configurations") as power_distribution:
                pass

                # Wiring takes care of wired/wireless infrastructure.
                with System(name="wiring",
                    description="This system contains wiring configurations") as wiring:
                    pass

                with System(name="sequential_shunt_unit",
                    description="Regulates output to 160VdC") as ssu:

                    num_ssu=Variable(
                        value=0.0,
                        units="na",
                        name="num_ssu",
                        track=Ture,
                        description="Number of SSU's available on-board at any given time"
                    )

                    with System(name="ssu1",
                    description = "Individual SSU unit") as ssu1:
                        x=Variable(
                            value=0.0,
                            units="m",
                            name="x",
                            track=False,
                            description="x coordinate of ssu1"
                        )

                        y=Variable(
                            value=0.0,
                            units="m",
                            name="y",
                            track=False,
                            description="y coordinate of ssu1"
                        )

                        z=Variable(
                            value=0.0,
                            units="m",
                            name="z",
                            track=False,
                            description="z coordinate of ssu1"
                        )

                        length=Parameter(
                            value=0.0,
                            units="m",
                            name="length",
                            track=False,
                            description="Ground length 1 of ssu1"
                        )

                        width=Parameter(
                            value=0.0,
                            units="m",
                            name="width",
                            track=False,
                            description="Ground length 2 of the ssu1"
                        )

                        height=Parameter(
                            value=0.0,
                            units="m",
                            name="height",
                            track=False,
                            description="Vertical dimension of the ssu1"
                        )

                        surface_area=Parameter(
                            value=0.0,
                            units="m^2",
                            name="surface_area",
                            track=False,
                            description="Surface area occupied by the ssu1"
                        )

                        effective_surface_area=Variable(
                            value=0.0,
                            units="m^2",
                            name="effective_surface_area",
                            track=True,
                            description="Effective surface area occupied by ssu1"
                        )

                        volume=Parameter(
                            value=0.0,
                            units="m^3",
                            name="volume",
                            track=False,
                            description="Volume occupied by the ssu1"
                        )

                        mass=Variable(
                            value=0.0,
                            units="kg",
                            name="mass",
                            track=True,
                            description="Mass of ssu1"
                        )

                        aging_factor=Variable(
                            value=0.0,
                            units="na",
                            name="aging_factor",
                            track=True,
                            description="Aging factor is the percentage/year"
                        )

                        reliability=Parameter(
                            value=0.0,
                            units="na",
                            name="reliability",
                            track=False,
                            description="Reliability of the ssu1"
                        )

                        efficiency=Parameter(
                            value=0.0,
                            units="na",
                            name="efficiency",
                            track=False,
                            description="Efficiency of the ssu1"
                        )

                        current_flow=Variable(
                            value=0.0,
                            units="A",
                            name="current_flow",
                            track=True,
                            description="Current flow through ssu1"
                        )

                        voltage_in=Variable(
                            value=0.0,
                            units="V",
                            name="voltage_in",
                            track=True,
                            description="Voltage in to ssu1"
                        )

                        voltage_out=Variable(
                            value=0.0,
                            units="V",
                            name="voltage_out",
                            track=True,
                            description="Voltage out through ssu1"
                        )

                        energy_density=Variable(
                            value=0.0,
                            units="Wh/m^3",
                            name="energy_density",
                            track=True,
                            description="Energy density of the solar arrays"
                        )

                        specific_energy=Variable(
                            value=0.0,
                            units="Wh/kg",
                            name="specific_energy",
                            track=True,
                            description="Specific energy of the solar arrays"
                        )

                with System(name="direct_current_switching_unit",
                    description="Connection between the power source and battery system as well as distributing power to different loads") as dcsu:
                    pass

                with System(name="battery_charge_discharge_unit",
                    description="Regulates charge rate and mainains bus voltage of 151VdC during an eclipse by discharging the batteries") as bcdu:
                    pass

                with System(name="dc_2_dc_converter",
                    description="Converts the primary input voltage to a regulated 124VdC as specified for user loads") as ddcu:
                    pass

                with System(name="remote_power_controller_module",
                    description="Contains individual switches called RPCs which are remotely commandable to apply or remove power to downstream user loads") as rpcm:
                    pass

                with System(name="electronics_control_unit",
                    description="Controller for beta gimbal (for solar arrays)") as ecu:
                    pass

                with System(name="pump_flow_controller_subassembly",
                    description="Pump system that provides cooling to the dcsu, bcdu's and batteries") as pfcs:
                    pass

                with System(name="main_bus_switching_unit",
                    description="Provides connectivity between a power channel and multiple downstream paths. It also allows for cross-connecting power channels in an event of a failure") as mbsu:
                    pass

            with System (name="power_storage",
                description="Different power storage options") as power_storage:
                pass


#Testing the Sanity of the Code
print(everything)
