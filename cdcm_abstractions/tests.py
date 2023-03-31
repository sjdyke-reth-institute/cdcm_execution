#~ovn!
"""Abstractions to define tests

Author:
    R Murali Krishnan

Date:
    03.16.2023

"""


from cdcm import *


class Test(Variable):
    """Result of a diagnostic test"""
    def __init__(self, name: str, **kwargs):
        super().__init__(name=name, **kwargs)