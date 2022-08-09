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
from ..common import *


def make_resource_consumer(name_or_system : Union[str,System],
                           in_resource_name : str,
                           in_resource_units : str,
                           in_resource_value : float = 0.0,
                           resource_req      : float = 0.0):

    sys = maybe_make_system(name_or_system, **kwargs)
    with sys:
        resource_req = Parameter(name=in_resource_name + "_required",
                                 value=resource_req,
                                 units=in_resource_units)

        resource_supplied = Variable(name=in_resource_name + "_supplied",
                                     value=in_resource_value,
                                     units=in_resource_units)

        switch = Variable(name="switch", value=1, units="",
                          description="The switch is on (value=1) if there is"
                                      + " enough power supplied. Otherwise it is"
                                      + " off (value=0).")

        resource_consumed = Variable(name=resource_name + "_consumed",
                                     value=resource_req,
                                     units=resource_units)

        @make_function(resource_consumed)
        def calculate_consumed_resource(s=switch,
                                        r_req=resource_req,
                                        r_in=resource_supplied):
            if s == 0:
                return 0.0
            else:
                if r_in > r_req:
                    return r_req
                else:
                    return 0.0



    return sys


if __name__ == "__main__":
    energy_consumer = make_resource_consumer("solar", "energy", "W")
    energy_consumer.switch.value = 0
    print(energy_consumer)
    energy_consumer.switch.value = 1
    print(energy_consumer)
    #oxygen_consumer = make_resource_consumer("human", "oxygen", "kg/m^3")
