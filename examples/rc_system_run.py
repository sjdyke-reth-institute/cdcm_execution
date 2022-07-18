"""An RC model for a single zone.

Author:
    Ilias Bilionis
    Ting-Chun Kuo

Date:
    4/20/2022
    7/06/2022

"""

import os

from cdcm import *
from rc_system import RCBuildingSystem
import pandas as pd

# df = pd.read_csv("examples/rc_system_data/weather_data_2017_pandas.csv")
df = pd.read_csv("rc_system_data/weather_data_2017_pandas.csv")

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

clock = make_clock(1800)

rc_sys = RCBuildingSystem(dt=clock.dt,
                          weather_system=weather_sys,
                          T_cor=T_cor,
                          Q_int=Q_int,
                          u=u_t,
                          name="rc_sys")

sys = System(
    name="everything",
    nodes=[clock, weather_sys, rc_sys]
)

print(sys)
max_steps = 1000
file_name = "test_make_rc_of_cdcm_det.h5"

if os.path.exists(file_name):
        os.remove(file_name)

test_saver_det = SimulationSaver(file_name,
                            sys,
                            max_steps=max_steps
)
for i in range(100):
    sys.forward()
    print(f"T_room = {rc_sys.T_room.value:1.2f}")
    test_saver_det.save()
    sys.transition()