"""
This is a coupled system demo of HVAC system, rc system, occupancy,
lighting, and devices system.
By adding noise to the weather data, we simulate conditions with sensors.

Author:
    Ting-Chun Kuo

Date:
    5/18/2022

"""

from rc_system import RCBuildingSystem
from smart_thermostat import SmartThermostat
from hvac_system import HVACSystem
from occupant_system import OccupantSystem
from device_system import DeviceSystem
from lighting_system import LightingSystem
from cdcm import *
import pandas as pd
import numpy as np

df = pd.read_csv("./rc_system_data/weather_data_2017_pandas.csv")

# WEATHER SYSTEM
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

Q_int = Variable(
    name="Q_int",
    units="W",
    value=150,
    description="Sum of internal heat gain"
)

u_t = Variable(
    name="u_t",
    units="W",
    value=0.0,
    description="Input loads"
)

T_cor = Variable(
    name="T_cor",
    units="degC",
    value=23,
    description="Corridor temperature"
)

# TODO: Make sensor model to make this simpler
# Add a sensor to weather system
T_out_sensor = Variable(
    name="T_out_sensor",
    units="degC",
    value=18.0,
    description="Measurement of external temperature."
)
T_out_sensor_sigma = Parameter(
    name="T_out_sensor_sigma",
    units="degC",
    value=0.01
)


@make_function(T_out_sensor)
def g_T_out_sensor(T_out=weather_sys.Tout, sigma=T_out_sensor_sigma):
    """Sample the T_out sensor."""
    return T_out + sigma * np.random.randn()


# A clock
clock = make_clock(300)

# The RC model
rc_sys = RCBuildingSystem(clock.dt, weather_sys, T_cor, Q_int,
                          u_t, name="rc_sys")

# The occupancy behavior model
occ_sys = OccupantSystem(
    clock,
    rc_sys.T_room_sensor
    )

thermostat = SmartThermostat(
    clock,
    occ_sys.action,
    rc_sys.T_room_sensor,
    name="thermostat")

# The HVAC model
hvac_sys = HVACSystem(
    clock.dt,
    thermostat.m_dot,
    thermostat.Q_h,
    thermostat.Q_c,
    T_out_sensor,
    name="hvac_sys"
)

lgt_sys = LightingSystem(
    clock.dt,
    occ_sys.lgt_on,
    name="lgt_sys"
    )

dev_sys = DeviceSystem(
    clock.dt,
    occ_sys.dev_on,
    name="dev_sys"
    )


IHG_noise = Parameter(
    name="IHG_noise",
    units="W",
    value=100
)


@make_function(Q_int)
def cal_Q_int(IHG_occ=occ_sys.IHG_occ,
              IHG_lgt=lgt_sys.IHG_lgt,
              IHG_dev=dev_sys.IHG_dev,
              sigma=IHG_noise):
    IHG = IHG_occ + IHG_lgt + IHG_dev + sigma * np.random.randn()
    return IHG


@make_function(u_t)
def input_loads_from_hvac(u_apply=hvac_sys.u_apply):
    return u_apply

# The combined system


sys = System(
    name="everything",
    nodes=[clock, weather_sys, rc_sys, thermostat,
           hvac_sys, occ_sys, lgt_sys, dev_sys,
           g_T_out_sensor, cal_Q_int, input_loads_from_hvac]
)
print(sys)

for i in range(100):
    sys.forward()
    print(f"T_out = {weather_sys.Tout.value:1.2f}")
    print(f"T_out_noisy = {T_out_sensor.value:1.2f}")
    print(f"T_room = {rc_sys.T_room.value:1.2f}")
    print(f"action = {occ_sys.action.value:1.0f}")
    print(f"IHG = {Q_int.value:1.2f}")
    sys.transition()
