#~ovn!
"""Some common utilities through the package

Author:
    Murali Krishnan R
    
Date:
    03.05.2023
    
"""


__all__ = ["make_pyvis_graph"]


import pyvis.network as nt

from cdcm import *
from cdcm_abstractions import *


def get_node_properties(node: Node):
    """Node properties"""
    node_type = str(type(node)).split('.')[-1][:-2]

    if isinstance(node, HealthStatus):
        return {"type": "Status", "color": "cyan", 'shape': 'dot'} 
    elif isinstance(node, State):
        return {"type": "State", "color": "green", 'shape': 'dot'}
    elif isinstance(node, Parameter):
        return {"type": "Parameter", "shape": "star", "color": "gray"}
    elif isinstance(node, Variable):
        return {"type": 'Variable', "color": "brown", 'shape': 'triangleDown'}
    elif isinstance(node, Transition):
        return {"type": 'Transition', "color": "green", "shape": 'triangle'}
    elif isinstance(node, Function):
        return {"type": 'Function', "color": "blue", 'shape': 'triangle'}
    else:
        raise TypeError(f"Unknown node type: {node_type}")

def make_pyvis_graph(sys: System, html_name: str, buttons: bool=True, **kwargs):
    """Build a `pyvis` graph instance of the system"""

    g = nt.Network('1500px', '75%', directed=True)
    for n in sys.nodes:
        node_absname = n.absname
        node_properties = get_node_properties(n)
        g.add_node(
            node_absname, 
            label=n.name,
            color=node_properties.get('color'), 
            shape=node_properties.get('shape', 'dot'))
        for c in n.children:
            child_properties = get_node_properties(c)
            child_absname = c.absname
            g.add_node(
                child_absname, 
                label=c.name,
                color=child_properties.get('color'), 
                shape=child_properties.get('shape', 'dot')
                )
            g.add_edge(node_absname, child_absname)
    if buttons:
        g.show_buttons()
    g.set_edge_smooth('dynamic')
    g.show(html_name)
    return g

