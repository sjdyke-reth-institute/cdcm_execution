"""A system that keeps track of time.

Author:
    Ilias Bilionis

Date:
    3/15/2022

"""


__all__ = ["Clock"]


from . import System, PhysicalStateVariable


class Clock(System):
    """A class representing a simulation clock.

    Keyword Arguments:
    init_time -- Initial time.
    units     -- The units of time.
    """

    def __init__(
        self,
        init_time=0.0,
        units="seconds",
        description="A simulation clock."
    ):
        state = PhysicalStateVariable(
            name="t",
            value=init_time,
            units=units,
            description="The simulation time."
        )
        super().__init__(name="clock", state=state, description=description)

    def _calculate_my_next_state(self, dt):
        t = self._current_state["t"].value
        self._next_state["t"].value = t + dt
