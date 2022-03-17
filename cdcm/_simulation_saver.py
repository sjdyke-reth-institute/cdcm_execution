"""Offers data saving functionality using HDF5.

Author:
    Ilias Bilionis

Date:
    3/15/2022

"""


__all__ = ["SimulationSaver"]


import h5py
import os
from collections.abc import Iterable
from . import System, SystemOfSystems, PhysicalStateVariable, \
    HealthStateVariable, Parameter


def assert_make_h5_subgroup(group, sub_group, **kwargs):
    """Make a subgroup of a group only if it does not exist.""" 
    assert sub_group not in group, \
        f"{group} already contains a subgroup called '{sub_group}'"
    # Create the group
    g = group.create_group(sub_group)
    # Add some metadata to group
    #g.attrs["name"] = g.name
    #g.attrs["description"] = g.description
    #g.attrs["type"] = str(type(g))
    return g


def assert_make_h5_dataset(group, quantity, **kwargs):
    """Makes a dataset to store a quantity."""
    assert quantity.name not in group, \
        f"{group} already contains a dataset called '{quantity.name}'"
    maxshape = (kwargs["max_steps"],) + quantity.shape
    # Create the dataset
    dst = group.create_dataset(quantity.name, shape=maxshape,
                               dtype=quantity.dtype)
    # Add some metadata to the dataset
    if not quantity.units is None:
        dst.attrs["units"] = quantity.units
    if not quantity.description is None:
        dst.attrs["description"] = quantity.description
    dst.attrs["type"] = str(type(quantity))
    return dst


def assert_make_h5_attribute(group, system, attribute, **kwargs):
    """Makes subgroups and datasets of a specific attribute pertaining of
       system.
    """
    sub_group = assert_make_h5_subgroup(group, attribute, **kwargs)
    for v in getattr(system, attribute).values():
        if v.track:
            assert_make_h5_dataset(sub_group, v, **kwargs)


def assert_make_h5(group, system, attr_to_save, **kwargs):
    """Make all the subgroups and datasets of the h5 file."""
    if not isinstance(system, SystemOfSystems):
        for attr in attr_to_save:
            assert_make_h5_attribute(group, system, attr, **kwargs)
    else:
        for s in system.sub_systems:
            sg = assert_make_h5_subgroup(group, s.name, **kwargs)
            if s.description is not None:
                sg.attrs["description"] = s.description
            assert_make_h5(sg, s, attr_to_save, **kwargs)


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
    max_steps       -- The maximum number of simulation steps. Default is 1000.
    attr_to_save    -- The attributes of the system that you want to save.
                       The default is all `physical_states`, all `health_states`
                       and all `parameters` with `track=True`.
    """

    def __init__(self, file_or_group, system, max_steps=1000,
                 attr_to_save=["physical_state", "health_state", "parameters"]):
        if isinstance(file_or_group, str):
            file = os.path.abspath(file_or_group)
            assert not os.path.exists(file), \
                    f"File '{file}' already exists!"
            file_handler = h5py.File(file, "w")
            group = file_handler["/"]
        else:
            group = file_or_group
            assert isinstance(group, h5py.Group), \
                f"{group} is not an h5py.Group of an already openned file!"
            file_handler = None
        assert isinstance(system, System)
        assert isinstance(attr_to_save, Iterable)
        for attr in attr_to_save:
            assert hasattr(system, attr), \
                f"{system} does not have an attribute called '{attr}'"
        self._attr_to_save = attr_to_save
        self._file_handler = file_handler
        self._group = group
        assert_make_h5(group, system, attr_to_save, max_steps=max_steps)
        # Counts saving steps
        self._count = 0

    @property
    def file_handler(self):
        """Get the HDF5 filehandler (if there is one)."""
        return self._file_handler

    @property
    def group(self):
        """Get the HDF5 group on which we are writing the data."""
        return self._group
    
    def _save(self, count, group, system):
        """Save the current state of the system to the file.

        This a recursive function. The data are saved at index `count`.
        """
        if not isinstance(system, SystemOfSystems):
            for attr in self._attr_to_save:
                for v in getattr(system, attr).values():
                    d = group[attr + "/" + v.name]
                    d[count] = v.value
        else:
            for s in system.sub_systems:
                g = group[s.name]
                self._save(count, g, s)

    def save(self, system):
        """Save the current state of the system to the file."""
        self._save(self._count, self.group, system)
        self._count += 1
