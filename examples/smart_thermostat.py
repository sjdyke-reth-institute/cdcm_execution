"""
This is a simple Smart thermostat
including a setpoint schedule, PID controller and control logic.

Theromstat takes the setpoint temperature (T_sp) as the control signal,
then transfer the T_sp into input loads by PID controller.

e(t) =& T_{sp, t} - T_{room, t} \\
u_t =& K_p e(t) + K_i \int^t_0 e(\tau)d\tau + K_d
\frac{e(t)}{dt} \\
\int^t_0 e(\tau)d\tau =& int^{t-1}_0 e(\tau)d\tau
+ e(t) dt\\
\frac{e(t)}{dt} =& \frac{e(t)-e(t-1)}{dt}

Author:
    Ting-Chun Kuo

Date:
    5/31/2022
"""

__all__ = ["SmartThermostat"]


from cdcm import *
import numpy as np


class SmartThermostat(System):
    """
    This is a simple occupancy behavior model.

    Arguements:
    clock           --  The clock system
    T_sp_occ        --  Setpoint override by occupancy. -1: no change
    T_room_sensor   --  The sensored room air temperature [C] from rc system

    States:
    integral_past    --  Intergral storage of past time step
    error_past       --  Portional storage of past time step

    Variables:
    T_sp            --  The setpoint temperature [C]
    error           --  Difference between setpoint and room temperature
    integral        --  Intergral storage of the PID controller
    derivative      --  The derivative of the error
    m_dot           --  The required mass flow rate [kg/s]
    Q_c             --  The required cooling load [W]
    Q_h             --  The required heating load [W]


    Parameters:
    K_p             --  actual preference temperature of the occupant[C]
    K_i             --  action noise of the occupants
    K_d             --  occupancy sensitivity of the room temperature
    Parameters of air property:
    cp_air          --  specific heat of air [J/kg]
    rho_air         --  density of air [kg/m**3]
    u_max_h         --  maximum heating loads [W]
    u_max_c         --  maximum cooling loads [W]

    Function nodes:
    setpoint_schedule-- Setpoint schedule that can be override by the occupnacy
    f_error         --  Find difference between setpoint and room temperature.
    f_error_past    --  Keeps track of the previous step error.
    f_integral      --  Find the next value of integral.
    f_integral_past --  Store the current value of the integral.
    f_derivative    --  Find the derivative of the error.
    PID             --  Calculate ideal u
    control_logic   --  Calculate m_dot, Q_c, Q_h to the HVAC system

    """
    def __init__(self,
                 clock: System,
                 T_sp_occ: Variable,
                 T_room_sensor: Variable,
                 **kwargs):
        super().__init__(**kwargs)

        T_sp = Variable(
            name="T_sp",
            value=23,
            units="degC",
            description="The setpoint temperature to hvac system"
        )

        @make_function(T_sp)
        def setpoint_schedule(time=clock.t, T_sp_occ=T_sp_occ):
            hour = time/3600 % 24
            if T_sp_occ == -1:
                # Follow schedule
                if (hour >= 8) and (hour <= 17):
                    return 23.0
                else:
                    return 18.0
            else:
                return T_sp_occ

        # TODO: Write decorator to simplify the following
        error = Variable(
            name="error",
            units="degC",
            value=0.0,
            description="Difference between setpoint and room temperature"
        )

        @make_function(error)
        def f_error(T_sp=T_sp, T_room=T_room_sensor):
            """Find difference between setpoint and room temperature."""
            return T_sp - T_room

        error_past = State(
            name="error_past",
            value=0.0,
            units="degC",
            description="The error in the previous step."
        )

        @make_function(error_past)
        def f_error_past(error_past=error_past, error=error):
            """Keeps track of the previous step error."""
            return error
        # END OF TODO

        # TODO: Write decorator to simplify the following
        integral = Variable(
            name="integral",
            value=0.0,
            units="degC * seconds",
            description="Intergral storage of the PID controller"
        )

        integral_past = State(
            name="integral_past",
            value=0.0,
            units="degC * seconds",
            description="Keeps track of the intgral in the previous timestep"
        )

        @make_function(integral)
        def f_integral(integral_past=integral_past, error=error, dt=clock.dt):
            """Find the next value of integral."""
            return integral_past + error * dt

        @make_function(integral_past)
        def f_integral_past(integral_past=integral_past, integral=integral):
            """Store the current value of the integral."""
            return integral

        derivative = Variable(
            name="derivative",
            value=0.0,
            description="The derivative of the error",
        )

        @make_function(derivative)
        def f_derivative(error_past=error_past, error=error, dt=clock.dt):
            """Find the derivative of the error."""
            return (error - error_past) / dt
        # END TODO

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

        u_max_h = Parameter(
            name="u_max_h",
            value=1500,
            units="W",
            description="maximum heating loads"
        )

        u_max_c = Parameter(
            name="u_max_c",
            value=-1500,
            units="W",
            description="maximum cooling loads"
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

        T_sup = Parameter(
            name="T_sup",
            value=16.5,
            units="C",
            description="supply air temperature"
        )

        cp_air = Parameter(
            name="cp_air",
            value=1004,
            units="J/kg",
            description="specific heat of air"
        )

        u_ideal = Variable(
            name="u_ideal",
            value=0,
            units="W",
            description="Ideal input heat fluxto hvac system"
        )

        m_dot = Variable(
            name="m_dot",
            value=0,
            units="kg/s",
            description="Required mass flow rate"
        )

        Q_h = Variable(
            name="Q_h",
            value=0,
            units="W",
            description="Required heating loads"
        )

        Q_c = Variable(
            name="Q_c",
            value=0,
            units="W",
            description="Required cooling loads"
        )

        @make_function(u_ideal)
        def PID(Kp=Kp, Ki=Ki, Kd=Kd, error=error, integral=integral,
                derivative=derivative):
            return Kp * error + Ki * integral + Kd * derivative

        @make_function(m_dot, Q_h, Q_c)
        def control_logic(u_ideal=u_ideal,
                          u_max_c=u_max_c,
                          u_max_h=u_max_h,
                          m_dot_max=m_dot_max,
                          m_dot_min=m_dot_min,
                          cp_air=cp_air,
                          T_sup=T_sup,
                          T_room=T_room_sensor
                          ):
            if u_ideal > u_max_h:
                u_ideal = u_max_h
            elif u_ideal <= u_max_c:
                u_ideal = u_max_c

            if u_ideal <= 0:  # cooling case
                u_c = u_ideal
                u_h = 0
                dp = -u_ideal / 2000
                m_fan = (m_dot_max - m_dot_min) * dp + m_dot_min
            elif u_ideal > 0:  # heating case
                u_c = m_dot_min * cp_air * (T_sup - T_room)
                u_h = u_ideal
                m_fan = m_dot_min
            return m_fan, u_h, u_c

        self.add_nodes(
                    [
                        T_sp,
                        setpoint_schedule,
                        error,
                        f_error,
                        error_past,
                        f_error_past,
                        integral,
                        f_integral,
                        integral_past,
                        f_integral_past,
                        derivative,
                        f_derivative,
                        Kp,
                        Ki,
                        Kd,
                        u_max_h,
                        u_max_c,
                        m_dot_min,
                        m_dot_max,
                        T_sup,
                        cp_air,
                        u_ideal,
                        m_dot,
                        Q_h,
                        Q_c,
                        PID,
                        control_logic
                    ]
                )
