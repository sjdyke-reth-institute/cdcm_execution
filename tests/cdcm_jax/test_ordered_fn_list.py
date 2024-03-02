"""Test sys_nodes_for_diffrax() for jax capabilities in cdcm

Author:
    Sreehari Manikkan
Date:
    02/27/2024
"""

import numpy as np
import pandas as pd
from duffing_oscillator import make_duff_osc_sys
from cdcm_utils.cdcm_jax import get_sys_nodes_for_diffrax
from cdcm_utils.cdcm_jax import  get_sys_dag_for_diffrax
from cdcm_utils.cdcm_jax import get_params_vars_input_states_set
from cdcm_utils.cdcm_jax import get_ordered_fn_list
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

duff_osc_sys.sys_nodes_for_diffrax = set()
duff_osc_sys.sys_nodes_for_diffrax = get_sys_nodes_for_diffrax(
    duff_osc_sys, duff_osc_sys.sys_nodes_for_diffrax
)
get_sys_dag_for_diffrax(duff_osc_sys)
param_set, vars_set, input_set, states_set = get_params_vars_input_states_set(
     cdcm_sys=duff_osc_sys,states=duff_osc_sys.states,
)
ordered_fn_list = get_ordered_fn_list(duff_osc_sys,vars_set,states_set)
print("#####################################")
print("ordered_fn_list",[i.name for i in ordered_fn_list])
print("Evaluation order of the cdcm system",
      [i.name for i in duff_osc_sys.evaluation_order])
print("#####################################")
