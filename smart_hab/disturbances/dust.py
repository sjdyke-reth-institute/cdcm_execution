"""A Dust deposition model."""



__all__ = ["make_dust_env_0"]



from cdcm import *
import random


def make_dust_env_0(clock):
    with System(name="dust", description="The dust environment") as dust:
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

        dust_rate = Variable(
            name="dust_rate",
            value=0.0,
            units="1/sec",
            description="Dust deposition rate"
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
                return 0.1 * 0.2 * 0.005 * random.normal(mean_dust_rate, std_dust_rate)

    return dust
