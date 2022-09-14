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

from common import maybe_make_system


def make_resource_generator(name_or_system : Union[str,System],
                            resource_input : Variable,
                            resource_input_name : str,
                            resource_input_units : str,
                            switch : str,
                            transformative_factor : Variable,
                            resource_output : Variable,
                            resource_input_value : float = 0.0,
                            resource_input_local_name : Union[None, str] = None,
                            **kwargs):

    sys = maybe_make_system(name_or_system, **kwargs)
    with sys:
        if resource_input_local_name is None:
            local_input_name = resource_input.name
        else:
            local_input_name = resource_input_local_name

        resource_input_local_copy = Variable(name=local_input_name,
                                             units=resource_input.units,
                                             value=resource_input.value,
                                             description= resource_input.description)

        # Why are making it multiple times?
        # make(resource_input_local_copy)
        # def copy_resource_input(x = resource_input)
            # return x


        resource_output(name=resource_output.name,
                        value=resource_output.value,
                        units=resource_output.units)

        if switch == "on":
            pass
        else:
            pass
            
