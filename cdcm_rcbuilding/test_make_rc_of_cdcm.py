#!/usr/bin/env python
# coding: utf-8

# """
# test_make_rc_of_cdcm.py
# This python file tests the making of RC system corresponding
# to a YABML building.
# 
# Author(s):
#     Sreehari Manikkan
# Date:
#     06/29/2022
# """

# In[1]:


import h5py
import os

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from cdcm import *
from yabml import *

from rc_system import RCBuildingSystem
from rc_system import make_rc_of_cdcm
from single_zone_deterministic import single_zone_building


# In[2]:


import cdcm
print(cdcm.__file__)


# In[6]:


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


# In[7]:


# ---------- RC System of a deterministic zone-----------------#

zone = single_zone_building.zones[0]
neighbor = single_zone_building.neighbor[0]

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
                              zone,
                              neighbor,
                              clock,
                              weather_sys,
                              T_cor,
                              Q_int,
                              u_t,
                              name='det_zone_rc_sys'
                    )


# In[ ]:


print('------ R C values of the current zone -------')
print(f"""
C_room={det_zone_rc_sys.C_room.value},
C_env={zone_sys_det.det_zone_rc_sys.C_env.value},
C_genv={zone_sys_det.det_zone_rc_sys.C_genv.value},
R_rc={zone_sys_det.det_zone_rc_sys.R_rc.value},
R_oe={zone_sys_det.det_zone_rc_sys.R_oe.value},
R_er={zone_sys_det.det_zone_rc_sys.R_er.value},
R_gr={zone_sys_det.det_zone_rc_sys.R_gr.value},
R_ge={zone_sys_det.det_zone_rc_sys.R_ge.value}""")


# In[ ]:


print(zone_sys_det)


# In[ ]:


## ------ Simulating the system -----------##
max_steps = 1000
file_name = "test_make_rc_of_cdcm_det.h5"

if os.path.exists(file_name):
        os.remove(file_name)

test_saver_det = SimulationSaver(file_name,
                            zone_sys_det,
                            max_steps=max_steps
)

for i in range(max_steps):
    zone_sys_det.forward()
    test_saver_det.save()
    zone_sys_det.transition()


# In[ ]:


## ------- Visualizing the results -------- ##
T_room_sensor = (
    test_saver_det.file_handler[
        "/zone_sys_det/det_zone_rc_sys/T_room_sensor"
    ][:]
)
T_env = (
    test_saver_det.file_handler["/zone_sys_det/det_zone_rc_sys/T_env"][:]
)
T_genv = (
    test_saver_det.file_handler["/zone_sys_det/det_zone_rc_sys/T_genv"][:]
)
T_out = (
    test_saver_det.file_handler["/zone_sys_det/weather_sys/Tout"][:]
)

time = np.arange(max_steps) * 0.5/24
plt.plot(time, T_room_sensor, label='T_room_sensor')
plt.plot(time, T_env, label='T_env')
plt.plot(time, T_genv, label='T_genv')
plt.plot(time, T_out, label='T_out')
plt.ylabel('Temperature (C)')
plt.xlabel('Time (days)')
plt.title('Results for single zone deterministic building')
plt.legend()
plt.show()


# In[ ]:


# ---------- RC System of a random zone -----------------#
"""
We make the RC system of a non deterministic zone.
"""
# Setting up of file to save simulated results
file_name = "test_make_rc_of_cdcm_random.h5"

if os.path.exists(file_name):
    os.remove(file_name)

file = h5py.File(file_name, "w")

sample_size = 9
building_no = 1
max_steps = 500
test_saver_random = []

from single_zone_random import single_zone_building

for single_zone_building_sample in single_zone_building.sample(sample_size):
    z = single_zone_building_sample.zones[0]
    n = single_zone_building_sample.neighbor[0]
    
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
    with System(name="zone_sys_random"+str(building_no)) as zone_sys_random:

        ## weather system ##
        weather_sys = get_weather_sys(df)

        ## clock system ##
        clock = make_clock(1800)

        ## We make the RC system of a random zone next. ##
        make_rc_of_cdcm(
            z,
            n,
            zone_sys_random.clock.dt,
            zone_sys_random.weather_sys,
            T_cor,
            Q_int,
            u_t,
            name='zone_rc_sys'
        )
    
    group = f"building_{building_no}"
    file.create_group(group)
    test_saver_random.append(SimulationSaver(file[group],
                                zone_sys_random,
                                max_steps=max_steps
    )
                      )

    for i in range(max_steps):
        zone_sys_random.forward()
        test_saver_random[-1].save()
        zone_sys_random.transition()
    building_no += 1


# In[ ]:


# Code for plotting was taken from here
# https://stackoverflow.com/questions/17210646/python-subplot-within-a-loop-first-panel-appears-in-wrong-position

fig, axs = plt.subplots(3,3, figsize=(15,10), facecolor='w', edgecolor='k')
fig.subplots_adjust(hspace = .5, wspace=.001)

axs = axs.ravel()

for building_no in np.arange(9):
    group = f"building_{building_no+1}"
    system_name = "zone_sys_random"+str(building_no+1)
    T_room_sensor = (
        test_saver_random[building_no].group[system_name+"/zone_rc_sys/T_room_sensor"
        ][:]
    )
    T_env = (
        test_saver_random[building_no].group[system_name+"/zone_rc_sys/T_env"][:]
    )
    T_genv = (
        test_saver_random[building_no].group[system_name+"/zone_rc_sys/T_genv"][:]
    )
    T_out = (
        test_saver_random[building_no].group[system_name+"/weather_sys/Tout"][:]
    )

    time = np.arange(max_steps) * 0.5/24
    axs[building_no].plot(time, T_room_sensor, label='T_room_sensor')
    axs[building_no].plot(time, T_env, label='T_env')
    axs[building_no].plot(time, T_genv, label='T_genv')
    #axs[building_no].plot(time, T_out, label='T_out')
    axs[building_no].set_ylabel('Temperature (C)')
    axs[building_no].set_xlabel('Time (days)')
    axs[building_no].set_title(f'Results for single zone random building{building_no+1}')
fig.tight_layout()
plt.legend()
plt.show()


# In[ ]:




