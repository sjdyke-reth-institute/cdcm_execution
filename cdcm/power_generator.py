"""A class representing a power generator.

Author:
    Ilias Bilionis

Date:
    3/21/2022

"""


__all__ = ["PowerGenerator", "DummyPowerGenerator"]


from . import System, Parameter, PhysicalStateVariable


class PowerGenerator(System):
    """A class representing a power generator.

    A PowerGenerator has a physical state variable called
    `power_output`. The units of `power_output` are kWatt.
    The inheriting classes do not have to add that
    variable. It is already added. But the inheriting classes must
    make sure that they calculate `power_output` in the method
    `calculate_my_next_state()`.

    See `System` for the definition of the keyword arguments.
    """

    def __init__(
        self,
        name="power_generator",
        state={},
        parameters={},
        parents={},
        sub_systems={},
        description=""
    ):
        power_output = PhysicalStateVariable(
            value=0.0,
            name="power_output",
            units="kWh",
            description="The power output of the generator.",
            track=True
        )
        state.update({"power_output": power_output})
        super().__init__(
            name=name,
            state=state,
            parameters=parameters,
            parents=parents,
            sub_systems=sub_systems,
            description=description
        )


class DummyPowerGenerator(PowerGenerator):
    """This is a power generator that generates power out of thin air.

    Use it for test purposes only.

    Keyword Arguments:
    nominal_power_output -- The constant value of the power output in
                            kWh.

    See `System` for the definition of the keyword arguments.
    """

    def __init__(
        self,
        name="dummy_power_generator",
        nominal_power_output=10.0,
        description="A power generator that generates power out of nothing."
    ):
        assert isinstance(nominal_power_output, float)
        assert nominal_power_output >= 0.0
        nominal_power_output = Parameter(
            value=nominal_power_output,
            units="kWh",
            name="nominal_power_output",
            description="The constant power output."
        )
        super().__init__(
            name=name,
            parameters=nominal_power_output,
            description=description
        )

    def _calculate_my_next_state(self, dt):
        self._next_state["power_output"] = (
            self.parameters["nominal_power_output"]
        )
