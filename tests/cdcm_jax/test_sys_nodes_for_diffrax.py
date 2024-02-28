"""Test sys_nodes_for_diffrax() for jax capabilities in cdcm

Author:
    Sreehari Manikkan
Date:
    02/27/2024
"""

from simple_harmonic_system import make_dsh_sys
from cdcm_utils.cdcm_jax import get_sys_nodes_for_diffrax

sh_sys = make_dsh_sys(
    dt = 0.01,
    name="sh_sys",
    zeta_val=0.032,
)

sh_sys.sys_nodes_for_diffrax = set()
sh_sys.sys_nodes_for_diffrax = get_sys_nodes_for_diffrax(
    sh_sys, sh_sys.sys_nodes_for_diffrax
)
print("sh_sys.nodes (cached property)")
print([i.name for i in sh_sys.nodes])
print("sh_sys.sys_nodes_for_diffrax (non cached property)")
print([i.name for i in sh_sys.sys_nodes_for_diffrax])
