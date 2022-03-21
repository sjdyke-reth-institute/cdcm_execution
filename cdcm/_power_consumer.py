"""A class representing a power consumer.

Author:
    Ilias Bilionis

Date:
    3/21/2022

"""


__all__ = ["PowerConsumer"]


from . import System, PhysicalStateVariable


class PowerConsumer(System):
    """A class representing a power consumer.

    We operate under the assumption that the required power to operate
    during the next timestep is known and stored in a physical state
    variable named `required_power`.

    Furthermore, the power consumer should accept a binary signal from a
    `PowerDistributionNetwork` that indicates whether or not there is
    enough power to operate during the next timestep. This is 
    essentially a parent that corresponds to a physical state variable
    in a `PowerDistributionNetwork`. 

    See `System` for the definition for the rest of the keyword 
    arguments.
    """

    def __init__(
        self,
        name="power_generator",
        state={},
        parameters={},
        parents={},
        description=""
    ):
        required_power = PhysicalStateVariable(
            value=0.0,
            units="kWh",
            name="required_power",
            description="The power required to operate during the next"
                + " timestep."
        )
        state.update(
            {
                "required_power": required_power
            }
        )
        super().__init__(
            name=name,
            state=state,
            parameters=parameters,
            parents=parents,
            description=description
        )


class ConstantPowerConsumer(PowerConsumer):
    """A class representing a 