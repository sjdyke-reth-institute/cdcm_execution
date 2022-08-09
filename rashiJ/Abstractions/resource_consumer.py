"""
Make systems that consume resources.

The idea of resource consumers is introduced for resources that are not infinite
For example solar power generators use solar energy (which is available infinite)
Therefore while describing solar panels, we do not categorize them as resource
consumers. However, we may do so for nuclear power generator, which uses some
nuclear agents to generate energy

                  ||========================||
                  || On or Off              ||
Input Energy ---->||                        || ----> Power Dissipated
                  ||                        ||
                  ||========================||

A resource consumer is defined by following variables:

    + resource_supplied      -- The input energy resource
    + switch                 -- Resource consumer: on-off switch
    + resource_consumed      -- The input energy consumed by the consumer
                                The energy consumed will usually be at some set
                                point for the consumer
    + power_dissipated       -- Power dissipated as heat.
"""

__all__ = ["make_resource_consumer"]

from cdcm import *
from typing import Union


def make_resource_consumer(name_or_system : Union[str,System],
                           in_resource_name : str,
                           in_resource_units : str,
                           in_resource_value : float = 0.0,
                           switch            : str,
                           resource_req      : float = 0.0):

    sys = maybe_make_system(name_or_system, **kwargs)
    with sys:

        if resource_supplied < resource_req:
            switch = "off"

        # Specify resource switch as "on" or "off"
        if switch == "on":
            # If switch is on, use values specified.
            resource_supplied = Variable(name=in_resource_name + "_supplied",
                                         value=in_resource_value,
                                         units=in_resource_units)

            resource_consumed = Variable(name=resource_name + "_consumed",
                                         value=resource_req,
                                         units=resource_units)

            @make_function(power_dissipated)
            def calculate_power_dissipated:
                return resource_supplied.value - resource_consumed.value

            power_dissipated = Variable(name="power_dissipated",
                                        value=power_dissipated,
                                        units=resource_units)
        else:
            resource_supplied = Variable(name=in_resource_name + "_supplied",
                                         value=0,
                                         units=in_resource_units)

            resource_consumed = Variable(name=in_resource_name + "_consumed",
                                         value=0,
                                         units=in_resource_units)

            power_dissipated = Variable(name="power_dissipated",
                                        value=0,
                                        units=in_resource_units)

    return sys


if __name__ == "__main__":
    energy_consumer = make_resource_consumer("solar", "energy", "W")
    oxygen_consumer = make_resource_consumer("human", "oxygen", "kg/m^3")
