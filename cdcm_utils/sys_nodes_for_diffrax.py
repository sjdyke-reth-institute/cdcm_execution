"""
A python function which returns the set of nodes of a given cdcm system

Author:
    Sreehari Manikkan

Date:
    02/25/2024
"""

from cdcm import *



def get_sys_nodes_for_diffrax(sys, sys_nodes_for_diffrax):
    """
    A python function which returns 
    the set of nodes of a given cdcm system.
    This is not a cached property unlike `sys.nodes`.
    Part of code is adapted from
    cdcm_execution repo System class
    defnition.

    Arguments:
        sys: A CDCM System object
        sys_nodes_for_diffrax: A set which is empty or already consisits of
        nodes from sys.
    
    Return:
        sys_nodes_for_diffrax: Set which consists of nodes of sys.
    """

    for node in sys.direct_nodes:
        if node not in  sys_nodes_for_diffrax:
            if isinstance(node, System):
                 sys_nodes_for_diffrax.update(
                    get_sys_nodes_for_diffrax(node, sys_nodes_for_diffrax)
                )
            else:
                 sys_nodes_for_diffrax.add(node)
    return  sys_nodes_for_diffrax
    