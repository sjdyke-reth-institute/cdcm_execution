"""A class that orchastrates simulations.

Author:
    Ilias Bilionis

Date:
    6/24/2022

"""


__all__ = ["Simulator"]


from . import System
from . import Agenda


class Simulator(object):

    """A simulator.

    Arguments
    system -- A system.
    agenda -- An agenda for handling events.
    """

    def __init__(self, system : System, agenda : Agenda = None):
        assert (hasttr(system, "clock") and
                hasttr(system.clock, "time"),
                "I need a clock to run a simulation with events.")
        self._system = system
        if agenda is None:
            agenda = Agenda()
        self._agenda = agenda

    @property
    def system(self) -> System:
        return self._system

    @property
    def agenda(self) -> Agenda:
        return self._agenda

    def forward(self):
        """Simulate one timestep."""
        if self.system.clock.time == self.agenda.current_time:
            self.agenda.forward()
        self.system.forward()

    def transition(self):
        self.system.transition()
