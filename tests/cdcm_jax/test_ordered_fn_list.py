"""Test sys_nodes_for_diffrax() for jax capabilities in cdcm

Author:
    Sreehari Manikkan
Date:
    02/27/2024
"""

from simple_harmonic_system import make_dsh_sys
from cdcm_utils.cdcm_jax import get_sys_nodes_for_diffrax
from cdcm_utils.cdcm_jax import get_sys_dag_for_diffrax
from cdcm_utils.cdcm_jax import get_params_vars_input_states_set
from cdcm_utils.cdcm_jax import get_ordered_fn_list
from cdcm import *

sh_sys = make_dsh_sys(
    dt = 0.01,
    name="sh_sys",
    zeta_val=0.032,
)

sh_sys.sys_nodes_for_diffrax = set()
sh_sys.sys_nodes_for_diffrax = get_sys_nodes_for_diffrax(
    sh_sys, sh_sys.sys_nodes_for_diffrax
)
get_sys_dag_for_diffrax(sh_sys)
param_set, vars_set, input_set, states_set = get_params_vars_input_states_set(
     cdcm_sys=sh_sys,states=sh_sys.states,
)
ordered_fn_list = get_ordered_fn_list(sh_sys,vars_set,states_set)
print("#####################################")
print("ordered_fn_list",[i.name for i in ordered_fn_list])
print("Evaluation order of the cdcm system",
      [i.name for i in sh_sys.evaluation_order])
print("#####################################")
