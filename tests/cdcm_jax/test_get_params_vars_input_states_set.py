"""Test sys_nodes_for_diffrax() for jax capabilities in cdcm

Author:
    Sreehari Manikkan
Date:
    02/27/2024
"""

import numpy as np
import pandas as pd
from duffing_oscillator import make_duff_osc_sys
from cdcm_utils.cdcm_jax import set_sys_nodes_for_diffrax
from cdcm_utils.cdcm_jax import get_params_vars_input_states_set
from cdcm import *

dt = 0.01
max_steps = 250*2
t_data = np.arange(0.,max_steps*dt,dt)
force_data = np.cos(t_data)
input_dict = {"force":force_data}

input_data_df = pd.DataFrame(input_dict)
input_data_df.head()
input_data = {
    "data":input_data_df,
    "name":"input_sys",
}
kwargs = {"input_data":input_data}
duff_osc_sys = make_duff_osc_sys(
    dt = dt,
    name="duff_osc_sys",
    **kwargs,
)

set_sys_nodes_for_diffrax(duff_osc_sys)
param_set, vars_set, input_set, states_set = get_params_vars_input_states_set(
     cdcm_sys=duff_osc_sys,
)
print("#####################################")
print("param_set obtained",[i.name for i in param_set])
print("cdcm_sys Parameters",[i.name for i in duff_osc_sys.parameters])
print("states_set obtained",[i.name for i in states_set])
print("cdcm_sys States",[i.name for i in duff_osc_sys.states])
print("vars_set obtained",[i.name for i in vars_set])
print("cdcm_sys Variables",[i.name for i in duff_osc_sys.nodes if type(i) is Variable])
print("input_set obtained",[i.name for i in input_set])
print("#####################################")
