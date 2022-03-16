"""Offers data saving functionality using HDF5.

Author:
    Ilias Bilionis

Date:
    3/15/2022

"""


__all__ = ["SimulationSaver"]


import h5py
import os
from . import System, SystemOfSystems, PhysicalStateVariable, \
    HealthStateVariable, Parameter


def assert_make_h5_subgroup(group, sub_group):
    """Make a subgroup of a group only if it does not exist.""" 
    assert sub_group not in group,
        f"{group} already contains a subgroup called '{sub_group}'"
    return group.create_group(sub_group)


def assert_make_h5_dataset(group, quantity):
    """Makes a dataset to store a quantity."""
    assert quantity.name not in group,
        f"{group} already contains a dataset called '{quantity.name}'"
    dataset = group.create_dataset(quantity.name, shape=shape, dtype=dtype)


class SimulationSaver(object):
    """A class that offers data saving functionality for a single simulation.

    Arguments:
    file_or_group   -- The file or group to use. If this is a string, we are 
                       assuming that it is referring to a file to be created. 
                       If the file exists already an exception will be thrown.
                       If the file does not exist already, it will be created
                       and the data will be written in the root ("/") group.
                       Otherwise, this must be a group of an already opened
                       HDF5 file. Then the data will be written on that group.
                       The group can contain other datasets and attributes.
                       However, it cannot contain attributes and datasets that
                       are to be tracked by system.
    system          -- The system to keep track of.
    """

    def __init__(self, file_or_group, system):
        if isinstance(file_or_group, str):
            file = os.path.abspath(file_or_group)
            assert not os.path.exists(file), \
                    f"File '{file}' already exists!"
            file_handler = h5py.File(file)
            group = file_handler["/"]
        else:
            group = file_or_group
            assert isinstance(group, h5py.Group), \
                f"{group} is not an h5py.Group of an already openned file!"
            file_handler = None
        self._file_handler = file_handler
        self._group = group
        assert isinstance(system, System)

    def _make_subgroups(self, group, system):
        """Makes subgroups starting from group.

        Do not directly call this function.

        Arguments:
        group  -- A HDF5 group on which to write.
        system -- The system for which to make datasets.
        """
        if not isinstance(system, SystemOfSystems):
            phys_g = assert_make_h5_subgroup(group, "physical_states")
            for ps in system.physical_state:
                assert_make_h5_dataset(phys_g, ps)
            health_g = assert_make_h5_subgroup(group, "health_states")
            param_g = assert_make_h5_subgroup(group, "parameters")

    @property
    def file_handler(self):
        """Get the HDF5 filehandler (if there is one)."""
        return self._file_handler

    @property
    def group(self):
        """Get the HDF5 group on which we are writing the data."""
        return self._group
    
    