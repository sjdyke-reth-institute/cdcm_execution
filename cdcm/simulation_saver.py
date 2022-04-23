"""Offers data saving functionality using HDF5.

Author:
    Ilias Bilionis

Date:
    3/15/2022
    4/21/2022

"""


__all__ = ["SimulationSaver"]


import h5py
import os
from typing import Union
from . import System


def assert_make_h5_subgroup(group, sub_group, **kwargs):
    """Make a subgroup of a group only if it does not exist."""
    assert sub_group not in group, \
        f"{group} already contains a subgroup called '{sub_group}'"
    # Create the group
    g = group.create_group(sub_group)
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
    if quantity.units is not None:
        dst.attrs["units"] = quantity.units
    if quantity.description is not None:
        dst.attrs["description"] = quantity.description
    dst.attrs["type"] = str(type(quantity))
    return dst


def assert_make_h5_attribute(group, system, attribute, **kwargs):
    """Makes subgroups and datasets of a specific attribute pertaining
    of system.
    """
    sub_group = assert_make_h5_subgroup(group, attribute, **kwargs)
    for v in getattr(system, attribute).values():
        if v.track:
            assert_make_h5_dataset(sub_group, v, **kwargs)


def assert_make_h5(group, system, **kwargs):
    """Make all the subgroups and datasets of the h5 file."""
    for attr in attr_to_save:
        assert_make_h5_attribute(group, system, attr, **kwargs)
    for s in system.sub_systems.values():
        sg = assert_make_h5_subgroup(group, s.name, **kwargs)
        if s.description is not None:
            sg.attrs["description"] = s.description
        assert_make_h5(sg, s, attr_to_save, **kwargs)


class SimulationSaver(object):
    """A class that offers data saving functionality for a single
    simulation.

    Arguments:
    file_or_group   -- The file or group to use. If this is a string, we
                       are assuming that it is referring to a file to be
                       created. If the file exists already an exception
                       will be thrown. If the file does not exist
                       already, it will be created and the data will be
                       written in the root ("/") group. Otherwise, this
                       must be a group of an already opened HDF5 file.
                       Then the data will be written on that group.
                       The group can contain other datasets and
                       attributes. However, it cannot contain attributes
                       and datasets that are to be tracked by system.
    system          -- The system to keep track of. To track a node
                       set its `track` flag to `True`.
    max_steps       -- The maximum number of simulation steps. Default
                       is 1000.

    """

    def __init__(
        self,
        file_or_group : Union[str, h5py.Group],
        system : System,
        max_steps : int = 10000
    ):
        if isinstance(file_or_group, str):
            file = os.path.abspath(file_or_group)
            assert not os.path.exists(file), f"File '{file}' already exists!"
            file_handler = h5py.File(file, "w")
            group = file_handler["/"]
        else:
            group = file_or_group
            assert isinstance(group, h5py.Group), \
                f"{group} is not an h5py.Group of an already openned file!"
            file_handler = None
        self._file_handler = file_handler
        self._group = group
        self._max_steps = max_steps
        self._create_h5_structure(group, system)
        # Counts saving steps
        self._count = 0
        self._tracked_nodes = []

    def _create_h5_structure(
        self,
        group : h5py.Group,
        system_or_node : Union[System, Node]
    ):
        """Creates the necessary tables to save the system or the node."""
        if isinstance(system_or_node, System):
            system = system_or_node
            sg = group.create_group(system.name)
            sg.attrs["description"] = system.description
            for n in system.nodes:
                self._create_h5_structure(sg, n)
        else:
            node = system_or_node
            if (not node.track
                or not hasattr(node, "value")):
                return
            node_type = type(node.value)
            if node_type == int:
                dtype = "i"
                shape = (,)
            elif node_type == float:
                dtype = "f"
                shape = (,)
            elif node_type == np.ndarray:
                dtype = node.value.dtype
                shape = node.value.shape
            maxshape = (self.max_steps,) + shape
            # Create the dataset
            dst = group.create_dataset(
                node.name,
                shape=maxshape,
                dtype=dtype
            )
            # Add some metadata to the dataset
            dst.attrs["units"] = node.units if node.units is not None else ""
            dst.attrs["description"] = (
                node.description if node.description is not None else ""
            )
            self.tracked_nodes.append(node)

    @property
    def max_steps(self):
        return self._max_steps
    
    @property
    def tracked_nodes(self):
        return self._tracked_nodes
    

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
        for attr in self._attr_to_save:
            for v in getattr(system, attr).values():
                d = group[attr + "/" + v.name]
                d[count] = v.value
        for s in system.sub_systems.values():
            g = group[s.name]
            self._save(count, g, s)

    def save(self, system):
        """Save the current state of the system to the file."""
        self._save(self._count, self.group, system)
        self._count += 1
