"""
A python function which creates an attribute `sys_dag_for_diffrax` for 
a given CDCM System object

Author:
    Sreehari Manikkan

Date:
    02/25/2024
"""

import networkx as nx
from cdcm import *



def get_sys_dag_for_diffrax(sys):
    """
    A python function which creates an attribute `sys_dag_for_diffrax` for 
    a given CDCM System object. This DAG doesnot contain string nodes
    representing next time step State node. This is the difference between
    this DAG and `sys.dag`.
    Part of code is adapted from
    cdcm_execution repo System class
    defnition.

    Arguments:
        sys: A CDCM System object
    
    Return:
        None
    """

    sys.sys_dag_for_diffrax = nx.DiGraph()
    g = sys.sys_dag_for_diffrax
    for n in sys.sys_nodes_for_diffrax:
        g.add_node(n)
        if isinstance(n, State):
            for c in n.children:
                if n in c.children:
                    continue
                g.add_edge(n, c)
        else:
            for c in n.children:
                g.add_edge(n, c)
