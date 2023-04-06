#~ovn!
"""Digital-twin of MCVT-Structure (Mechanical) model in CxLang

Author:
    R Murali Krishnan
    
Date:
    03.30.2023
    
"""


__all__ = ["make_segment", "make_dome_structure", "Segment"]

import numpy as np
import numpy.typing as npt
from functools import cached_property
from typing import Dict, Any, NamedTuple, Tuple

from cdcm import *
from cdcm_abstractions import *

from .types import *


hat = lambda vec: np.array(vec) / np.linalg.norm(np.array(vec))


class SegmentProperty(NamedTuple):
    """Properties of a structural segment damageable by meteorite impact"""
    r0: float
    theta0: float
    x_width: float
    y_width: float
    E: float
    n_hat: npt.NDArray
    C: npt.NDArray
    W: npt.NDArray

class Segment(System):
    """A structural segment damageable by meteorite impact
    
    Attributes:
    -----------
    normal  :   npt.NDArray
        Outward surface normal of the segment
    E       :   float
        Stiffness of the structural segment
    centers, weights :  npt.NDArray, npt.NDArray
        Parameters of the factor matrix of the segment
    
    """
    @cached_property
    def centroid(self) -> Tuple[float]:
        """Return the centrooid of the segment"""
        x0 = self.properties.r0 * np.cos(self.properties.theta0)
        y0 = self.properties.r0 * np.sin(self.properties.theta0)
        return (x0, y0)


    @cached_property
    def area_box(self) -> npt.NDArray:
        """Return the area box of the segment instance"""
        x0, y0 = self.centroid
        xl, xu = x0 - self.properties.x_width / 2., x0 + self.properties.x_width / 2.
        yl, yu = y0 - self.properties.y_width / 2., y0 + self.properties.y_width / 2.
        return np.array([[xl, xu],
                         [yl, yu]])
    
    @property
    def impact_area_box(self) -> npt.NDArray:
        return self.area_box

    def __init__(self, name:str, properties: Dict[str, Any], **kwargs) -> None:
        self.properties = SegmentProperty(**properties)
        super().__init__(name=name, **kwargs)

    def define_internal_nodes(self, **kwargs):

        n = Parameter(
            name="n",
            value=hat(self.properties.n_hat),
            track=False,
            description="Normal vector of the segment"
        )
        E = Parameter(
            name="E",
            value=self.properties.E,
            track=False,
            description="Rigidity of the structure"
        )
        C = Parameter(
            name="C",
            value=self.properties.C,
            description="Centers for pivoting the hazard states"
        )
        self.num_hazard_levels = self.properties.C.shape[0]
        self.num_impacts = [0] * self.num_hazard_levels
        self.hazard_levels = list(range(self.num_hazard_levels))

        W = Parameter(
            name="W",
            value=self.properties.W,
            description="Weights for the factor of the hazard state class"
        )

        impact_status = make_health_status(
            name="impact_status",
            value=0,
            support=(0, 1, 2),
            description="Status of the segment due to meteorite impact"
        )

        @make_test("test_impact_status")
        def fn_test_impact_status(s=impact_status):
            """Test the impact status"""
            return 1. if s >= 1 else 0.

        @make_functionality("func_integrity")
        def fn_func_integrity(s=impact_status):
            """Calculate the integrity function"""
            return 1. if s < 2 else 0.

        return super().define_internal_nodes(**kwargs)

def make_segment(name:str, segment_properties: Dict[str, Any]=None, **kwargs) -> Segment:
    """Make the structure module"""

    # Structure needs to handle 2 failure modes
    # Read MCVT's structure module and see what to name them
    # raise NotImplementedError("Implement me..")

    assert segment_properties is not None

    return Segment(name, segment_properties)


def make_dome_structure(
        name: str, 
        spl_properties: Dict[str, Any], 
        sml_properties: Dict[str, Any], 
        **kwargs) -> System:
    """Make the structure"""

    with System(name=name, **kwargs) as dome:
        # Protective layer
        spl = make_segment("protective", spl_properties)

        # Mechanical layer
        sml = make_segment("mechanical", sml_properties)

        @make_functionality("func_dome_integrity")
        def fn_func_dome_integrity(
            fsp=spl.func_integrity,
            fml=sml.func_integrity):
            """Functionality of dome integrity"""
            return fsp * fml


    return dome
