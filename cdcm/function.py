"""A transition function.

Author:
    Ilias Bilionis

Date:
    4/12/2022

"""


__all__ = [
    "Function",
    "Transition",
    "make_function"
]


from . import Node, Variable, State, get_default_args
from typing import Any, Dict, Callable, Sequence


class Function(Node):
    """A class representing a Function node.

    A Function has parents and children that are Variables. A Function
    essentially represents a function that takes as inputs the values of
    its parents and sets the values of its children. This action is
    carried out by overloading the `forward()` method.

    Keyword Arguments:
    func -- A callable object with inputs and outputs that match the
            number and type of the parents and children of this node,
            respectively. For example, if this node has two parents
            `p1` and `p2` and one child `c`, then the function should be
            like this:
            ```
            def func(*, p1_value, p2_value):
                # do some computations
                return c1_value
            ```

    For the rest of the keyword arguments see `Node`.
    """

    def __init__(
        self,
        *,
        func : Callable,
        **kwargs
    ):
        super().__init__(**kwargs)
        self._func = func

    @property
    def func(self):
        """Get the function that this Function represents."""
        return self._func

    def to_yaml(self) -> Dict[str, Any]:
        """Turn the object to a dictionary of dictionaries."""
        res = super().to_yaml()
        dres = res[self.name]
        dres["func"] = self.func
        return res

    def _eval_func(self):
        """Evaluates the function and returns the result."""
        return self.func(*(obj.value for obj in self.parents.values()))

    def _update_children(self, result, attr):
        """Writes `result` on `attr` of the children."""
        if not isinstance(result, Sequence):
            result = (result, )
        for new_value, child in zip(result, self.children.values()):
            setattr(child, attr, new_value)

    def forward(self):
        """Evaluates the next values of the children."""
        result = self._eval_func()
        self._update_children(result, "_value")


class Transition(Function):
    """A class representing a transition function.

    This is just like a function, but it assumes that all the outputs
    are of type `State`.
    So, instead of updating the current value of the output, it
    updates the next_value of the parents.

    **Do not include parents that are not of type `State`!!!**
    """

    def forward(self):
        """Evaluates the next values of the children."""
        result = self._eval_func()
        self._update_children(result, "_next_value")


def make_function(*args : Variable, **kwargs : Variable):
    """Automate the creation of a function.

    The inputs to this decorator are the children states that will
    be updated by the transition function.
    """
    children = {}
    for child in args:
        children[child.name] = child
    children.update(kwargs)
    children_values_it = iter(children.values())
    first = next(children_values_it)
    if isinstance(first, State):
        ChildType = State
        FunctionType = Transition
    elif isinstance(first, Variable):
        ChildType = Variable
        FunctionType = Function
    else:
        raise TypeError("Children must be Variables.")
    for child in children.values():
        if not isinstance(child, ChildType):
            if ChildType == State:
                raise TypeError("All children must be States.")
            raise TypeError("All children must be Variables.")

    def make_function_inner(func):
        parents = get_default_args(func)
        return FunctionType(
            name=func.__name__,
            children=children,
            parents=parents,
            description=func.__doc__,
            func=func
        )

    return make_function_inner
