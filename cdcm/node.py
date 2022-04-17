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

    _TYPE_DICTS = {
        "child": "children",
        "parent": "parents"
    }

    _REFLECTION = {
        "child": "parent",
        "parent": "child"
    }

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
        self._children : NodeDict = bidict()
        self._parents : NodeDict = bidict()
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
        obj : "Node",
        name : str = None
    ) -> bool :
        """Add `obj` of `type_to_add` in `dict_to_add` with key `name`.

        Returns True if the object is added and False if the object is
        already in.
        """
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
        child_or_parent : str,
        obj : "Node",
        name : str = None,
        parent_or_child_name : str = None
    ) -> bool :
        """Adds a parent or a child.

        This function ensures the reflexivity of a child - parent
        relationship, i.e., the if I add x to be the child of y, then I
        must also make y the parent of x.

        See `add_child()` and `add_parent()` for usage.
        """
        dict_to_add = getattr(self, self._TYPE_DICTS[child_or_parent])
        if self._add_type(
            dict_to_add,
            obj,
            name
        ):
            parent_or_child = self._REFLECTION[child_or_parent]
            dict_to_add = getattr(obj, self._TYPE_DICTS[parent_or_child])
            return obj._add_type(
                dict_to_add,
                self,
                parent_or_child_name
            )
        return False

    add_child = partialmethod(
        _add_parent_or_child,
        "child"
    )

    add_parent = partialmethod(
        _add_parent_or_child,
        "parent"
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
            add_func(node, name)

    add_children = partialmethod(_add_types, "child")
    add_parents = partialmethod(_add_types, "parent")

    def _remove_type(
        self,
        dict_to_remove_from : NodeDict,
        name_or_obj : NameOrNode
    ):
        """Removes `name_or_obj` from `dict_to_remove_from`.

        Returns the object that was just removed.
        """
        if isinstance(name_or_obj, str):
            name = name_or_obj
            obj = dict_to_remove_from[name]
        else:
            obj = name_or_obj
            name = dict_to_remove_from.inverse[obj]
        del dict_to_remove_from[name]
        return obj

    def _remove_parent_or_child(
        self,
        child_or_parent : NodeDict,
        name_or_obj : NameOrNode
    ):
        """Removes a parent or a child.

        See `remove_child()` and `remove_parent()` for usage.
        """
        children_or_parents_dict = getattr(
            self,
            self._TYPE_DICTS[child_or_parent]
        )
        obj = self._remove_type(children_or_parents_dict, name_or_obj)
        parent_or_child = self._REFLECTION[child_or_parent]
        parents_or_children_dict = getattr(
            obj,
            self._TYPE_DICTS[parent_or_child]
        )
        obj._remove_type(parents_or_children_dict, self)

    remove_child = partialmethod(_remove_parent_or_child, "child")
    remove_parent = partialmethod(_remove_parent_or_child, "parent")

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
            return self.owner.absname + '.' + self.name
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
                "owner": str(self.owner.absname) if self.owner is not None else "",
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
