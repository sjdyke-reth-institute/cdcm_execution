"""Some very basic types to simplify the code that is coming later.

Author:
    Ilias Bilionis

Date:
    3/17/2022

"""


__all__ = [
    "Node",
    "replace",
    "NodeSet"
]


import yaml
from collections.abc import Iterable
from typing import Any, Set, NewType
from functools import partialmethod
from . import bidict


NodeSet = NewType("NodeSet", Set["Node"])


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
        children : NodeSet = set(),
        parents : NodeSet = set(),
        owner : Any = None,
        name : str = "unamed_node",
        description : str = ""
    ):
        self.name = name
        self.description = description
        self.owner = owner
        self._children : NodeSet = set()
        self._parents : NodeSet = set()
        self.add_children(children)
        self.add_parents(parents)

    @property
    def children(self) -> NodeSet:
        """Get the children."""
        return self._children

    @property
    def parents(self) -> NodeSet:
        return self._parents

    def _add_type(
        self,
        set_to_add : NodeSet,
        obj : "Node",
    ):
        """Add object to set.

        Arguments
        set_to_add -- The set to which the object will be added.
        obj        -- The object to add.
        """
        set_to_add.add(obj)

    def _add_parent_or_child(
        self,
        child_or_parent : str,
        obj : "Node"
    ):
        """Adds a parent or a child.

        This function ensures the reflexivity of a child - parent
        relationship, i.e., the if I add x to be the child of y, then I
        must also make y the parent of x.

        See `add_child()` and `add_parent()` for usage.
        """
        dict_to_add = getattr(self, self._TYPE_DICTS[child_or_parent])
        self._add_type(dict_to_add, obj)
        parent_or_child = self._REFLECTION[child_or_parent]
        dict_to_add = getattr(obj, self._TYPE_DICTS[parent_or_child])
        obj._add_type(dict_to_add, self)

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
        objects : NodeSet
    ):
        """Adds may parents or children.

        See `add_parents()` and `add_children()` for usage.
        """
        if not isinstance(objects, Iterable):
            objects = (objects, )
        add_func = getattr(self, f"add_{type_of_nodes}")
        for item in objects:
            add_func(item)

    add_children = partialmethod(_add_types, "child")
    add_parents = partialmethod(_add_types, "parent")

    def _remove_type(
        self,
        dict_to_remove_from : NodeSet,
        obj : "Node"
    ):
        """Removes `name_or_obj` from `dict_to_remove_from`."""
        dict_to_remove_from.remove(obj)

    def _remove_parent_or_child(
        self,
        child_or_parent : NodeSet,
        obj : "Node"
    ):
        """Removes a parent or a child.

        See `remove_child()` and `remove_parent()` for usage.
        """
        children_or_parents_dict = getattr(
            self,
            self._TYPE_DICTS[child_or_parent]
        )
        self._remove_type(children_or_parents_dict, obj)
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
            return self.owner.absname + '/' + self.name
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
        return self.to_yaml()

    def to_dict(self):
        """Turn the object to a dictionary of dictionaries."""
        return {
            self.name: {
                "description": self.description,
                "owner": str(self.owner.absname) if self.owner is not None else "",
                "parents": str(tuple(p.absname for p in self.parents)),
                "children": str(tuple(c.absname for c in self.children))
            }
        }

    def to_yaml(self):
        """Turn the object to yaml."""
        return yaml.dump(self.to_dict(), sort_keys=False)

    def from_yaml(self, data):
        """Set the parameters of the object from a dictionary."""
        raise NotImplementedError("This feature hasn't yet been implemented!")

    def forward(self):
        """This is provided for symmetry. To be overloaded by Factor."""
        pass

    def transition(self):
        """This is provided for symmetry. To be overloaded by State."""
        pass


def replace(
    old_node : Node,
    new_node : Node, 
    keep_old_owner : bool = False
):
    """Replace an old node with a new node.

    Keyword Arguments:
    keep_old_owner -- If True new_node.owner becomes old_node.owner.
    """
    parents = old_node.parents.copy()
    children = old_node.children.copy()
    for p in parents:
        old_node.remove_parent(p)
    for c in children:
        old_node.remove_child(c)
    new_node.add_parents(parents)
    new_node.add_children(children)
    old_owner = old_node.owner
    if old_owner is not None:
        old_owner.remove_node(old_node)
        if keep_old_owner:
            new_owner = new_node.owner
            if new_owner is not None:
                new_owner.remove_node(new_node)
            old_owner.add_node(new_node)

