"""
A Damped Harmonic Oscialltor CDCM System for testing cdcm jax capabilities

Author:
    Sreehari Manikkan
Date:
    02/27/2024
"""

from cdcm import *
import numpy as np

__all__ = ["make_duff_osc_sys"]

class DuffingOscillator(System):

    def __init__(self, name, **kwargs):
        super().__init__(name=name, **kwargs)

    def define_internal_nodes(self, dt, **kwargs):

        input_sys = make_data_system(**kwargs["input_data"])

        force = input_sys.force
                       
        alpha = Parameter(
            value=1.,
            name='alpha',
            units=None,
        )
        beta = Parameter(
            value=5.,
            name='beta',
            units=None,
        )
        gamma = Parameter(
            value=.37,
            name='gamma',
            units=None,
        )
        delta = Parameter(
            value=.1,
            name='delta',
            units=None,
        )

        n1 = Parameter(
            value=0.01,
            name="n1",
            units="m",
            description="noise of emission y1"
        )

        n2 = Parameter(
            value=0.01,
            name="n2",
            units="m",
            description="noise of emission y2"
        )
        
        x1 = State(
            name="x1",
            value=0.,
            units="m",
        )
        
        x2 = State(
            name="x2",
            value=1.,
            units="m/s",
        )

        y1 = Variable(
            name="y1",
            value=0.,
            units="m",
        )

        y2 = Variable(
            name="y2",
            value=0.,
            units="m",
        )

        x2_rhs = Variable(
            name="x2_rhs",
            value=0.,
            units=None,
        )

        @make_function(y1,y2)
        def calc_y1_y2(x1=x1,x2=x2,n1=n1,n2=n2):
            return x1 + n1*np.random.randn(), x2 + n2*np.random.randn()
        
        
        @make_function(x1)
        def calc_x1(x1=x1, x2=x2, dt=dt):
            return x1 + x2*dt
        
        @make_function(x2_rhs)
        def calc_x2_rhs(
            x2=x2,
            x1=x1,
            a=alpha,
            b=beta,
            g=gamma,
            d=delta,
            f=force,
        ):
            return -a*x1-b*x1**3-d*x2+g*f
        
        @make_function(x2)
        def calc_x2(
            x2_rhs=x2_rhs,
            x2=x2,
            dt=dt
        ):
            return x2 + dt*x2_rhs


def make_duff_osc_sys(dt,name,**kwargs):
    with System(name=name) as sys:
        clock = make_clock(dt=dt, units='seconds')
        duff_osc = DuffingOscillator(
                name='duff_osc', 
                dt=clock.dt,
                **kwargs,
        )
    return sys