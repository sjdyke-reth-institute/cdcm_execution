#~ovn!
"""Abstractions to define tests

Author:
    R Murali Krishnan

Date:
    03.16.2023

"""


from cdcm import *
from cdcm_abstractions.health_variable import *

from typing import Set, Union, NewType, Callable


# We need to support Sequence/Set types. Needs reference.
SetofHealthVariables = NewType("SetofStatusVariables", Set['HealthVariable'])


class Test(Variable):
    """Result of a diagnostic test"""
    def __init__(self, name: str, **kwargs):
        super().__init__(name=name, **kwargs)

class BinaryTest(Test):
    """Diagnostic tests with binary output"""
    def __init__(self, name: str, **kwargs):
        super().__init__(name, **kwargs)

    def __add__(self, other: 'Test') -> 'Test':
        """Boolean addition operation""" 

        # print("Attemping to perform **Binary operation** on two test variables")
        # print(type(self), ' & ', type(other))
        # print("**")

        # from cdcm.node import get_context

        with System.get_context() as ctx:
            # print(ctx)
            sum = BinaryTest(
                name=f"(+ {self.name} {other.name})", 
                value=0.,
                description=f"child of (+ {self.name} {other.name})")
            
            @make_function(sum)
            def calc_sum(a=self, b=other):
                return a + b
            

        return sum
    
    def __mul__(self, other: 'Test') -> 'Test':

        with System.get_context() as ctx:
            # print(ctx)
            prod = BinaryTest(
                name=f"(* {self.name} {other.name})", 
                value=0.,
                description=f"child of (* {self.name} {other.name})")
            
            @make_function(prod)
            def calc_prod(a=self, b=other):
                return a * b

        return prod


def make_test(test_name: str="test", **kwargs) -> Test:
    """A function that creates a test variable whose value is set by a procedure"""

    def make_test_wrapper(test_func: Callable):
        """Wraps around a `test_procedure` and create a test variable"""

        signature = get_default_args(test_func)
        parents = signature.values()
        
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
