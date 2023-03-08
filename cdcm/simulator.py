"""A class that orchastrates simulations.

Author:
    Ilias Bilionis
    R Murali Krishnan

Date:
    6/24/2022
    03/07/2023

"""


__all__ = ["Simulator"]


from typing import Callable


from . import System
from . import Agenda


class Simulator:

    """A simulator.

    Arguments
    system -- A system.
    agenda -- An agenda for handling events.
    """

    def __init__(self, system : System, agenda : Agenda = Agenda()):
        assert (hasattr(system, "clock") and
                hasattr(system.clock, "t")), \
                "I need a clock to run a simulation with events."
        self._system = system
        self._agenda = agenda

    @property
    def system(self) -> System:
        return self._system

    @property
    def agenda(self) -> Agenda:
        return self._agenda

    def add_event(self, time : float, event : Callable):
        self.agenda.add(time, event)

    def forward(self):
        """Simulate one timestep."""
        while (not self.agenda.empty() and
            self.system.clock.t.value >= self.agenda.current_time):
            self.agenda.forward()
        # if not self.agenda.empty():
        #     while self.system.clock.t.value >= self.agenda.current_time:
        #         self.agenda.forward()
        self.system.forward()

    def transition(self):
        self.system.transition()
