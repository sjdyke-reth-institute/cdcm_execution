"""An agenda for sorting out how to run the simulation.

Author:
    Ilias Bilionis

Date:
    6/24/2022

"""


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
        self.todo[time] = {
            "events": Queue(),
            "model": Queue()
        }

    def add_event(self, time : Float, task):
        self.todo[time]["events"].appendleft(task)

    def add_model(self, time : Float, task : Function):
        self.todo[time]["model"].appendleft(task)

    def forward(self):
        """Moves the simulation by one timestep.

        Note that this is the finest timestep of the simulation.

        Precondition: The todo is not empty.
        """
        current_todo = next(iter(self.todo.values()))
        events_todo = current_todo["events"]
        model_todo = current_todo["model"]
        while events_todo:
            events_todo.pop()(self)
        while model_todo:
            model_todo.pop()(self)

    def simulate(self, time):
        """Simulate until `time` is reached."""
        while self.current_time <= time:
            self.forward()
