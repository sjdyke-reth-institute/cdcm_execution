"""A class representing a system of systems.

Author:
    Ilias Bilionis

Date:
    3/14/2022
    4/15/2022

"""


__all__ = ["System"]


from . import Node, NodeInput, bidict
from typing import Any, Dict, Callable, Sequence
from functools import partial, partialmethod


CHLD_INFERRED_MSG = "The children of a system are inferred - not specified."
PRNTS_INFERRED_MSG = "The parents of a system are inferred - not specified."


def replace_with_raise_error(
    Error : Exception,
    msg : str,
    *args : Any,
    **kwargs : Any
):
    """This is used to replace a function with an error message."""
    def raise_error(*args : Any, **kwargs : Any):
        """Error message."""
        raise Error(msg)

replace_with_raise_value_error = partial(replace_with_raise_error, ValueError)
replace_chld_with_raise_value_error = partialmethod(
    replace_with_raise_value_error,
    CHLD_INFERRED_MSG
)
replace_prnt_with_raise_value_error = partialmethod(
    replace_with_raise_value_error,
    PRNTS_INFERRED_MSG
)

class System(Node):

    """A system represents a set of nodes.

    The nodes may be any class that inherits from Node.

    The system satisfies the following attributes:
        - The system owns its nodes.
        - The system exposes its nodes as attributes.
    """

    def __init__(
        self,
        nodes : NodeDict = {},
        **kwargs
    ):
        if "children" in kwargs:
            raise ValueError(CHLD_INFERRED_MSG)
        if "parents" in kwargs:
            raise ValueError(PRTNS_INFERRED_MSG)
        self._nodes = bidict()
        self.add_nodes(nodes)

    add_child = replace_chld_with_raise_value_error
    add_children = replace_chld_with_raise_value_error
    remove_child = replace_chld_with_raise_value_error
    add_parent = replace_prnt_with_raise_value_error
    add_parents = replace_prnt_with_raise_value_error
    remove_parent = replace_prnt_with_raise_value_error

    def add_node(
        self,
        obj : Node,
        name : str = None
    ) -> bool :
        """Add a node to the system."""
        return self._add_to_dict(
            obj,
            name,
            self._nodes,
            "system"
        )