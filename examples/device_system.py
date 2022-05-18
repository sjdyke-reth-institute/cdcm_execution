"""
This is a simple model of ON/OFF devices system

$$IHG_{dev} = dev_{on} * dev_{base}$$

Author:
    Ting-Chun Kuo

Date:
    5/17/2022

"""

__all__ = ["DeviceSystem"]


from cdcm import *


class DeviceSystem(System):
    """
    This is a simple device system model.

    Arguements:
    dt              --  The timestep to use (must be a node.)
    dev_on          --  The ON/OFF indicator of devices

    States:
    IHG_dev         --  Internal heat gain at the time step [W]

    Parameters:
    dev_base        --  Base internal heat gain created by
                        devices when fully on

    Function nodes:
    cal_IHG_dev     --  calculate internal heat gain


    """
    def __init__(self,
                 dt: Parameter,
                 dev_on:Variable,
                 **kwargs):
        super().__init__(**kwargs)

        IHG_dev = State(
            name="IHG_dev",
            value=0.0,
            units="W",
            description="Internal heat gain at the time step"
        )

        dev_base = Parameter(
            name="dev_base",
            value=500,
            units="W",
            description="Base internal heat gain created by \
                         devices when fully on"
        )

        @make_function(IHG_dev)
        def cal_IHG_dev(dev_on=dev_on,
                        dev_base=dev_base):
            """
            Calculate internal heat gain

            """
            return dev_on * dev_base

        self.add_nodes([
                IHG_dev,
                dev_base,
                cal_IHG_dev
            ])