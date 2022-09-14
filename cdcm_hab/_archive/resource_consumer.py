"""

"""


__all__ = ["make_resource_consumer"]


from cdcm import *
from typing import Union

from common import maybe_make_system


def make_resource_consumer(
    name_or_system: Union[str, System],
    resource_name: str,
    resource_units: str,
    resource_default_value: float = 0.0,
    **kwargs
):
    sys = maybe_make_system(name_or_system, **kwargs)
    with sys:
        resource_supplied = Variable(
            name=resource_name + "_supplied",
            value=resource_default_value,
            units=resource_units,
        )
        resource_consumed = Variable(
            name=resource_name + "_consumed",
            value=resource_default_value,
            units=resource_units,
        )
    return sys


if __name__ == "__main__":
    energy_consumer = make_resource_consumer("solar", "energy", "W")
    oxygen_consumer = make_resource_consumer("human", "oxygen", "kg/m^3")
