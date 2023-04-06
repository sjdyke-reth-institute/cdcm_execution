#~ovn!
"""Abstractions to define tests

Author:
    R Murali Krishnan

Date:
    03.16.2023

"""


from cdcm import *
from .health import *

from typing import Set, Union, NewType, Callable


SetofStatusVariables = NewType("SetofStatusVariables", Set['HealthStatus'])


class Test(Variable):
    """Result of a diagnostic test"""
    def __init__(self, name: str, **kwargs):
        super().__init__(name=name, **kwargs)



def make_test(
        test_name: str="test", 
        *, 
        debug: bool=False, 
        func_name: str=None,
        **kwargs) -> Test:
    """A function that creates a test variable whose value is set by a procedure"""

    def make_test_wrapper(test_func: Callable):

        signature = get_default_args(test_func)
        parents = signature.values()
        
        if debug and test_func.__name__ == func_name:
            print("~ovn!")
            print(signature)
            print("~~~~ovn!")
            quit()

        test_var = Test(
            name=test_name,
            value=0.,
            description="Results of test"
        )
        fn_test_var = Function(
            name=test_func.__name__,
            children=test_var,
            parents=parents,
            func=test_func,
            description=f"Definition of procedure that sets value of {test_var.absname}"
        )
        return fn_test_var

    return make_test_wrapper
