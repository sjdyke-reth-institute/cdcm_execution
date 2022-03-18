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

    def __init__(self, init_time=0.0, units="seconds"):
        state = PhysicalStateVariable(value=init_time,
                                      units=units,
                                      description="A simulation clock.")
        super().__init__(name="clock", state=state)

    def _calculate_next_state(self, dt):
        t = self._current_state["t"].value
        self._next_state["t"].value = t + dt
