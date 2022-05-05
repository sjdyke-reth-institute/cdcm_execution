"""An RC model for a single zone.
This file include an external PID-controller
that interact with the system.
Author:
    Ilias Bilionis
    Ting-Chun Kuo

Date:
    4/29/2022
"""


from cdcm import *
from rc_system import RCBuildingSystem
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def PID(T_room, T_out, T_sp, integral, e_p,
        Kp=20.0, Ki=0.1, Kd=0.0, dt_PI=1800,
        u_max=1500, m_dot_max=0.080938984*550/140, m_dot_min=0.080938984,
        Tlvc=7.0, T_sup=16.5, cp_air=1004, rho_air=1.225,
        EFc=np.array([14.8187, -0.2538, 0.1814, -0.0003, -0.0021, 0.002]),
        m_design=0.9264*0.4, dP=500, e_tot=0.6045,
        c_FAN=np.array([0.040759894, 0.08804497,
                        -0.07292612, 0.943739823, 0])):
    err = T_sp - T_room
    integral += err*dt_PI
    derivative = (err - e_p) / dt_PI
    u_t = Kp * err + Ki * integral + Kd * derivative

    # bound u_t by upper limit
    if abs(u_t) > u_max:
        u_t = u_t/abs(u_t)*u_max
    COPh = 0.9
    COPc = EFc[0] + T_out*EFc[1] + Tlvc*EFc[2] + (T_out**2)*EFc[3] + \
        (Tlvc**2)*EFc[4] + T_out*Tlvc*EFc[5]
    if u_t <= 0:  # cooling case
        dp = -u_t/2000
        m_fan = (m_dot_max - m_dot_min) * dp + m_dot_min
        energy = -1*u_t/COPc/1000*(dt_PI/3600)
    elif u_t > 0:  # heating case
        u_c = m_dot_min*cp_air*(T_sup - T_room)
        u_h = u_t
        u_t = u_c + u_h
        m_fan = m_dot_min
        energy = (u_h / COPh + u_c / COPc) / 1000*(dt_PI/3600)

    f_flow = m_fan / m_design
    f_pl = c_FAN[0] + c_FAN[1] * f_flow + c_FAN[2] * f_flow**2 + \
        c_FAN[3] * f_flow**3 + c_FAN[4] * f_flow**4
    Q_fan = f_pl * m_design * dP / (e_tot * rho_air)
    energy += Q_fan/1000*(dt_PI/3600)

    e_p = err
    return integral, e_p, u_t, energy


df = pd.read_csv("examples/rc_system_data/weather_data_2017_pandas.csv")

weather_sys = make_data_system(
    df[["Tout", "Qsg", "Qint"]],
    name="weather_sytem",
    column_units=["degC", "Wh", "Wh"],
    column_desciptions=[
        "Outdoor air temperature",
        "Solar irradiance",
        "Internal heat gain"
    ]
)

clock = make_clock(300)

rc_sys = RCBuildingSystem(clock.dt, weather_sys, name="rc_sys")

sys = System(
    name="everything",
    nodes=[clock, weather_sys, rc_sys]
)

print(sys)

T_room = []
T_out = []
u_list = []
energy_list = []
T_sp_list = []
# add PID controller here
T_sp = 23
Kp = 20.0
Ki = 0.1
Kd = 0.0
e_p = 0.0
integral = 0.0
dt_PI = 300
for i in range(100):
    sys.forward()
    T_room_t = rc_sys.T_room.value
    T_out_t = weather_sys.Tout.value

    # Run PID to calculate u_t
    integral, e_p, u_t, energy = PID(T_room_t,
                                     T_out_t, T_sp, integral, e_p)
    # Keep track with some measurement
    T_sp_list.append(T_sp)
    u_list.append(u_t)
    energy_list.append(energy)
    T_room.append(T_room_t)
    T_out.append(T_out_t)
    sys.rc_sys.u.value = u_t
    print(f"T_room = {rc_sys.T_room.value:1.2f}")
    sys.transition()

fig, axs = plt.subplots(4, figsize=(10, 7))
fig.suptitle('PID_controller_Performance')
axs[0].plot(T_room, label='Troom')
axs[0].plot(T_sp_list, label='T_sp')
axs[0].legend()
axs[0].set(ylabel='Temperature[C]')
axs[1].plot(T_out, label='Tout')
axs[1].legend()
axs[1].set(ylabel='Outdoor Air Temperature[C]')
axs[2].plot(u_list)
axs[2].set(ylabel='input loads[W]')
axs[3].plot(energy_list)
axs[3].set(ylabel='Energy Consumption[kW]')
plt.show()
