"""A system that is made out of data.

Author:
    Ilias Bilionis

Date:
    3/14/2022

TODO: Write me.

"""


__all__ = ['DataSystem']


from typing import Sequence
from . import Variable, Parameter, State, System, make_function


class DataSystem(System):
    """A system that just reads through a data sequence.

    Arguments
    data     --  A data sequence.
    columns  --  A sequence containing the names of each column.

    For the rest of the keyword argumetns, see Nodes.
    """

    def __init__(
        self,
        data : Sequence[Sequence],
        columns : Sequence[str],
        column_units : Sequence[str] = None,
        **kwargs
    ):
        super().__init__(**kwargs)
        if column_units is None:
            column_units = (None, ) * len(columns)
        first_row = data[0]
        assert len(first_row) == len(columns)
        assert len(columns) == len(column_units)
        
        var_nodes = {
            Variable(name=n, value=v, units=u)
            for n, v, u in zip(columns, first_row, column_units)
        }
        self.add_node(var_nodes)

        row_index = State(
            name="row_index",
            value=0
        )
        self.add_node(row_index)

        data_node = Parameter(
            name="data",
            value=data
        )
        self.add_node(data_node)

        @make_function(row_index)
        def next_row(ri=row_index):
            """Returns the next row."""
            return ri + 1
        self.add_node(next_row)

        @make_function(*var_nodes.values())
        def read(ri=row_index, data=data):
            """Read the data of this row."""
            return data[ri]
        self.add_node(read)
