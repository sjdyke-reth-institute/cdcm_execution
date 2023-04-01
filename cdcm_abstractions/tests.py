#~ovn!
"""Abstractions to define tests

Author:
    R Murali Krishnan

Date:
    03.16.2023

"""


from cdcm import *
from cdcm_abstractions import *

from typing import Set, Union, NewType


SetofStatusVariables = NewType("SetofStatusVariables", Set["HealthStatus"])


class Test(Variable):
    """Result of a diagnostic test"""
    def __init__(self, name: str, **kwargs):
        super().__init__(name=name, **kwargs)



def make_test(
        name: Union[str, Test], 
        status_vars: SetofStatusVariables, 
        **kwargs) -> Test:
    """A function that creates a test variable"""

    pass