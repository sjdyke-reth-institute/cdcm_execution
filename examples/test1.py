"""
Example of creating an RC model of a single zone fully deterministic
building from YABML in CDCM.

Author(s):
    Sreehari Manikkan
Date:
    05/16/2022
"""
import pandas as pd
import yaml

from yabml import *
from cdcm import *

from building_rc_system import rc_of_building
from single_zone import single_zone_building

#df = pd.read_csv("examples/rc_system_data/weather_data_2017_pandas.csv")
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

for sample_building in single_zone_building.sample(1):
    rc_sample = rc_of_building(sample_building, weather_sys, clock)
    print('\n',rc_sample[0].R_oe,
            '\n',rc_sample[0].C_env,
            '\n',rc_sample[0].R_er,
            '\n',rc_sample[0].R_gr,
            '\n',rc_sample[0].R_ge,
            '\n', rc_sample[0].C_genv,
            '\n',rc_sample[0].R_rc,
            '\n', rc_sample[0].A,
            '\n', rc_sample[0].B)
    sys = System(
            name="everything",
            nodes=[clock, weather_sys, rc_sample[0]]
    )
    
    '''max_steps = 2
    saver = SimulationSaver("test_rc.h5", sys, max_steps=max_steps)

    for i in range(max_steps):
        sys.forward()
        saver.save()
        sys.transition()

    T_room_sensor = (
        saver.file_handler["/everything/zone_rc_sys/T_room_sensor"][:]
    )
    print(T_room_sensor)'''