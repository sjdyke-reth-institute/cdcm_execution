"""Test sys_nodes_for_diffrax() for jax capabilities in cdcm

Author:
    Sreehari Manikkan
Date:
    02/27/2024
"""

from simple_harmonic_system import make_dsh_sys
from cdcm_utils.cdcm_jax import get_sys_nodes_for_diffrax,\
    get_sys_dag_for_diffrax
from cdcm_utils.cdcm_jax import get_params_vars_input_states_set
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
print("#####################################")
print("param_set obtained",[i.name for i in param_set])
print("cdcm_sys Parameters",[i.name for i in sh_sys.parameters])
print("vars_set obtained",[i.name for i in vars_set])
print("states_set obtained",[i.name for i in states_set])
print("cdcm_sys States",[i.name for i in sh_sys.states])
print("cdcm_sys Variables",[i.name for i in sh_sys.nodes if type(i) is Variable])
print("""Variable y1 and y2 are children of the states
      and they do not come in the subgraph""")
print("input_set obtained",[i.name for i in input_set],'(no input to this system)')
print("#####################################")
