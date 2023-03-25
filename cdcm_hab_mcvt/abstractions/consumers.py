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


resource_consumed_during_time [t, t+dt] = resource_required_per_unit_time * dt
                                            if resource_supplied_per_unit_time > resource_required_per_unit_time
                                               and switch is on
                                          0.0 otherwise

"""

__all__ = ["make_resource_consumer"]

from cdcm import *
from typing import Union

from .common import *

Scalar = Union[int, float]


def make_resource_consumer(
    name_or_system: Union[str, System],
    dt: Parameter,
    in_resource_name: str,
    in_resource_units: str,
    in_resource_value: float = 0.0,
    in_resource_req: float = 0.0,
    **kwargs
):

    sys = make_system(name_or_system, **kwargs)
    with sys:
        resource_req = Parameter(
            name=in_resource_name + "_rate_required",
            value=in_resource_req,
            units=in_resource_units,
        )

        resource_supplied = Variable(
            name=in_resource_name + "_rate_supplied",
            value=in_resource_value,
            units=in_resource_units,
        )

        switch = Variable(
            name=in_resource_name + "_switch",
            value=1,
            units="",
            description="The switch is on (value=1) if there is"
            + " enough power supplied. Otherwise it is"
            + " off (value=0).",
        )

        resource_consumed = Variable(
            name=in_resource_name + "_consumed",
            value=0.0,
            units=in_resource_units + dt.units,
        )

        @make_function(resource_consumed)
        def calculate_consumed_resource(
            s=switch, r_req=resource_req, r_in=resource_supplied, dt=dt
        ):
            if s == 0:
                return 0.0
            else:
                if r_in > r_req:
                    return r_req * dt
                else:
                    return 0.0

    return sys

def make_resource_generator(
        name_or_system: Union[str, System],
        dt: Parameter,
        out_resource_name: str,
        out_reseource_value: Scalar = 0.,
        out_resource_req: Scalar = 0.,
        ) -> System:
    """Make a resource generator"""

    

    pass

def make_power_consumer(
    name_or_system: Union[str, System],
    dt: Parameter,
    in_power_value: float = 0.0,
    in_power_req: float = 0.0,
    energy_to_heat_coefficient_value: float = 0.0,
    **kwargs
):
    sys = make_resource_consumer(
        name_or_system, dt, "energy", "W", in_power_value, in_power_req, **kwargs
    )

    with sys:
        energy_to_heat_coefficient = Parameter(
            name="energy_to_heat_coefficient",
            value=energy_to_heat_coefficient_value,
            units="",
        )
        heat_gain = Variable(
            name="heat_gain",
            value=0.0,
            units=sys.energy_consumed.units,
            description="Heat dissipated to the environment as heat.",
        )

        @make_function(heat_gain)
        def calculate_heat_gain(
            eta=energy_to_heat_coefficient, energy=sys.energy_consumed, dt=dt
        ):
            return eta * energy * dt

    return sys


if __name__ == "__main__":
    clock = make_clock(dt=0.5, units="h")
    energy_consumer = make_power_consumer("laptop_01", clock.dt, 50.0, 10.0, 0.5)
    energy_consumer2 = make_power_consumer("laptop_02", clock.dt, 50.0, 10.0, 0.5)
    energy_consumer.energy_switch.value = 0
    energy_consumer.forward()
    print(energy_consumer)
    energy_consumer.energy_switch.value = 1
    energy_consumer.forward()
    print(energy_consumer)
    energy_consumer.energy_switch.value = 1
    energy_consumer.energy_rate_supplied.value = 5
    energy_consumer.forward()
    print(energy_consumer)
    # oxygen_consumer = make_resource_consumer("human", "oxygen", "kg/m^3")
