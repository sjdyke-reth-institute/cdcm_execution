"""
Author: Amir Behjat

Date:
    7/12/2022

Defines the concept of `ShocksEnvironment`.


                     _______________________
                    |                      |
clock  :: Clock  => |  ShocksEnvironment   |-> high_current :: Variable
                    |______________________|

"""

from cdcm import *

import random
import numpy as np


__all__ = ["make_current_shock_env_0"]


def make_current_shock_env_0(clock,
                             battery_specs):
    with System(name="current_shock", description="The  environment") as current_shock:

        high_current = Variable(
            name="_rate",
            value=0.0,
            units="1/hour",
            description=" Events of having Extra current per hour nominator is actually % of the current over the nominal current it s not just 1 but A/A"
        )  # was Variable; Change it to State for consistency if you want

        high_current = Parameter(
            name="high_current",
            value=0.0,
            units="1/hour",
            description="rate that high current rate events happen"
        )
        high_current_distribution_mean = Parameter(
            name="high_current_distribution_mean",
            value=10.0,
            units="",
            description="Mean of the high current values"
        )
        high_current_distribution_std = Parameter(
            name="high_current_distribution_std",
            value=7.5,
            units="",
            description="Standard deviation of the high current values"
        )

        @make_function(high_current)
        def f_shock_rate(
            high_current_distribution_mean=high_current_distribution_mean,
            high_current_distribution_std=high_current_distribution_std,
            t=clock.t
        ):
            """Calculate the high current rate"""
            if t == 0.0:
                return 0.0
            else:
                return max(0.0, (high_current_distribution_mean + np.random.normal(0.0, high_current_distribution_std)))

    return current_shock
