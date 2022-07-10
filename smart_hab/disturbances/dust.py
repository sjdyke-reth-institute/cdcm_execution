"""
Author: Amir Behjat

Date:
    7/08/2022

Defines the concept of `MoonDustEnvironment`.

What is a MoonDustEnvironment?

It is a System that provides access to the following variables:

        dust_rate = Variable(
            name="dust_rate",
            value=0.0,
            units="1/sec/m^2",
            description="Dust deposition rate per unit time and area on a horizontal surface."
        )

We say that any `System` that has a `dust_rate` matching the above
specification is an **instance** of the `MoonDustEnvironment`
**interface**.

Say that `moon_dust` is an instance of the `MoonDustEnvironment`
interface. This means, that it has a variable `moon_dust.dust_rate`
and that any system that interacts with it can only do so
through that variable.

 _____________________
|                     |
| MoonDustEnvironment |-> dust_rate
|_____________________|

There many implentations of a `MoonDustEnvironment`.
Each one of these implementations has a **constructor**.
A **constructor** is a function that makes `MoonDustEnvironment`s.

A constructor for a `MoonDustEnvironment` is a function that
requires an instance of a `Clock` and returns an instance of
a `MoonDustEnvironment`.

Suggestions for future?

                     _______________________
                    |                      |
clock  :: Clock  => |  MoonDustEnvironment |-> dust_rate :: Variable
                    |______________________|

"""

from cdcm import *

import random
import numpy as np


__all__ = ["make_dust_env_0"]


def make_dust_env_0(clock):
    with System(name="dust", description="The dust environment") as dust:
        # It absolutely essential to define this.
        # Because this implements the interface:
        dust_rate = Variable(
            name="dust_rate",
            value=0.0,
            units="1/sec",
            description="Dust deposition rate"
        )  # was Variable; Change it to State for consistency if you want

        # Whatever follows is particular to this implementation
        # of the MoonDustEnvironment:
        mean_dust_rate = Parameter(
            name="mean_dust_rate",
            value=1.0,
            units="1/sec",
            description="Average dust deposition rate"
        )
        std_dust_rate = Parameter(
            name="std_dust_rate",
            value=0.25,
            units="1/sec",
            description="Standard deviation of dust deposition rate"
        )

        @make_function(dust_rate)
        def f_dust_rate(
            mean_dust_rate=mean_dust_rate,
            std_dust_rate=std_dust_rate,
            t=clock.t
        ):
            """Calculate the dust rate"""
            if t == 0.0:
                return 0.0
            else:
                return 0.1 * 0.2 * 0.005 * \
                    (mean_dust_rate + np.random.random() * std_dust_rate)

    return dust
