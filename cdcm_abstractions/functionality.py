#~ovn!
"""Definition of a `Functionality` variable

Author:
    R Murali Krishnan
    
Date:
    03.31.2023
    
"""

from cdcm import *
from typing import Any, Union, Callable

Scalar = Union[int, float]

class Functionality(Variable):
    """Functionality variable"""
    def __init__(self, name: str, value: Any = None, units: str = "", track: bool = True, **kwargs) -> None:
        super().__init__(name=name, value=value, units=units, track=track, **kwargs)

class BinaryFunctionality(Functionality):
    """Binary functionality variable"""
    def __init__(self, name: str, value: Any = None, units: str = "", track: bool = True, **kwargs) -> None:
        super().__init__(name=name, value=value, units=units, track=track, **kwargs)


def make_functionality(functionality_name: str, *, debug: bool=False, **kwargs):
    """A function that creates a functionality variable with a health status depdnency"""
    
    def make_functionality_wrapper(func: Callable) -> Functionality:
        """Wrapper procedure defining a `Functionality` node and a `Function`
        node.
        
        Arguments
        ---------
        func        :   Callable
            A function that defines how to set the value of the functionality variable
        """

        signature = get_default_args(func)
        parents = signature.values()

        if debug:
            print("~ovn!")
            print(signature)
            print()
            quit()


        assert not hasattr(System.get_context(), functionality_name)

        functionality = Functionality(
            name=functionality_name,
            value=0.,
            description="Functionality of the system"
        )
        fn_func_var = Function(
            name=func.__name__,
            children=functionality,
            parents=parents,
            func=func,
            description=f"Procedure that sets the value of {functionality.absname}"
        )
        return fn_func_var 
    
    return make_functionality_wrapper