"""A HVAC model with PID controller for a single zone.
# TODO: REVISE this
This model contains 4 models, PID controller, a fan model,
a heating model and a chiller model.

Then calculate the energy consumption by a chiller, a heater,
and a fan model.

Author:
    Ilias Bilionis
    Ting-Chun Kuo

Date:
    5/04/2022
    5/31/2022
    7/06/2022

"""


__all__ = ["HVACSystem"]


from cdcm import *
from scipy import signal
import numpy as np


class HVACSystem(System):
    """
    This is a demo of VAV system.
    Arguements:
    dt              --  The timestep to use (must be a node.)
    Tout            --  Outdoor air temperature [C]
    m_dot           --  The required mass flow rate [kg/s]
    Q_c             --  The required cooling load [W]
    Q_h             --  The required heating load [W]

    States:
    measured_energy  -- measured consumed energy [W]

    Function nodes:
    f_u             --  Calculate u to RC model and energy consumption

    Parameters of air property:
    cp_air          --  specific heat of air [J/kg]
    rho_air         --  density of air [kg/m**3]
    Parameters of heatpump:
    Tlvc            --  heatpump leaving water temperature [C]
    T_sup           --  supply air temperature [C]
    COPh            --  heatpump heating efficiency coefficient
    EFc             --  heatpump cooling efficiency coefficient
    Parameters of fan:
    c_FAN           --  fan efficiency coefficient
    m_design        --  fan design air mass flow rate[kg/s]
    dP              --  fan design pressure rise [kg/m/s**2]
    e_tot           --  fan total efficiency
    """
    def define_internal_nodes(self,
                              dt=None,
                              m_dot=None,
                              Q_h=None,
                              Q_c=None,
                              T_out=None,
                              **kwargs):

        measured_energy = Variable(
            name="measured_energy",
            value=0.0,
            units="W",
            track=True,
            description="measured energy"
        )

        u_apply = Variable(
            name="u_apply",
            value=0.0,
            units="W",
            description="applied u to the rc model")

        cp_air = Parameter(
            name="cp_air",
            value=1004,
            units="J/kg",
            description="specific heat of air"
        )

        rho_air = Parameter(
            name="rho_air",
            value=1.225,
            units="kg/m**3",
            description="density of air"
        )

        Tlvc = Parameter(
            name="Tlvc",
            value=7.0,
            units="C",
            description="heatpump leaving water temperature"
        )

        T_sup = Parameter(
            name="T_sup",
            value=16.5,
            units="C",
            description="supply air temperature"
        )

        COPh = Parameter(
            name="COPh",
            value=0.9,
            units=None,
            description="heatpump heating efficiency coefficient"
        )

        EFc = Parameter(
            name="EFc",
            value=np.array(
                [14.8187, -0.2538, 0.1814, -0.0003, -0.0021, 0.002]
            ),
            units=None,
            description="heatpump cooling efficiency coefficient"
        )

        c_FAN = Parameter(
            name="c_FAN",
            value=np.array(
                [0.040759894, 0.08804497, -0.07292612, 0.943739823, 0]
            ),
            units=None,
            description="fan efficiency coefficient"
        )

        m_design = Parameter(
            name="m_design",
            value=0.9264*0.4,
            units="kg/s",
            description="fan design air mass flow rate"
        )

        dP = Parameter(
            name="dP",
            value=500,
            units="kg/m/s**2",
            description="fan design pressure rise"
        )

        e_tot = Parameter(
            name="e_tot",
            value=0.6045,
            units=None,
            description="fan total efficiency"
        )

        @make_function(measured_energy, u_apply)
        def f_u(
            dt=dt,
            Tout=T_out,
            Q_h=Q_h,
            Q_c=Q_c,
            EFc=EFc,
            Tlvc=Tlvc,
            cp_air=cp_air,
            T_sup=T_sup,
            COPh=COPh,
            m_design=m_design,
            m_dot=m_dot,
            c_FAN=c_FAN,
            e_tot=e_tot,
            rho_air=rho_air,
            dP=dP
        ):
            COPc = (
                EFc[0] + Tout * EFc[1] + Tlvc * EFc[2]
                + (Tout ** 2) * EFc[3]
                + (Tlvc ** 2) * EFc[4] + Tout * Tlvc * EFc[5]
            )
            energy = (Q_h / COPh + Q_c / COPc) / 1000 * (dt / 3600)

            f_flow = m_dot / m_design
            f_pl = (c_FAN[0] + c_FAN[1] * f_flow +
                    c_FAN[2] * f_flow**2 + c_FAN[3] * f_flow**3
                    + c_FAN[4] * f_flow**4)
            Q_fan = f_pl * m_design * dP / (e_tot * rho_air)

            energy += Q_fan/1000*(dt/3600)

            return energy, Q_h+Q_c

