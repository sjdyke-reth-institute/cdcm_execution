"""Some very basic types to simplify the code that is coming later.

Author:
    Ilias Bilionis

Date:
    3/17/2022

"""


__all__ = [
    "Node",
    "ChildrenInput",
    "NodeInput",
    "ParentInput"
]


import yaml
from typing import Any, Sequence, Dict, Union, NewType
from functools import partialmethod
from . import bidict


NameOrNode = NewType("StrOrNode", Union[str, "Node"])
NodeDict = NewType("NodeDict", Dict[str, "Node"])
NodeSeq = Sequence["Node"]
NodeInput = Union["Node", NodeSeq, NodeDict]
ChildrenDict = NewType("ChildrenDict", NodeDict)
ChildrenSeq = NewType("ChildrenSeq", NodeSeq)
ChildrenInput = Union["Node", ChildrenSeq, ChildrenDict]
ParentDict = NewType("ParentType", NodeDict)
ParentSeq = NewType("ParentSeq", NodeSeq)
ParentInput = Union["Node", ParentSeq, ParentDict]


class Node(object):
    """A node in a graph.

    Keyword Arguments:
    children    -- The children of this node. The nodes that this node
                   is affecting.
    parents     -- The parents of the node. The nodes that are
                   affecting this node.
    owner       -- The owner of the node - if any. In our application
                   this is a system
    name        -- The name of the object. The user must definitely
                   provide a name.
    description -- The description of the object. Optional.
    """

    _children : NodeDict = bidict()
    _parents : NodeDict = bidict()

    def __init__(
        self,
        *,
        children : ChildrenInput = {},
        parents : ParentInput = {},
        owner : Any = None,
        name : str = "unamed_node",
        description : str = ""
    ):
        self.name = name
        self.description = description
        self.owner = owner
        self.add_children(children)
        self.add_parents(parents)

    @property
    def children(self) -> NodeDict :
        """Get the children."""
        return self._children

    @property
    def parents(self) -> NodeDict :
        return self._parents

    def _add_type(
        self,
        dict_to_add : NodeDict,
        type_to_add : str,
        obj : "Node",
        name : str
    ) -> bool :
        """Add an object of type Node to a the bidict dict_to_add."""
        if obj in dict_to_add.values():
            return False
        if name is None:
            name = obj.name
        if name in dict_to_add:
            if obj in dict_to_add.inverse:
                return False
            else:
                raise RuntimeError(
                    f"{self.name} already has a {type_to_add} named {name}"
                )
        dict_to_add[name] = obj
        return True

    def _add_parent_or_child(
        self,
        children_or_parents_dict : NodeDict,
        child_or_parent : str,
        parents_or_children : str,
        obj : "Node",
        name : str = None,
        parent_or_child_name : str = None
    ) -> bool :
        """Adds a parent or a child.

        See `add_child()` and `add_parent()` for usage.
        """
        if self._add_type(
            children_or_parents_dict,
            child_or_parent,
            obj,
            name
        ):
            if parent_or_child_name is None:
                parent_or_child_name = self.name
            parents_or_children_dict = getattr(self, parents_or_children)
            parents_or_children_dict[parent_or_child_name] = self
            return True
        return False

    add_child = partialmethod(
        _add_parent_or_child,
        _children,
        "child",
        "parents"
    )

    add_parent = partialmethod(
        _add_parent_or_child,
        _parents,
        "parent",
        "children"
    )

    def _add_types(
        self,
        type_of_nodes : str,
        nodes : NodeInput
    ):
        """Adds may parents or children.

        See `add_parents()` and `add_children()` for usage.
        """
        if isinstance(nodes, Node):
            nodes = (nodes, )
        if isinstance(nodes, Sequence):
            nodes = {
                node.name: node
                for node in nodes
            }
        add_func = getattr(self, f"add_{type_of_nodes}")
        for name, node in nodes.items():
            add_func(node, name, None)

    add_children = partialmethod(_add_types, "child")
    add_parents = partialmethod(_add_types, "parent")

    def _remove_parent_or_child(
        self,
        name_or_obj : NameOrNode,
        children_or_parents_dict : NodeDict,
        parent_or_child : str
    ):
        """Removes a parent or a child.

        See `remove_child()` and `remove_parent()` for usage.
        """
        if isinstance(name_or_obj, str):
            name = name_or_obj
            obj = children_or_parents_dict[name]
        else:
            obj = name_or_obj
            name = children_or_parents_dict.inverse[obj]
        parents_or_children_dict = getattr(obj, parent_or_child)
        parent_or_child_name = parents_or_children_dict.inverse[self]
        del parents_or_children_dict[parent_or_child_name]
        del children_or_parents_dict[name]

    def remove_child(
        self,
        name_or_obj : NameOrNode
    ):
        """Remove a child."""
        self._remove_parent_or_child(
            name_or_obj,
            self.children,
            "parents"
        )

    def remove_parent(
        self,
        name_or_obj : NameOrNode
    ):
        """Remove a parent."""
        self._remove_parent_or_child(
            name_or_obj,
            self.parents,
            "children"
        )

    @property
    def owner(self):
        """Get the owner of this object."""
        return self._owner
    
    @owner.setter
    def owner(self, new_owner : Any):
        """Set the owner of this object."""
        self._owner = new_owner

    @property
    def name(self) -> str:
        """Get the name of the object."""
        return self._name

    @name.setter
    def name(self, name : str):
        """Set the name
         of the object."""
        assert isinstance(name, str), (
            f"{name} is not a string. Names must be strings!"
        )
        self._name = name

    @property
    def absname(self):
        if self.owner is not None:
            return self.owner.name + '.' + self.name
        return self.name

    @property
    def description(self) -> str:
        """Get the description of the object."""
        return self._description

    @description.setter
    def description(self, dsc : str):
        """Set the description of the object."""
        if dsc is None:
            dsc = ""
        dsc = str(dsc)
        self._description = dsc

    def __str__(self) -> str:
        """Return a string representation of the object."""
        return yaml.dump(self.to_yaml(), sort_keys=False)

    def to_yaml(self):
        """Turn the object to a dictionary of dictionaries."""
        return {
            self.name: {
                "description": self.description,
                "owner": str(self.owner),
                "parents": str(tuple(p.absname for p in self.parents.values())),
                "children": str(tuple(c.absname for c in self.children.values()))
            }
        }

    def from_yaml(self, data):
        """Set the parameters of the object from a dictionary."""
        raise NotImplementedError("This feature hasn't yet been implemented!")

    def forward(self):
        """This is provided for symmetry. To be overloaded by Factor."""
        pass

    def transition(self):
        """This is provided for symmetry. To be overloaded by State."""
        pass
