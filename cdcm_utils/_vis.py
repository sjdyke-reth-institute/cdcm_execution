#~ovn!
"""Data visualization utilities

Author:
    R Murali Krishnan
    
Date:
    10.02.2023
    
"""


__all__ = ["make_pyvis_graph"]


from cdcm import System
import pyvis.network as nt
import seaborn as sns
import itertools as it


node_shapes = {
    "Variable": {"shape": "dot"},
    "State": {"shape": "dot"},
    "Parameter":{"shape": "dot"},
    "Function": {"shape": "triangle"},
    "Transition": {"shape": "triangle"},
    "Test": {"shape": "ellipse"},
    "HealthState": {"shape": "square"},
}

def find_closest_key(type_name):
    """Find the key from node_shapes matching the type_name"""
    for key, val in node_shapes.items():
        if key in type_name:
            return {key: val}


def make_pyvis_graph(sys: System) -> nt.Network:
    """Make a `pyviz` graph instance of the system"""

    g = nt.Network('1500px', '75%', directed=True)

    cmap = it.cycle(sns.color_palette('pastel').as_hex())
    colors = {}
    for n in sys.nodes:
        owner_name = n.owner.absname
        ntype = type(n).__name__
        if owner_name not in colors:
            colors[owner_name] = next(cmap)

        g.add_node(n.absname, label=n.absname, color=colors[owner_name], **find_closest_key(ntype))
        for c in n.children:
            ctype = type(c).__name__
            g.add_node(c.absname, label=c.absname, color=colors[owner_name], **find_closest_key(ctype))
            g.add_edge(n.absname, c.absname)
    g.show_buttons()
    g.set_edge_smooth('dynamic')
    return g

