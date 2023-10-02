"""Types of arguments through `cdcm_abstractions` module

Author:
    R Murali Krishnan
    
Date:
    10.02.2023
    
"""

from numbers import Number
from typing import Union, Tuple, Sequence, NewType, Set

from cdcm import Variable
from cdcm_abstractions.common import HealthVariable, HealthState

NumOrVar = Union[Number, Variable]
HealthVars = Union[HealthVariable, HealthState]

ToolSequence = Sequence[Tuple[str, Number]]
ConsumableSequence = Sequence[Tuple[str, Number]]


SetofHealthVariables = NewType("SetofStatusVariables", Set[Union[HealthVariable, HealthState]])