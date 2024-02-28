"""Test sys_nodes_for_diffrax() for jax capabilities in cdcm

Author:
    Sreehari Manikkan
Date:
    02/27/2024
"""

from simple_harmonic_system import make_dsh_sys
from cdcm_utils.cdcm_jax import get_sys_nodes_for_diffrax, get_sys_dag_for_diffrax

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
print("#####################################")
print("\n sh_sys.dag")
temp = []
for i in sh_sys.dag.nodes:
     temp.append(i) if type(i) is str else temp.append(i.name)
print(temp)
print("\n sh_sys.sys_dag_for_diffrax (no future state nodes)")
print([i.name for i in sh_sys.sys_dag_for_diffrax.nodes])
print("#####################################")
