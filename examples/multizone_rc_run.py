"""An RC model for 2 nighbor zones.
The temperature of corridor should be replaced as
the neighbor room nodes.

Author:
    Ting-Chun Kuo

Date:
    5/24/2022

"""


from cdcm import *
from rc_system import RCBuildingSystem
import pandas as pd
import numpy as np

# df = pd.read_csv("examples/rc_system_data/weather_data_2017_pandas.csv")
df = pd.read_csv("./rc_system_data/weather_data_2017_pandas.csv")

weather_sys = make_data_system(
    df[["Tout", "Qsg"]],
    name="weather_sytem",
    column_units=["degC", "W"],
    column_desciptions=[
        "Outdoor air temperature",
        "Solar irradiance"
    ]
)

Q_int = Variable(
    name="Q_int",
    units="W",
    value=150,
    description="Sum of internal heat gain"
)

T_cor1 = Variable(
    name="T_cor1",
    units="degC",
    value=23,
    description="Measured corridor temperature for zone 1."
)

T_cor2 = Variable(
    name="T_cor2",
    units="degC",
    value=23,
    description="Measured corridor temperature for zone 2."
)

clock = make_clock(1800)

rc_sys = RCBuildingSystem(clock.dt,
                          weather_sys,
                          T_cor1,
                          Q_int,
                          name="rc_sys_1")

rc_sys2 = RCBuildingSystem(clock.dt,
                           weather_sys,
                           T_cor2,
                           Q_int,
                           name="rc_sys_2")

T_room_sensor_sigma = Parameter(
    name="T_room1_sensor_sigma",
    units="degC",
    value=0.1
)


@make_function(T_cor1)
def g_T_cor1_sensor(T_neighbor=rc_sys2.T_room, sigma=T_room_sensor_sigma):
    """Sample the T_out sensor."""
    return T_neighbor + sigma * np.random.randn()


@make_function(T_cor2)
def g_T_cor2_sensor(T_neighbor=rc_sys.T_room, sigma=T_room_sensor_sigma):
    """Sample the T_out sensor."""
    return T_neighbor + sigma * np.random.randn()


sys = System(
    name="everything",
    nodes=[clock, weather_sys, rc_sys, rc_sys2, T_cor1, T_cor2,
           g_T_cor1_sensor, g_T_cor2_sensor]
)

print(sys)
print(sys.rc_sys_1)
# quit()

for i in range(100):
    sys.forward()
    print(f"T_room1 = {rc_sys.T_room.value:1.2f}")
    print(f"T_cor1(Measured for room 2) = {T_cor1.value:1.2f}")
    print(f"T_room2 = {rc_sys2.T_room.value:1.2f}")
    print(f"T_cor2(Measured for room 1) = {T_cor2.value:1.2f}")
    sys.transition()
