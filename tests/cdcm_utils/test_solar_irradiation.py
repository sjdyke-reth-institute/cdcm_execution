# ~ovn!
"""Test the solar irradiation model

Author:
    Sreehari Manikkan
    R Murali Krishnan
    
Date:
    01.30.2023
    05.08.2023
    
"""

from cdcm import *
from cdcm_utils.solar_irradiation import *

import numpy as np
import matplotlib.pyplot as plt


start_time = "2022-01-10%2000:00"
end_times = ["2022-03-10%2000:00", "2023-01-10%2000:00"]
step_size = "1h"
phis = [0.7, 45.6, 88.5]
lamdas = [0.5, 88.5, -88.5]

data = get_insolation_ephemeris(
    start_time=start_time,
    end_time=end_times[1],
    step_size=step_size,
    phi=phis[0],
    lamda=lamdas[0],
    alpha=0.0,
    beta=0.0
)

print(data.columns.values)
print(data.columns.value_counts())

with System(name="sys") as sys:

    clock = make_clock(dt=1.0, units="hr")

    ExtEnv = DataSystem(
        name="ext_env",
        data=data['Q'].to_numpy(),
        columns=["Q"],
        column_units=["W/m^2"],
        column_descriptions=["Solar irradiation"]
    )
    ExtEnv.forward()

print(ExtEnv)

print("~ovn!!")