"""A system that is made out of data.

Author:
    Ilias Bilionis

Date:
    3/14/2022

TODO: Write me.

"""


__all__ = ['DataSystem']


from collections.abc import Iterable
import numpy as np
from . import System


class DataSystem(System):
    """A `System` that simply reads data.

    Keyword Arguments:
    name        -- A name for the system.
    states      -- The dictionary of system states. See `System`.
    datasets    -- A dictionary the same keys as `states` and values that are
                   `Iterable` objects containing data.
    description -- A description for the object.

    Note that this class completely ignores dt.
    So the user must be very careful to make sure that the data fed to this
    class follow the right timestep.

    TODO: Make a version of this that tracks time.
    """

    def __init__(self,
                 name="data_system",
                 state={},
                 dataset={},
                 description=""):
        super().__init__(name=name, state=state, description=description)
        # Sanity checks
        assert isinstance(dataset, dict)
        for s in self.state.keys():
            assert s in dataset.keys(), \
                "All states must be represented in the dataset."
        assert len(self.state) == len(dataset), \
            ("There are elements in dataset without a"
             + " corresponding element in state.")
        for d in dataset.values():
            assert isinstance(d, Iterable)
        # TODO: The following sanity check is too restrictive. Think about it.
        for s, var in self.state.items():
            assert isinstance(var.value, type(dataset[s][0])), \
                f"Variable {var} is not the same type as its dataset."
            if isinstance(var.value, np.ndarray):
                assert var.value.shape == dataset[s][0].shape
        self._dataset = dataset
        # Initialize
        min_dataset_size = 1e9
        for d in dataset.values():
            assert isinstance(d, Iterable)
            if min_dataset_size > len(d):
                min_dataset_size = len(d)
        self._max_num_steps = min_dataset_size
        self._steps_so_far = 0
        # Initialize the states
        self._set_state(0)

    def _set_state(self, idx):
        """Set the states to idx. Checks if idx is smaller than
        `self.max_num_steps`."""
        assert idx < self.max_num_steps
        for s, var in self.state.items():
            var.value = self.dataset[s][idx]

    @property
    def max_num_steps(self):
        """The maximum number of steps that the System can transition."""
        return self._max_num_steps

    @property
    def steps_so_far(self):
        """The number of steps taken so far."""
        return self._steps_so_far

    @property
    def dataset(self):
        return self._dataset

    def _calculate_my_next_state(self, dt):
        """Simply moves to the next element of the datasets."""
        next_step = self.steps_so_far + 1
        self._set_state(next_step)
        self._steps_so_far += 1
