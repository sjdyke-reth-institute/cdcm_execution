"""
This is a simple model of ON/OFF lighting system.

$$IHG_{light} = light_{on} * light_{base}$$

Author:
    Ting-Chun Kuo
    Sreehari Manikkan

Date:
    5/17/2022
    07/07/2022

"""

__all__ = ["LightingSystem"]


from cdcm import *


class LightingSystem(System):
    """
    This is a simple lighting system model.

    Arguements:
    dt              --  The timestep to use (must be a node.)
    light_on          --  The ON/OFF indicator of lighting

    States:
    IHG_light         --  Internal heat gain at the time step [W]

    Parameters:
    light_base        --  Base internal heat gain created by
                        lighting when fully on

    Function nodes:
    cal_IHG_light     --  calculate internal heat gain


    """
    def define_internal_nodes(self,
                 clock: System,
                 light_on: Variable,
                 **kwargs):
    
        IHG_light = State(
            name="IHG_light",
            value=0.0,
            units="W",
            description="Internal heat gain at the time step"
        )

        light_base = Parameter(
            name="light_base",
            value=110,
            units="W",
            description="""Base internal heat gain created by
                         lighting when fully on"""
        )

        @make_function(IHG_light)
        def cal_IHG_lgt(light_on=light_on,
                        light_base=light_base):
            """
            Calculate lighting internal heat gain.

            """
            return light_on * light_base
