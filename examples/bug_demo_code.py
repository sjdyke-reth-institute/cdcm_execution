"""
bug_demo_code.py
This python file is used to demonstrate any ongoing bugs

Author(s):
    Sreehari Manikkan
Date:
    07/12/2022
"""

import pandas as pd
import numpy as np

from cdcm import *

from rc_system import RCBuildingSystem

def make_rc_of_cdcm(dt, weather_sys, T_cor, Q_int, u_t, name):
    """
    modified make_rc_of_cdcm function for bug testing purpose.
    """
    with RCBuildingSystem(
            dt=dt,
            weather_sys=weather_sys,
            T_cor=T_cor,
            Q_int=Q_int,
            u=u_t,
            name=name,
        ) as zone_rc_sys:
            """
            we parse the information from YABML to CDCM system by setting
            the values of C and R parameters of CDCM RC system with the values
            we obtained.
            """
            zone_rc_sys.C_room.value = 10**5
            zone_rc_sys.C_env.value = 200
            zone_rc_sys.C_genv.value = 3.8*10**4
            zone_rc_sys.R_rc.value = 0.001
            zone_rc_sys.R_oe.value = 0.0023
            zone_rc_sys.R_er.value = 0.0087
            zone_rc_sys.R_gr.value = 0.1
            zone_rc_sys.R_ge.value = np.inf
            return zone_rc_sys

df = pd.read_csv("./rc_system_data/weather_data_2017_pandas.csv")

# Function which creates a CDCM weather system and return it.
def get_weather_sys(df):
    weather_sys = make_data_system(
        df[["Tout", "Qsg", "Qint"]],
        name="weather_sys",
        column_units=["degC", "Wh", "Wh"],
        column_desciptions=[
            "Outdoor air temperature",
            "Solar irradiance",
            "Internal heat gain"
        ]
    )
    return weather_sys

## Creating variables to pass while constructing RC system object

Q_int = Variable(
    name="Q_int",
    units="W",
    value=150,
    description="Sum of internal heat gain",
)
T_cor = Variable(
    name="T_cor",
    units="degC",
    value=23,
    description="Corridor temperature",
)
u_t = Variable(
    name="u_t", units="W", value=0.0, description="Input loads"
)

"We create a CDCM system consisiting of clock, weather system and RC system"
with System(name="zone_sys_det") as zone_sys_det:
    
    ## weather system ##
    weather_sys = get_weather_sys(df)
    
    ## clock system ##
    clock = make_clock(1800)
    
    ## We make the RC system of a deterministic zone next. ##
    det_zone_rc_sys = make_rc_of_cdcm(
                              clock.dt,
                              weather_sys,
                              T_cor,
                              Q_int,
                              u_t,
                              name='det_zone_rc_sys'
                    )