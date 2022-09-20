"""
This is a simple model of ON/OFF devices system

$$IHG_{device} = device_{on} * device_{base}$$

Author:
    Ting-Chun Kuo
    Sreehari Manikkan

Date:
    5/17/2022
    07/07/2022

"""

__all__ = ["DeviceSystem"]


from cdcm import *


class DeviceSystem(System):
    """
    This is a simple device system model.

    Arguements:
    dt              --  The timestep to use (must be a node.)
    device_on          --  The ON/OFF indicator of devices

    States:
    IHG_device         --  Internal heat gain at the time step [W]

    Parameters:
    device_base        --  Base internal heat gain created by
                        devices when fully on

    Function nodes:
    cal_IHG_device     --  calculate internal heat gain


    """
    def define_internal_nodes(self,
                 clock: System,
                 device_on:Variable,
                 **kwargs):

        IHG_device = State(
            name="IHG_device",
            value=0.0,
            units="W",
            description="Internal heat gain at the time step"
        )

        device_base = Parameter(
            name="device_base",
            value=500,
            units="W",
            description="""Base internal heat gain created by
                         devices when fully on"""
        )

        @make_function(IHG_device)
        def cal_IHG_device(device_on=device_on,
                        device_base=device_base):
            """
            Calculate internal heat gain

            """
            return device_on * device_base