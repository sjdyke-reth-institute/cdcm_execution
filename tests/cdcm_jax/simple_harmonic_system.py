"""
A Damped Harmonic Oscialltor CDCM System for testing cdcm jax capabilities

Author:
    Sreehari Manikkan
Date:
    02/27/2024
"""

from cdcm import *
import numpy as np

__all__ = ["make_dsh_sys"]

class DampedHarmonicOscillator(System):

    def __init__(self, name, **kwargs):
        super().__init__(name=name, **kwargs)

    def define_internal_nodes(self, dt, **kwargs):

        input_sys = make_data_system(**kwargs["input_dict"])
                       
        zeta = Parameter(
            value=kwargs["zeta_val"],
            name='zeta',
            units=None,
        )
        omega_o = Parameter(
            value=2.16,
            name='omega_o',
            units="rad/s",
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

        @make_function(y1,y2)
        def calc_y1_y2(x1,x2,n1,n2):
            return x1 + n1*np.random.randn(), x2 + n2*np.random.randn()
        
        
        @make_function(x1)
        def calc_x1(x1=x1, x2=x2, dt=dt):
            return x1 + x2*dt
        
        @make_function(x2)
        def calc_x2(
            x1=x1,
            x2=x2,
            wo=omega_o,
            z=zeta,
            dt=dt
        ):
            return x2 + dt*(-2*z*wo*x2-wo**2*x1)


def make_dsh_sys(dt,name,zeta_val):
    with System(name=name) as sys:
        clock = make_clock(dt=dt, units='seconds')
        dho = DampedHarmonicOscillator(
                name='dho', 
                dt=clock.dt,
                zeta_val=zeta_val
        )
    return sys