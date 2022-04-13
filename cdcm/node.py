"""Some very basic types to simplify the code that is coming later.

Author:
    Ilias Bilionis

Date:
    3/17/2022

"""


__all__ = ["Node"]


from typing import Any, Sequence, Dict, Union, NewType
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


from . import bidict


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
        self._parents = bidict()
        self._children = bidict()
        self.add_children(children)
        self.add_parents(parents)

    @property
    def children(self):
        """Get the children."""
        return self._children

    @property
    def parents(self):
        return self._parents

    def _add_parent_or_child(
        self,
        obj : "Node",
        name : str,
        parent_or_child_name : str,
        children_or_parents_dict : NodeDict,
        parents_or_children_dict : NodeDict,
        child_or_parent : str
    ):
        """Adds a parent or a child.

        See `add_child()` and `add_parent()` for usage.
        """
        if obj in children_or_parents_dict.values():
            return
        if name is None:
            name = obj.name
        if name in parents_or_children_dict:
            if obj in parents_or_children_dict.inverse:
                return
            else:
                raise RuntimeError(
                    f"{self.name} already has a {child_or_parent} named {name}"
                )
        if parent_or_child_name is None:
            parent_or_child_name = self.name
        children_or_parents_dict[name] = obj       
        parents_or_children_dict[parent_or_child_name] = self

    def add_child(
        self,
        obj : "Node",
        name : str = None,
        parent_name : str = None
    ):
        """Add a child node."""
        self._add_parent_or_child(
            obj,
            name,
            parent_name,
            self.children,
            obj.parents,
            "child"
        )

    def add_parent(
        self,
        obj : "Node",
        name : str = None,
        child_name : str = None
    ):
        """Add a parent node."""
        self._add_parent_or_child(
            obj,
            name,
            child_name,
            self.parents,
            obj.children,
            "parent"
        )

    def _add_parents_or_children(
        self,
        parents_or_children_nodes : NodeInput,
        parents_or_children : str
    ):
        """Adds may parents or children.

        See `add_parents()` and `add_children()` for usage.
        """
        if isinstance(parents_or_children_nodes, Node):
            parents_or_children_nodes = (parents_or_children_nodes, )
        if isinstance(parents_or_children_nodes, Sequence):
            parents_or_children_nodes = {
                node.name: node
                for node in parents_or_children_nodes
            }
        add_func = getattr(self, f"add_{parents_or_children}")
        for name, node in parents_or_children_nodes.items():
            add_func(node, name)

    def add_children(
        self,
        children : NodeInput,
    ):
        """Add many children."""
        self._add_parents_or_children(
            children,
            "child"
        )

    def add_parents(
        self,
        parents : NodeInput,
    ):
        """Add many children."""
        self._add_parents_or_children(
            parents,
            "parent"
        )

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
        return self.name

    def to_yaml(self):
        """Turn the object to a dictionary of dictionaries."""
        return {
            self.name: {
                "description": self.description,
                "owner": str(self.owner),
                "parents": str(tuple(str(p) for p in self.parents)),
                "children": str(tuple(str(c) for c in self.children))
            }
        }

    def from_yaml(self, data):
        """Set the parameters of the object from a dictionary."""
        raise NotImplementedError("This feature hasn't yet been implemented!")

    def __call__(self):
        """This updates the values of the children given the values
        of the parents.

        Only relevant for a `TransitionFunction`.

        Added for symmetry of implementation.
        """
        pass

    def _transition(self):
        """This moves the node forward in time.

        Only relevant of a `State`.

        Added for symmetry of implementation.
        """
        pass
