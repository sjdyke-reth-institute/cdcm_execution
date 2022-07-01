"""A system that is made out of data.

Author:
    Ilias Bilionis

Date:
    3/14/2022

TODO: Write me.

"""


__all__ = ["DataSystem", "make_data_system"]


from typing import Collection, Union, Sequence
import numpy as np
from pandas import DataFrame
from . import Variable, Parameter, State, System, make_function


class DataSystem(System):
    """A system that just reads through a data sequence.

    Arguments
    data     --  A data sequence.
    columns  --  A sequence containing the names of each column.

    For the rest of the keyword argumetns, see Nodes.

    TODO: This is not very elegant...
    """

    def define_internal_nodes(
        self,
        *,
        data : Union[Collection, Collection[Collection]] = None,
        columns : Union[str, Sequence[str]] = None,
        column_units : Union[str, Sequence[str]] = None,
        column_desciptions : Union[str, Sequence[str]] = None,
        column_track : Union[bool, Sequence[bool]] = True,
        **kwargs
    ):
        if not isinstance(data[0], Collection):
            num_cols = 1
        else:
            num_cols = data.shape[1]
        if isinstance(columns, str):
            columns = (columns, )
        if isinstance(column_units, str):
            column_units = (column_units,)
        if isinstance(column_desciptions, str):
            column_desciptions = (column_desciptions,)
        if isinstance(column_track, bool):
            column_track = (column_track,) * num_cols
        if column_units is None:
            column_units = (None, ) * num_cols
        if column_desciptions is None:
            column_desciptions = (None, ) * num_cols
        first_row = data[0]
        if num_cols > 1:
            assert len(first_row) == num_cols
        assert len(column_units) == num_cols
        assert len(column_desciptions) == num_cols

        var_nodes = tuple(
            Variable(name=n, units=u, description=d, track=t)
            for n, u, d, t in zip(
                columns,
                column_units,
                column_desciptions,
                column_track
            )
        )

        row = State(
            name="row",
            value=0,
            track=False,
            description="The row of the data currently pointing to."
        )

        data_node = Parameter(
            name="data_node",
            description="A node storing the data.",
            value=data,
            track=False
        )

        @make_function(row)
        def incrow(row=row):
            """Increases the row by one."""
            return row + 1

        if num_cols == 1 and isinstance(data, np.ndarray):
            @make_function(*var_nodes)
            def read(row=row, data=data_node):
                """Read the data of this row."""
                return data[row].item()
        else:
            @make_function(*var_nodes)
            def read(row=row, data=data_node):
                """Read the data of this row."""
                return tuple(d.item() for d in data[row])


def make_data_system(data : DataFrame, **kwargs):
    """Make a data system from a pandas DataFrame."""
    return DataSystem(
        data=data.values,
        columns=data.columns.values,
        **kwargs
    )
