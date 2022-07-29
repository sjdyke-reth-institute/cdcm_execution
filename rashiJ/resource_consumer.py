"""
Write me.
"""


from cdcm import *
from typing import Union


def make_resource_consumer(name_or_system : Union[str,System],
                           resource_name : str,
                           resource_units : str,
                           resource_default_value : float = 0.0):
    if isinstance(name_or_system, str):
            # I am making a new system
        sys = System(name=name_or_system, **kwargs)
    elif isinstance(name_or_system, System):
            # I am just adding variables to an existing system
        sys = name_or_system
    else:
        raise ValueError(f"I do not know what to do with {type(name_or_system)}!")
    with sys:
        resource_supplied = Variable(name=resource_name + "_supplied",
                                     value=resource_default_value,
                                     units=resource_units)
        resource_consumed = Variable(name=resource_name + "_consumed",
                                     value=resource_default_value,
                                     units=resource_units)
    return sys


if __name__ == "__main__":
    energy_consumer = make_resource_consumer("solar", "energy", "W")
    oxygen_consumer = make_resource_consumer("human", "oxygen", "kg/m^3")
