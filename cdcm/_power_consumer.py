"""A class representing a power consumer.

Author:
    Ilias Bilionis

Date:
    3/21/2022

"""


__all__ = ["PowerConsumer"]


from . import System, PhysicalStateVariable, Parameter


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

    Keyword Arguments
    power_input --

    See `System` for the definition for the rest of the keyword
    arguments.
    """

    def __init__(
        self,
        power_input=None,
        name="power_consumer",
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


class DummyPowerConsumer(PowerConsumer):
    """A class representing a power consumer that requires constant
    power and does nothing.

    The system has an additional state called `operation_mode` which
    is either 'on' or 'off'.
    The system is always `on `if there is enough power. Otherwise, it is
    `off`.

    Keyword Arguments
    nominal_required_power -- The power required to operate this
                              consumer.
    name                   -- A name for this object.
    description            -- A description for the object.
    """

    def __init__(
        self,
        name="constant_power_consumer",
        nominal_required_power=5.0,
        description="A system that consumes energy without doing"
                    + " anything."
    ):
        assert isinstance(nominal_required_power, float)
        assert nominal_required_power >= 0.0
        nominal_required_power = Parameter(
            value=nominal_required_power,
            units="kWh",
            name="nominal_required_power_",
            description="The constant power required to operate."
        )
        operation_mode = PhysicalStateVariable(
            value="off",
            name="operation_mode",
            units="",
            description="Indicates if the system is `on` or `off`."
        )
        super().__init__(
            name=name,
            state=operation_mode,
            parameters=nominal_required_power,
            description=description
        )

    def _calculate_my_next_state(self, dt):
        self._next_state["required_power"] = (
            self.parameters["nominal_required_power"])
