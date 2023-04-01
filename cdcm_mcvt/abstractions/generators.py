# ovn!
"""
Make systems that are resource generators.

All resource generators take in some form of energy, and have a mechanism
for converting that input energy to some useful output energy. This is done
via some parameters (or mechanism) that are defined within the system.
During conversion some energy is dissipated as heat.

                  ||========================||
                  || On or Off              ||
Input Energy ---->|| Transformation Factor  || ----> Output Energy
                  ||                        || ----> Power Dissipated
                  ||========================||

A resource generator is defined by following variables:

    + resource_input         -- The input energy resource
    + switch                 -- Resource Generator: on-off switch
    + transformative_factor  -- Transformative factor(s) of the physical object
    + resource_output        -- The output resource energy
    + power_dissipated       -- Power dissipated as heat.
"""

__all__ = ["make_resource_generator"]

from cdcm import *
from typing import Union

from cdcm_abstractions import *


def make_resource_generator_new():
    # wrapper function around a resource consumer
    # all it needs to do it supply resource_consumer with negative units
    raise NotImplementedError("Implement me..")

def make_resource_generator(
    name_or_system: Union[str, System],
    dt: Parameter,
    out_resource_name: str,
    out_resource_units: str,
    out_resource_value: float = 0.0,
    out_resource_req: float = 0.0,
    **kwargs
):
    """Make a resource generator
    """

    with maybe_make_system(name_or_system, **kwargs) as resource_generator:

        # Add a switch to resource_generator
        switch = Variable(
            name=out_resource_name + "_switch",
            value=1,
            units="",
            description="The switch is on (value=1) if there is"
            + " enough power supplied. Otherwise it is"
            + " off (value=0).",
        )
        resource_req = Parameter(
            name=out_resource_name + "_rate_required",
            value=out_resource_req,
            units=out_resource_units,
        )

        resource_supplied = Variable(
            name=out_resource_name + "_rate_supplied",
            value=out_resource_value,
            units=out_resource_units,
        )

        resource_generated = Variable(
            name=out_resource_name + "_generated",
            value=0.0,
            units=out_resource_units + dt.units,
        )

        @make_function(resource_generated)
        def calculate_generated_resource(
            s=switch, r_req=resource_req, r_in=resource_supplied, dt=dt
        ):
            """Calculate generated resource"""

            if s == 0:
                return 0.0
            else:
                if r_in > r_req:
                    return r_in * dt
                else:
                    return 0.0

    return resource_generator


def make_power_generator(
    name_or_system: Union[str, System],
    dt: Parameter,
    out_power_value: float = 0.0,
    out_power_req: float = 0.0,
    energy_to_heat_coefficient_value: float = 0.0,
    **kwargs
):
    """Make a power generator abstraction"""
    power_generator = make_resource_generator(
        name_or_system, dt, "energy", "W", out_power_value, out_power_req, **kwargs
    )

    with power_generator:
        energy_to_heat_coefficient = Parameter(
            name="energy_to_heat_coefficient",
            value=energy_to_heat_coefficient_value,
            units="",
        )
        heat_gain = Variable(
            name="heat_gain",
            value=0.0,
            units=power_generator.energy_generated.units,
            description="Heat dissipated to the environment as heat.",
        )

        @make_function(heat_gain)
        def calculate_heat_gain(
            eta=energy_to_heat_coefficient,
            energy=power_generator.energy_generated,
            dt=dt,
        ):
            """Dissipation loss"""
            return eta * energy * dt

    return power_generator