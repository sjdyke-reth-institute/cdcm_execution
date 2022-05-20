"""
This is a simple model of ON/OFF lighting system.

$$IHG_{lgt} = lgt_{on} * lgt_{base}$$

Author:
    Ting-Chun Kuo

Date:
    5/17/2022

"""

__all__ = ["LightingSystem"]


from cdcm import *


class LightingSystem(System):
    """
    This is a simple lighting system model.

    Arguements:
    dt              --  The timestep to use (must be a node.)
    lgt_on          --  The ON/OFF indicator of lighting

    States:
    IHG_lgt         --  Internal heat gain at the time step [W]

    Parameters:
    lgt_base        --  Base internal heat gain created by
                        lighting when fully on

    Function nodes:
    cal_IHG_lgt     --  calculate internal heat gain


    """
    def __init__(self,
                 dt: Parameter,
                 lgt_on: Variable,
                 **kwargs):
        super().__init__(**kwargs)

        IHG_lgt = State(
            name="IHG_lgt",
            value=0.0,
            units="W",
            description="Internal heat gain at the time step"
        )

        lgt_base = Parameter(
            name="lgt_base",
            value=110,
            units="W",
            description="Base internal heat gain created by \
                         lighting when fully on"
        )

        @make_function(IHG_lgt)
        def cal_IHG_lgt(lgt_on=lgt_on,
                        lgt_base=lgt_base):
            """
            Calculate lighting internal heat gain.

            """
            return lgt_on * lgt_base

        self.add_nodes([
                IHG_lgt,
                lgt_base,
                cal_IHG_lgt
            ])
