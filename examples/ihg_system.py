"""
This is a simple model of internal heat gain sources
such as lighting and devices.

Author:
    Ting-Chun Kuo

Date:
    5/11/2022

"""

__all__ = ["IHGSystem"]


from cdcm import *


class IHGSystem(System):
    """
    This is a simple internal heat gain sources model.

    Arguements:
    dt              --  The timestep to use (must be a node.)

    States:
    IHG             --  Internal heat gain at the time step [W]

    Variables:
    use_factor_lgt  --  The use percentage of ligting
    use_factor_dev  --  The use percentage of devices


    Parameters:
    lgt_base        --  Base internal heat gain created by
                        lighting when fully on
    dev_base        --  Base internal heat gain created by
                        devices when fully on

    Function nodes:
    cal_IHG         --  calculate internal heat gain


    """
    def __init__(self,
                 dt: Parameter,
                 **kwargs):
        super().__init__(**kwargs)

        IHG = State(
            name="IHG",
            value=0.0,
            units="W",
            description="Internal heat gain at the time step"
        )

        use_factor_lgt = Variable(
            name="use_factor_lgt",
            value=1.0,
            units=None,
            description="The use percentage of ligting"
        )

        use_factor_dev = Variable(
            name="use_factor_dev",
            value=1.0,
            units=None,
            description="The use percentage of devices"
        )

        lgt_base = Parameter(
            name="lgt_base",
            value=110,
            units="W",
            description="Base internal heat gain created by \
                         lighting when fully on"
        )

        dev_base = Parameter(
            name="dev_base",
            value=500,
            units="W",
            description="Base internal heat gain created by \
                         devices when fully on"
        )

        @make_function(IHG)
        def cal_action(use_factor_lgt=use_factor_lgt,
                       use_factor_dev=use_factor_dev,
                       lgt_base=lgt_base,
                       dev_base=dev_base):
            """
            Determine to act or not by temperature difference
            and a sigmoid function.

            """
            return use_factor_lgt * lgt_base + use_factor_dev * dev_base
