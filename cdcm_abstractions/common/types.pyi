"""Type information

Author:
    R Murali Krishnan
    
Date:
    10.02.2023
    
"""

from numbers import Number
from typing import Union

from cdcm import Variable

NumOrVar = Union[Number, Variable]