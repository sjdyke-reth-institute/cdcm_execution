"""An RC model for a single zone.

Author:
    Ilias Bilionis
    Ting-Chun Kuo

Date:
    4/20/2022

"""


from cdcm import *
from rc_system import RCBuildingSystem
import pandas as pd


df = pd.read_csv("./rc_system_data/weather_data_2017_pandas.csv")

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

clock = make_clock(1800)

rc_sys = RCBuildingSystem(clock.dt, weather_sys, name="rc_sys")

sys = System(
    name="everything",
    nodes=[clock, weather_sys, rc_sys]
)

print(sys)

for i in range(100):
    sys.forward()
    print(f"T_room = {rc_sys.T_room.value:1.2f}")
    sys.transition()
