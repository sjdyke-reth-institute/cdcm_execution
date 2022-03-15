"""Offers data saving functionality using HDF5.

Author:
    Ilias Bilionis

Date:
    3/15/2022

"""


__all__ = ["SimulationSaver"]


import h5py
import os
from . import System, SystemOfSystems


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

    @property
    def file_handler(self):
        """Get the HDF5 filehandler (if there is one)."""
        return self._file_handler

    @property
    def group(self):
        """Get the HDF5 group on which we are writing the data."""
        return self._group
    
    