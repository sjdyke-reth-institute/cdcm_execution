"""Write me."""


__all__ = ["make_solar"]


from cdcm import *
from typing import Union

from physical_object import *
from resource_generator import *


def make_solar(
    name_or_system: Union[str, System],
    irradiance: Variable,
    area: float,
    eta: float,
    **kwargs,
):
    print(name_or_system)
    sys = make_resource_generator(
        make_physical_system(name_or_system), irradiance, "power", "W"
    )
    with sys:
        area = Parameter(name="area", value=area, units="m^2")
        efficiency = Variable(name="efficiency", value=eta, units="")

        @make_function(solar.power_output)
        def calculate_power(I=solar.irradiance, A=area, eta=efficiency):
            return A * eta * I

    return sys


if __name__ == "__main__":
    with System(name="moon") as moon:
        irradiance = Variable(
            name="irradiance",
            units="W/m^2",
            value=1000.0,
            description="Dummy irradiance",
        )

    with System(name="solar_array") as sa:
        for i in range(10):
            si = make_solar(f"solar_{i}", moon.irradiance, 10.0, 1.0)
            si.x.value = 0.0
            si.y.value = i * 10.1

    print(sa)
