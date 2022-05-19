"""
This is a coupled system demo of HVAC system and rc system.
By adding noise to the weather data, we simulate conditions with sensors.

Author:
    Ilias Bilionis
    Ting-Chun Kuo

Date:
    5/5/2022

"""

from rc_system import RCBuildingSystem
from hvac_system import HVACSystem
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

# TODO: Make sensor model to make this simpler
# Add a sensor to weather system
T_out_sensor = Variable(
    name="T_out_sensor",
    units="degC",
    description="Measurement of external temperature."
)
T_out_sensor_sigma = Parameter(
    name="T_out_sensor_sigma",
    units="degC",
    value=0.01
)

T_sp = Variable(
    name="T_sp",
    units="degC",
    value=23
)


@make_function(T_out_sensor)
def g_T_out_sensor(T_out=weather_sys.Tout, sigma=T_out_sensor_sigma):
    """Sample the T_out sensor."""
    return T_out + sigma * np.random.randn()


# A clock
clock = make_clock(300)

# The RC model
rc_sys = RCBuildingSystem(clock.dt, weather_sys, Q_int, name="rc_sys")

# The HVAC model
hvac_sys = HVACSystem(
    clock.dt,
    T_out_sensor,
    rc_sys.T_room_sensor,
    rc_sys.u,
    T_sp,
    name="hvac_sys"
)

# The combined system

sys = System(
    name="everything",
    nodes=[clock, weather_sys, rc_sys, hvac_sys]
)
print(sys)

print("A should have shpae of :", np.shape(rc_sys.A.value))
for i in range(100):
    sys.forward()
    print(f"T_room = {rc_sys.T_room.value:1.2f}")
    sys.transition()
