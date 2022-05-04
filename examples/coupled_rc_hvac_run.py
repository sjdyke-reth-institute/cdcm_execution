from rc_system import RCBuildingSystem
from hvac_system import HVACSystem
from cdcm import *
import pandas as pd
import numpy as np

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

clock = make_clock(300)

rc_sys = RCBuildingSystem(clock.dt, weather_sys, name="rc_sys")
hvac_sys = HVACSystem(clock.dt, weather_sys, rc_sys, name="hvac_sys")
replace(rc_sys.u, hvac_sys.u)
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
