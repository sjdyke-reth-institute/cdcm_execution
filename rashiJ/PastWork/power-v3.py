"""
This is version 2 of the power system.

Author:
    Rashi Jain

Date:
    07/22/2022
    07/26/2022

Notes:

Code Comment:
    Code begins on Line 21.
    This is the version 2 of Power Systems.


Edits by Prof. Bilionis:
    Guide to wiritng abstractions.

"""

## Installing dictionaries
from cdcm import *
import numpy as np

# from physical_object import *

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

                    with System(name="solar_array",
                        description="Solar arrays assembly") as solar_array:

                        num_solar_array_assemblies=Variable(
                            value=0.0,
                            units="na",
                            name="num_solar_array_assemblies",
                            track=True,
                            description="number of solar panel assemblies associated with the habitat"
                        )

                        with System(name="solar_array_1",
                            description="solar arrays assembly #1") as solar_array_1:

                            solar_array_ID=Variable(
                                value="solar_array_1",
                                units="na",
                                name="solar_array_ID",
                                track=True,
                                description="Unique ID for solar array assembly(i)"
                            )

                            effective_area=Variable(
                                value=0.0,
                                units="m^2",
                                name="effective_surface_area",
                                track=True,
                                description="Effective surface area occupied by solar arrays"
                            )

                            aging_factor=Variable(
                                value=0.0,
                                units="na",
                                name="aging_factor",
                                track=True,
                                description="Aging factor is the percentage/year of degradation for solar panels"
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

                            current_out=Variable(
                                value=0.0,
                                units="A",
                                name="current_out",
                                track=True,
                                description="Current output from solar arrays "
                            )

                            voltage_out=Variable(
                                value=0.0,
                                units="V",
                                name="voltage_out",
                                track=True,
                                description="Voltage output from solar arrays"
                            )

                            power=Variable(
                                value=0.0,
                                units="W",
                                name="power",
                                track=True,
                                description="Power generated by arrays"
                            )

                            energy=Variable(
                                value=0.0,
                                units="Wh",
                                name="energy",
                                track=True,
                                description="Energy generated by solar arrays"
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

                            power_required=Variable(
                                value=0.0,
                                units="W",
                                name="power_required",
                                track=True,
                                description="Power requried for solar array assembly"
                            )

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
                        track=True,
                        description="Number of SSU's available on-board at any given time"
                    )

                    with System(name="ssu1",
                    description = "ssu #1") as ssu1:

                        ssu_ID=Variable(
                            value="ssu1",
                            units="na",
                            name="ssu_ID",
                            track=True,
                            description="Unique ID for ssu(i)"
                        )

                        ssu_status=Variable(
                            value="on",
                            units="na",
                            name="ssu_status",
                            track=True,
                            description="Identifies whether ssu(i) is on or off"
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

                        current_in=Variable(
                            value=0.0,
                            units="A",
                            name="current_flow",
                            track=True,
                            description="Current in to ssu1"
                        )

                        current_out=Variable(
                            value=0.0,
                            units="A",
                            name="current_out",
                            track=True,
                            description="Current out of ssu1"
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
                            description="Voltage out of ssu1"
                        )

                        power_required=Variable(
                            value=0.0,
                            units="W",
                            name="power_required",
                            track=True,
                            description="Power required by sequential_shunt_unit"
                        )

                with System(name="direct_current_switching_unit",
                    description="Connection between the power source and battery system as well as distributing power to different loads") as dcsu:

                    num_dcsu=Variable(
                        value=0.0,
                        units="na",
                        name="num_dcsu",
                        track=True,
                        description="Number of dcsu's available"
                        )

                    with System(name="dcsu1", description="dcsu #1") as dcsu1:

                        dcsu_ID=Variable(
                            value="dcsu1",
                            units="na",
                            name="dcsu_ID",
                            track=True,
                            description="Unique ID for dcsu(i)"
                        )

                        dcsu_status=Variable(
                            value="on",
                            units="na",
                            name="dcsu_status",
                            track=True,
                            description="Identifies whether dcsu(i) is on or off"
                        )

                        power_from_source=Variable(
                            value=0.0,
                            units="W",
                            name="power_from_source",
                            track=True,
                            description="Power in at dcsu1"
                        )

                        energy_from_source=Variable(
                            value=0.0,
                            units="Wh",
                            name="energy_from_source",
                            track=True,
                            description="Energy in at dcsu1"

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
                            description="Reliability of dcsu1"
                        )

                        efficiency=Parameter(
                            value=0.0,
                            units="na",
                            name="efficiency",
                            track=False,
                            description="Efficiency of dcsu1"
                        )

                        percentage_to_storage=Variable(
                            value=0.0,
                            units="na",
                            name="percentage_to_storage",
                            track=True,
                            description="Monitors the percentage of the power directed to storage systems"
                        )

                        percentage_to_distribution=Variable(
                            value=0.0,
                            units="na",
                            name="percentage_to_distribution",
                            track=True,
                            description="Monitors the percentage of the power directed to distribution to different loads"
                        )

                        power_loss=Variable(
                            value=0.0,
                            units="na",
                            name="power_loss",
                            track=True,
                            description="Calculates power loss at any given point between source and power delievered to storage and distribution"
                        )

                        current_in = Variable(
                            value=0.0,
                            units="A"
                            name="current_in",
                            track=True,
                            description="Current input for DCSU"
                        )

                        power_required=Variable(
                            value=0.0,
                            units="W",
                            name="power_required",
                            track=True,
                            description="Power requried for dscu to function"
                        )

                with System(name="battery_charge_discharge_unit",
                    description="Regulates charge rate and mainains bus voltage of 151VdC during an eclipse by discharging the batteries") as bcdu:

                    num_bcdu=Variable(
                        value=0.0,
                        units="na",
                        name="num_bcdu",
                        track=True,
                        description="Number of bcdu's available"
                    )

                    with System(name="bcdu1", description="bcdu #1") as bcdu1:

                        bcdu_ID=Variable(
                            value="bcdu1",
                            units="na",
                            name="bcdu_ID",
                            track=True,
                            description="Unique ID for bcdu(i)"
                        )

                        bcdu_status=Variable(
                            value="on"
                            units="na",
                            name="bcdu_status",
                            track=True,
                            description="Identifies wether bcdu(i) is on or off or in a hazard state"
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
                            description="Reliability of dcsu1"
                        )

                        efficiency=Parameter(
                            value=0.0,
                            units="na",
                            name="efficiency",
                            track=False,
                            description="Efficiency of dcsu1"
                        )

                        battery_charge_rate=Variable(
                            value=0.0,
                            units="W",
                            name="battery_charge_rate",
                            track=True,
                            description="Charge rate of battery connected to bcdu"
                        )

                        battery_discharge_rate=Variable(
                            value=0.0,
                            units="W",
                            name="battery_discharge_rate",
                            track=True,
                            description="Discharge rate of battery connected to bcdu at eclipse"
                        )

                        current_in=Variable(
                            value=0.0,
                            units="A",
                            name="current_in",
                            track=True,
                            description="Current in to bcdu1"
                        )

                        current_out=Variable(
                            value=0.0,
                            units="A",
                            name="current_out",
                            track=True,
                            description="Current out to bcdu1"
                        )

                        voltage_in=Variable(
                            value=0.0,
                            units="V",
                            name="volatge_in",
                            track=True,
                            description="Voltage in to bcdu1"
                        )

                        voltage_out=Variable(
                            value=0.0,
                            units="V",
                            name="voltage_out",
                            track=True,
                            description="Voltage out to bcdu1"
                        )

                        power_required=Variable(
                            value=0.0,
                            units="A",
                            name="power_required",
                            track=True,
                            description="Power required by bcdu"
                        )

                        batteries_connect=Variable(
                            value=0.0,
                            units="na",
                            name="batteries_connect",
                            track=True,
                            description="IDs of battery connected to specified bcdu"
                        )

                with System(name="dc_2_dc_converter",
                    description="Converts the primary input voltage to a regulated 124VdC as specified for user loads") as ddcu:

                    num_ddcu=Variable(
                        value=0.0,
                        units="na",
                        name="num_ddcu",
                        track=True,
                        description="Number of DDCU's available on-board at any given time"
                    )

                    with System(name="ddcu1",
                    description = "ddcu #1") as ssu1:

                        ddcu_ID=Variable(
                            value="ddcu1",
                            units="na",
                            name="ddcu_ID",
                            track=True,
                            description="Unique ID for ddcu(i)"
                        )

                        ddcu_status=Variable(
                            value="on",
                            units="na",
                            name="ddcu_status",
                            track=True,
                            description="Identifies whether ddcu(i) is on or off"
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
                            description="Reliability of the ddcu1"
                        )

                        efficiency=Parameter(
                            value=0.0,
                            units="na",
                            name="efficiency",
                            track=False,
                            description="Efficiency of the ddcu1"
                        )

                        current_in=Variable(
                            value=0.0,
                            units="A",
                            name="current_in",
                            track=True,
                            description="Current in to ddcu1"
                        )

                        current_out=Variable(
                            value=0.0,
                            units="A",
                            name="current_out",
                            track=True,
                            description="Current out of ddcu1"
                        )

                        voltage_in=Variable(
                            value=0.0,
                            units="V",
                            name="voltage_in",
                            track=True,
                            description="Voltage in to ddcu1"
                        )

                        voltage_out=Variable(
                            value=0.0,
                            units="V",
                            name="voltage_out",
                            track=True,
                            description="Voltage out of ddcu1"
                        )

                        power_required=Variable(
                            value=0.0,
                            units="W",
                            name="power_required",
                            track=True,
                            description="Power required by ddcu"
                        )

                        rpcm_connect=Variable(
                            value=0.0,
                            units="na",
                            name="rpcm_connect"
                            track=True,
                            description="IDs of rpcms connected to specified ddcu"
                        )

                with System(name="remote_power_controller_module",
                    description="Contains individual switches called RPCs which are remotely commandable to apply or remove power to downstream user loads") as rpcm:

                    num_rpcm=Variable(
                        value=0.0,
                        units="na",
                        name="num_rpcm",
                        track=True,
                        description="Number of RPCM's available on board at any given time"
                    )

                    with System(name="rpcm1", description="rpcm #1") as rpcm1:

                        rpcm_ID=Variable(
                            value="rpcm1",
                            units="na",
                            name="rpcm_ID",
                            track=True,
                            description="Unique ID for rpcm(i)"
                        )

                        rpcm_status=Variable(
                            value="on",
                            units="na",
                            name="rpcm_status",
                            track=True,
                            description="Identifies whether the rpcm(i) is on or off or stored or in a hazard state"
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
                            description="Reliability of the rpcm1"
                        )

                        efficiency=Parameter(
                            value=0.0,
                            units="na",
                            name="efficiency",
                            track=False,
                            description="Efficiency of the rpcm1"
                        )

                        current_in=Variable(
                            value=0.0,
                            units="A",
                            name="current_in",
                            track=True,
                            description="Current in to rpcm1"
                        )

                        current_out=Variable(
                            value=0.0,
                            units="A",
                            name="current_out",
                            track=True,
                            description="Current out of rpcm1"
                        )

                        voltage_in=Variable(
                            value=0.0,
                            units="V",
                            name="voltage_in",
                            track=True,
                            description="Voltage in to rpcm1"
                        )

                        voltage_out=Variable(
                            value=0.0,
                            units="V",
                            name="voltage_out",
                            track=True,
                            description="Voltage out of rpcm1"
                        )

                        power_required=Variable(
                            value=0.0,
                            units="W",
                            name="power_required",
                            track=True,
                            description="Power required by rpcm"
                        )

                        loads_connect=Variable(
                            value=0.0,
                            units="na",
                            name="loads_connect",
                            track=True,
                            description="Connected Loads to specified RPCM"
                        )

                with System(name="electronics_control_unit",
                    description="Controller for beta gimbal (for solar arrays)") as ecu:

                    num_ecu=Variable(
                        value=0.0,
                        units="na",
                        name="num_ecu",
                        track=True,
                        description="Number of ecu's on board at any given time"
                    )

                    with System(name="ecu1", description="ecu #1") as ecu1:

                        ecu_ID=Variable(
                            value="ecu1",
                            units="na",
                            name="ecu_ID",
                            track=True,
                            description="Unique ID for ecu(i)"
                        )

                        ecu_status=Variable(
                            value="on",
                            units="na",
                            name="ecu_status",
                            track=True,
                            description="Identifies whether ecu(i) is on or off or stored or in a hazard state"
                        )

                        aging_factor=Variable(
                            value=0.0,
                            units="na",
                            name="aging_factor",
                            track=True,
                            description="Aging factor in percentage/year"
                        )

                        reliability=Parameter(
                            value=0.0,
                            units="na",
                            name="reliability",
                            track=False,
                            description="Reliability of ecu1"
                        )

                        effciency=Parameter(
                            value=0.0,
                            units="na",
                            name="efficiency",
                            track=False,
                            description="Efficiency fo ecu1"
                        )

                        current_in=Variable(
                            value=0.0,
                            units="A",
                            name="current_in",
                            track=True,
                            description="Current in to ecu1"
                        )

                        voltage_in=Variable(
                            value=0.0,
                            units="V",
                            name="voltage_in",
                            track=True,
                            description="Voltage in to ecu1"
                        )

                        power_required=Variable(
                            value=0.0,
                            units="W",
                            name="power_required",
                            track=True,
                            description="Power required by ecu1"
                        )

                        beta_gimbal_controller=Variable(
                            value=0.0,
                            units="degree",
                            name="beta_gimbal_controller",
                            track=True,
                            description="Beta gimbal output"
                        )

                with System(name="pump_flow_controller_subassembly",
                    description="Pump system that provides cooling to the dcsu, bcdu's and batteries") as pfcs:

                    num_pfcs=Variable(
                        value=0.0,
                        units="na",
                        name="num_pfcs",
                        track=True,
                        description="Number of pfcs's on board at any given time"
                    )

                    with System(name="pfcs1", description="pfcs #1") as ecu1:

                        pfcs_ID=Variable(
                            value="pfcs1",
                            units="na",
                            name="pfcs_ID",
                            track=True,
                            description="Unique ID for pfcs(i)"
                        )

                        pfcs_status=Variable(
                            value="on",
                            units="na",
                            name="pfcs_status",
                            track=True,
                            description="Identifies whether pfcs(i) is on or off or stored or in a hazard state"
                        )

                        aging_factor=Variable(
                            value=0.0,
                            units="na",
                            name="aging_factor",
                            track=True,
                            description="Aging factor in percentage/year"
                        )

                        reliability=Parameter(
                            value=0.0,
                            units="na",
                            name="reliability",
                            track=False,
                            description="Reliability of pfcs1"
                        )

                        effciency=Parameter(
                            value=0.0,
                            units="na",
                            name="efficiency",
                            track=False,
                            description="Efficiency fo pfcs1"
                        )

                        current_in=Variable(
                            value=0.0,
                            units="A",
                            name="current_in",
                            track=True,
                            description="Current in to pfcs1"
                        )

                        power_required=Variable(
                            value=0.0,
                            units="W",
                            name="power_required",
                            track=True,
                            description="Power reqruied by pfcs1"
                        )

                with System(name="main_bus_switching_unit",
                    description="Provides connectivity between a power channel and multiple downstream paths. It also allows for cross-connecting power channels in an event of a failure") as mbsu:

                    num_mbsu=Variable(
                        value=0.0,
                        units="na",
                        name="num_mbsu",
                        track=True,
                        description="Number of mbsu's on board at any given time"
                    )

                    with System(name="mbsu1", description="mbsu #1") as mbsu1:

                        mbsu_ID=Variable(
                            value="pfcs1",
                            units="na",
                            name="mbsu_ID",
                            track=True,
                            description="Unique ID for mbsu(i)"
                        )

                        mbsu_status=Variable(
                            value="on",
                            units="na",
                            name="mbsu_status",
                            track=True,
                            description="Identifies whether mbsu(i) is on or off or stored or in a hazard state"
                        )

                        aging_factor=Variable(
                            value=0.0,
                            units="na",
                            name="aging_factor",
                            track=True,
                            description="Aging factor in percentage/year"
                        )

                        reliability=Parameter(
                            value=0.0,
                            units="na",
                            name="reliability",
                            track=False,
                            description="Reliability of mbsu1"
                        )

                        effciency=Parameter(
                            value=0.0,
                            units="na",
                            name="efficiency",
                            track=False,
                            description="Efficiency fo mbsu1"
                        )

                        current_in=Variable(
                            value=0.0,
                            units="A",
                            name="current_in",
                            track=True,
                            description="Current in to mbsu1"
                        )

                        current_out=Variable(
                            value=0.0,
                            units="A",
                            name="current_out",
                            track=True,
                            description="Current out to mbsu1"
                        )

                        voltage_in=Variable(
                            value=0.0,
                            units="A",
                            name="voltage_in"
                            track=True,
                            description="Voltage in to mbsu1"
                        )

                        voltage_out=Variable(
                            value=0.0,
                            units="V",
                            name="voltage_out",
                            track=True,
                            description="Voltage out of mbsu1"
                        )

                        power_required=Variable(
                            value=0.0,
                            units="W",
                            name="power_required",
                            track=True,
                            description="Power required by mbsu1"
                        )

                        ddcu_connect=Variable(
                            value=0.0,
                            units="na",
                            name="ddcu_connect"
                            track=True,
                            description="IDs of ddcu connected to the specified mbsu"
                        )


            with System (name="power_storage",
                description="Different power storage options") as power_storage:
                pass


#Testing the Sanity of the Code
print(everything)
