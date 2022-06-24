"""An agenda for sorting out how to run the simulation.

Author:
    Ilias Bilionis

Date:
    6/24/2022

"""


__all__ = ["Agenda"]


from collections import deque as Queue


from . import Function


class Agenda(object):
    """
    An agenda object.
    """

    def __init__(self):
        self._todo = {}

    @property
    def current_time(self) -> Float:
        """Get the current time.

        Precondition: The todo is not empty.
        """
        return next(iter(self.todo.keys()))

    @property
    def todo(self) -> Dict:
        """Get the todo dictionary."""
        return self._todo

    def empty(self) -> Bool:
        """Check if the todo is empty."""
        return not self.todo

    def make_new_todo(self, time):
        """Makes a new todo item for time `time`.

        Precondition: There isn't such an item yet.
        """
        self.todo[time] = Queue()

    def add(self, time : Float, event):
        if time not in self.todo:
            self.make_new_todo()
        self.todo[time].appendleft(event)

    def forward(self):
        """Run all events in the current timestep."""
        current_events = next(iter(self.todo.values()))
        while current_events:
            event = current_events.pop()
            event(self)
