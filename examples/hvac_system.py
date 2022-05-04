"""A HVAC model with PID controller for a single zone.

Author:
    Ting-Chun Kuo

Date:
    5/4/2022

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
    weather_system  --  A weather system that includes:
                        Tout: outdoor air temperature
                        Qsg:  solar irradiance
                        Qint: internal heat gain
                        T_gd: ground temperature

    rc_system       --  A rc system that includes:
                        T_room: The room air temperature [C]
    Variables:
    T_sp            --  The setpoint temperature [C]

    States:
    integral        --  Intergral storage of the PID controller
    e_p             --  Portional storage of the PID controller
    u               --  Required input loads to the building/zone [W]
    energy          --  Consumed energy [W]

    Parameters of PID controller:
    Kp              --  proportional coefficient of PID controller
    Ki              --  integral coefficient of PID controller
    Kd              --  derivative coefficient of PID controller
    Parameters of air property:
    cp_air          --  specific heat of air [J/kg]
    rho_air         --  density of air [kg/m**3]
    Parameters of heatpump:
    u_max_h         --  maximum heating loads [W]
    u_max_c         --  maximum cooling loads [W]
    Tlvc            --  heatpump leaving water temperature [C]
    T_sup           --  supply air temperature [C]
    COPh            --  heatpump heating efficiency coefficient
    EFc             --  heatpump cooling efficiency coefficient
    Parameters of fan:
    c_FAN           --  fan efficiency coefficient
    m_design        --  fan design air mass flow rate[kg/s]
    m_dot_max       --  maximum fan design air mass flow rate[kg/s]
    m_dot_min       --  minimum fan design air mass flow rate[kg/s]
    dP              --  fan design pressure rise [kg/m/s**2]
    e_tot           --  fan total efficiency
    """
    def __init__(self,
                 dt: Parameter,
                 weather_system: System,
                 rc_system: System,
                 **kwargs):
        super().__init__(**kwargs)

        T_sp = Variable(
            name="T_sp",
            value=23,
            description="Setpoint tempertature of the system"
        )

        integral = State(
            name="integral",
            value=0.0,
            units=None,
            track=True,
            description="Intergral storage of the PID controller"
        )
        e_p = State(
            name="e_p",
            value=0.0,
            units=None,
            track=True,
            description="Portional storage of the PID controller"
        )

        u = State(
            name="u",
            value=0.0,
            units="W",
            track=True,
            description="Required input loads to the building/zone"
        )

        energy = State(
            name="energy",
            value=0.0,
            units="W",
            track=True,
            description="Consumed energy"
        )

        Kp = Parameter(
            name="Kp",
            value=20,
            units=None,
            description="proportional coefficient of PID controller"
        )

        Ki = Parameter(
            name="Ki",
            value=0.1,
            units=None,
            description="integral coefficient of PID controller"
        )

        Kd = Parameter(
            name="Kd",
            value=0.0,
            units=None,
            description="derivative coefficient of PID controller"
        )

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

        u_max_h = Parameter(
            name="u_max_h",
            value=1500,
            units="W",
            description="maximum heating loads"
        )

        u_max_c = Parameter(
            name="u_max_c",
            value=1500,
            units="W",
            description="maximum cooling loads"
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
            value=np.array([14.8187, -0.2538, 0.1814, -0.0003, -0.0021,
                            0.002]),
            units=None,
            description="heatpump cooling efficiency coefficient"
        )

        c_FAN = Parameter(
            name="c_FAN",
            value=np.array([0.040759894, 0.08804497, -0.07292612, 0.943739823,
                            0]),
            units=None,
            description="fan efficiency coefficient"
        )

        m_design = Parameter(
            name="m_design",
            value=0.9264*0.4,
            units="kg/s",
            description="fan design air mass flow rate"
        )

        m_dot_max = Parameter(
            name="m_dot_max",
            value=0.080938984*550/140,
            units="kg/s",
            description="maximum fan design air mass flow rate"
        )

        m_dot_min = Parameter(
            name="m_dot_min",
            value=0.080938984,
            units="kg/s",
            description="minimum fan design air mass flow rate"
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

        @make_function(u, integral, e_p, energy)
        def transition_hvac(
            T_sp=T_sp,
            integral=integral, e_p=e_p, energy=energy, u=u,
            Kp=Kp, Ki=Ki, Kd=Kd,
            u_max_h=u_max_h, u_max_c=u_max_c,
            Tlvc=Tlvc, T_sup=T_sup, EFc=EFc, COPh=COPh,
            cp_air=cp_air, rho_air=rho_air,
            c_FAN=c_FAN, dP=dP, e_tot=e_tot,
            m_dot_max=m_dot_max, m_dot_min=m_dot_min, m_design=m_design,
            dt=dt,
            Tout_PID=weather_system.Tout,
            T_room=rc_system.T_room
        ):
            """Transitions the system."""
            err = T_sp - T_room
            integral += err*dt
            derivative = (err - e_p) / dt
            u_t = Kp * err + Ki * integral + Kd * derivative

            # bound u_t by upper limit
            if u_t > u_max_h:
                u_t = u_max_h
            elif u_t < u_max_c:
                u_t = u_max_c
            COPc = (EFc[0] + Tout_PID*EFc[1] + Tlvc*EFc[2]
                    + (Tout_PID**2)*EFc[3] +
                    (Tlvc**2)*EFc[4] + Tout_PID*Tlvc*EFc[5])
            if u_t <= 0:  # cooling case
                dp = -u_t/2000
                m_fan = (m_dot_max - m_dot_min) * dp + m_dot_min
                energy = -1*u_t/COPc/1000*(dt/3600)
            elif u_t > 0:  # heating case
                u_c = m_dot_min*cp_air*(T_sup - T_room)
                u_h = u_t
                u_t = u_c + u_h
                m_fan = m_dot_min
                energy = (u_h / COPh + u_c / COPc) / 1000*(dt/3600)

            f_flow = m_fan / m_design
            f_pl = (c_FAN[0] + c_FAN[1] * f_flow +
                    c_FAN[2] * f_flow**2 + c_FAN[3] * f_flow**3
                    + c_FAN[4] * f_flow**4)
            Q_fan = f_pl * m_design * dP / (e_tot * rho_air)
            energy += Q_fan/1000*(dt/3600)
            e_p = err
            return u_t, integral, e_p, energy

        self.add_nodes([
            integral, e_p,
            energy, u, T_sp,
            Kp, Ki, Kd,
            u_max_h, u_max_c,
            Tlvc, T_sup, EFc, COPh,
            cp_air, rho_air,
            c_FAN, dP, e_tot,
            m_dot_max, m_dot_min, m_design,
            transition_hvac
            ]
        )
