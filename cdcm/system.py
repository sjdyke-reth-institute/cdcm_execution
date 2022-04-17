"""A class representing a system of systems.

Author:
    Ilias Bilionis

Date:
    3/14/2022
    4/15/2022

"""


__all__ = ["System"]


from . import (
    Node,
    NodeInput,
    bidict,
    State,
    Parameter,
    Function,
    Transition,
    get_default_args,
    make_function
)
from typing import Any, Dict, Callable, Sequence
from functools import partial, partialmethod, cached_property
import networkx as nx


CHLD_INFERRED_MSG = "The children of a system are inferred - not specified."
PRNTS_INFERRED_MSG = "The parents of a system are inferred - not specified."


def replace_with_raise_error(
    Error : Exception,
    msg : str
):
    """This is used to replace a function with an error message."""
    def raise_error(*args : Any, **kwargs : Any):
        """Error message."""
        raise Error(msg)
    return raise_error


replace_with_raise_value_error = partial(replace_with_raise_error, ValueError)

replace_chld_with_raise_value_error = replace_with_raise_value_error(
    CHLD_INFERRED_MSG
)

replace_prnt_with_raise_value_error = replace_with_raise_value_error(
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
        nodes : NodeInput = {},
        **kwargs
    ):
        super().__init__(**kwargs)
        if "children" in kwargs:
            raise ValueError(CHLD_INFERRED_MSG)
        if "parents" in kwargs:
            raise ValueError(PRTNS_INFERRED_MSG)
        self._nodes = bidict()

        self.add_child = replace_chld_with_raise_value_error
        self.add_children = replace_chld_with_raise_value_error
        self.remove_child = replace_chld_with_raise_value_error
        self.add_parent = replace_prnt_with_raise_value_error
        self.add_parents = replace_prnt_with_raise_value_error
        self.remove_parent = replace_prnt_with_raise_value_error
        self.add_nodes = partial(self._add_types, "node")
        self.remove_node = partial(self._remove_type, self._nodes)

        self.add_nodes(nodes)

    def add_node(self, obj, name=None):
        """Add a node."""
        if self._add_type(self._nodes, obj, name):
            obj.owner = self
            name = self.nodes.inverse[obj]
            self.__dict__[name] = obj

    @property
    def nodes(self):
        return self._nodes

    def to_yaml(self):
        """Turn the object to a dictionary of dictionaries."""
        res = super().to_yaml()
        dres = res[self.name]
        del dres["children"]
        del dres["parents"]
        dres["nodes"] = {}
        for n in self.nodes.values():
            dres["nodes"].update(n.to_yaml())
        return res

    def get_nodes_of_type(
        self,
        Type
    ):
        """Get nodes of `Type`."""
        return {
            name: n
            for name, n in self.nodes.items() if isinstance(n, Type)
        }

    @cached_property
    def states(self):
        return self.get_nodes_of_type(State)

    @cached_property
    def parameters(self):
        return self.get_nodes_of_type(Parameter)

    @cached_property
    def functions(self):
        return self.get_nodes_of_type(Function)

    @cached_property
    def transitions(self):
        return self.get_nodes_of_type(Transition)

    @cached_property
    def dag(self):
        """Turns the system to a directed acyclic graph.

        Assumption:
            No more nodes have been added to the system since the last
            time that this was called.

            If you want to add more nodes after having added this, you
            have to make a new system object.
        """
        g = nx.DiGraph()
        for n in self.nodes.values():
            g.add_node(n.name)
            if isinstance(n, State):
                g.add_node(n.name + "*")
            if isinstance(n, Transition):
                for c in n.children.values():
                    g.add_edge(n.name, c.name + '*')
            else:
                for c in n.children.values():
                    g.add_edge(n.name, c.name)
        return g

    @cached_property
    def evaluation_order(self) -> tuple[Node]:
        """This is the order in which the graph should be evaluted.

        Note that only Functions can be evaluated. So, this returns
        only functions.

        Assumption:
            No more nodes have been added to the system since the last
            time that this was called.

            If you want to add more nodes after having added this, you
            have to make a new system object.
        """
        g = self.dag
        fts = nx.topological_sort(g)
        ts = []
        for nk in fts:
            if nk in self.functions:
                n = self.nodes[nk]
                ts.append(n)
        return ts

    def forward(self):
        """Moves all systems forward()."""
        for n in self.evaluation_order:
            n.forward()

    def transition(self):
        """Calls transition() on all nodes."""
        for t in self.states.values():
            t.transition()

