"""python file containing functions for setting derivatives
in cdcm

Author:
    Sreehari Manikkan
Date:
    08/22/2023
"""
__all__ = ["set_derivative",
           "update_loss_grad",
           "get_derivative_update_seq",
           ]

from cdcm import *
from jax import jacfwd
import jax.numpy as jnp
import networkx as nx
import math


def get_sys_nodes_for_grad(sys, sys_nodes_for_grad):
    """
    part of code is adapted from
    cdcm_execution repo System class
    defnition
    """

    for node in sys.direct_nodes:
        if node not in sys_nodes_for_grad:
            if isinstance(node, System):
                sys_nodes_for_grad.update(
                    get_sys_nodes_for_grad(node, sys_nodes_for_grad)
                )
            else:
                sys_nodes_for_grad.add(node)
    return sys_nodes_for_grad


def update_sys_dag_for_grad(sys):
    """part of code is adapted from
    cdcm_execution repo System class
    defnition
    """

    sys.sys_dag_for_grad = nx.DiGraph()
    g = sys.sys_dag_for_grad
    for n in sys.sys_nodes_for_grad:
        g.add_node(n)
        if isinstance(n, State):
            for c in n.children:
                if n in c.children:
                    continue
                g.add_edge(n, c)
        else:
            for c in n.children:
                g.add_edge(n, c)


def edge_jac_fn(y_fn,x):
    posn = y_fn.parents.index(x)
    def wrap_fn(*args):
        args=[*args]
        f1 = lambda q1: y_fn.func(*args[:posn],q1,*args[posn+1:])
        return jacfwd(f1)(args[posn])
    return wrap_fn


def get_edge_gradient(
        x,
        y_fn,
        sys,
        sys_nodes_for_grad,
        grad_edge_name,
    ):
    """
    get the gradient of edge going from x to y with the mapping given by
    y_fn.
    """
    
    # setting gradients along the edges of path
    if grad_edge_name not in [i.name for i in sys_nodes_for_grad]:
        with sys:
            dydx_edge = Variable(
                name=grad_edge_name,
                value=0.,
                units=None,
            )
            calc_dydx_edge = Function(
                name=f"calc_{dydx_edge.name}",
                func=edge_jac_fn(y_fn,x),
                parents=y_fn.parents,
                children=dydx_edge
            )
        sys_nodes_for_grad.add(dydx_edge)
        sys_nodes_for_grad.add(calc_dydx_edge)
    else:
        dydx_edge = [
            n for n in sys_nodes_for_grad if n.name == grad_edge_name
        ][0]
    return dydx_edge


def get_simple_path_gradients(
        path,
        sys_nodes_for_grad,
        sys,
    ):
    grad_path_edges = []
    # setting the gradient along the path
    for idx in range(len(path)-2,-1,-2):
        dydx_edge = get_edge_gradient(
            x=path[idx-1],
            y_fn=path[idx],
            sys=sys,
            sys_nodes_for_grad=sys_nodes_for_grad,
            grad_edge_name=f"pd{path[idx+1].absname}d{path[idx-1].absname}",
        )
        grad_path_edges.append(dydx_edge)    
    return grad_path_edges


def get_dir_indir_path_gradients(
        dir_path,
        indir_path,
        sys_nodes_for_grad,
        sys,
    ):
    grad_dir_path_edges = []
    grad_indir_path_edges = []
    for idx in range(len(dir_path)-2,-1,-2):
        dydx_edge = get_edge_gradient(
            x=dir_path[idx-1],
            y_fn=dir_path[idx],
            sys=sys,
            sys_nodes_for_grad=sys_nodes_for_grad,
            grad_edge_name=f"pd{dir_path[idx+1].name}d{dir_path[idx-1].name}",
        )
        grad_dir_path_edges.append(dydx_edge)

    for idx in range(len(indir_path)-2,-1,-2):
        grad_edge_name=f"pd{indir_path[idx+1].name}d{indir_path[idx-1].name}"
        dydx_edge = get_edge_gradient(
            x=indir_path[idx-1],
            y_fn=indir_path[idx],
            sys=sys,
            sys_nodes_for_grad=sys_nodes_for_grad,
            grad_edge_name=grad_edge_name,
        )
        grad_indir_path_edges.append(dydx_edge)
    return grad_dir_path_edges, grad_indir_path_edges


def edi_is_oned(edi,edj):
    if len(edj.shape)==1:
        assert edi.shape[0]==edj.shape[0]
        return edi@edj.T
    else: #edj is 2d
        if edj.shape[0] == edi.shape[0]:
            return edj.T@edi
        elif edj.shape[1] == edi.shape[0]:
            return edj@edi
        else:
            raise Exception(
                f"""Dimensions of edge Jacobian should match
                for matrix multiplication. Detected edge
                dimensions are {edi.shape} and {edj.shape}
                """
            )


def edge_jac_prod(ed1,ed2):
    if not hasattr(ed1, "__len__"):
        # ed1 is scalar
        return ed1*ed2
    elif not hasattr(ed2, "__len__"):
        # ed2 is scalar, ed1 not
        return ed1*ed2
    elif len(ed1.shape)>2 or len(ed2.shape)>2:
        raise Exception(
            f"""Jacobian matrix of dimension upto 2 is allowed
                for edge derivative. detected shapes are {ed1.shape},
                {ed2.shape}"""
        )
    elif len(ed1.shape)==0:
        return ed1*ed2
    elif len(ed2.shape)==0:
        return ed1*ed2
    elif len(ed1.shape)==1:
        return edi_is_oned(ed1,ed2)
    elif len(ed2.shape)==1:
        # ed1 should have len 2 here
        return edi_is_oned(ed2,ed1)
    else:
        # both ed1 and ed 2 have len 2 now
        if ed1.shape[1]==ed2.shape[0]:
            return ed1@ed2
        elif ed2.shape[1]==ed1.shape[0]:
            return ed2@ed1
        else:
            raise Exception(
                f"""Dimensions of edge Jacobian should match
                for matrix multiplication. Detected edge
                dimensions are {ed1.shape} and {ed2.shape}
                """
            )


def path_jac_fn(*args):
    eds = [*args]
    res = 1.
    for edi in eds:
        res = edge_jac_prod(res,edi)
    return res


def get_simple_path_grad_nodes(
        paths,
        sys,
        grad_paths,
        grad_name,
):  
    
    # getting gradients from simple paths
    for path_no, path in enumerate(paths):
        grad_path_name = grad_name+f"{path_no}"
        # grad_path_name does not guarantee uniqueness w.r.t 
        # path. hence dydx_path are not added to the 
        # sys_nodes_for_grad.
        grad_path_edges = get_simple_path_gradients(
                        path=path,
                        sys_nodes_for_grad=sys.sys_nodes_for_grad,
                        sys=sys,
                    )
            
        if len(grad_path_edges) == 1:
            dydx_path = grad_path_edges[0]
        else:
            with sys:
                dydx_path = Variable(
                    name=grad_path_name,
                    value=0.,
                    units=None,
                    track=False
                )
                calc_dydx_path = Function(
                    name=f"calc_{dydx_path.name}",
                    func = path_jac_fn,
                    parents=grad_path_edges,
                    children=dydx_path
                )
                sys.sys_nodes_for_grad.add(dydx_path)
                sys.sys_nodes_for_grad.add(calc_dydx_path)
        
        grad_paths.append(dydx_path)
    
    return grad_paths,path_no


def get_dir_indir_path_grad_nodes(
        dir_paths,
        indir_paths,
        sys,
        path_no,
        grad_paths,
        grad_name,
):
    # getting gradients from dir_indir paths
    for idx, dp in enumerate(dir_paths):
        grad_path_name = grad_name+f"{path_no+idx+1}"
        grad_dir_path_edges, grad_indir_path_edges = (
            get_dir_indir_path_gradients(
                dir_path=dp,
                indir_path=indir_paths[idx],
                sys_nodes_for_grad=sys.sys_nodes_for_grad,
                sys=sys,
            )
        )
        with sys:
            dydx_dir_path = Variable(
                name=grad_path_name+"dir",
                value=0.,
                units=None,
                track=False
            )
            dydx_indir_path = Variable(
                name=grad_path_name+"indir",
                value=0.,
                units=None,
                track=False
            )
            calc_dydx_dir_path = Function(
                name=f"calc_{dydx_dir_path.name}",
                func = lambda *args: math.prod([*args]),
                parents=grad_dir_path_edges,
                children=dydx_dir_path
            )
            calc_dydx_indir_path = Function(
                name=f"calc_{dydx_indir_path.name}",
                func = rec_prod_func,
                parents=grad_indir_path_edges,
                children=dydx_indir_path
            )
            dydx_path = Variable(
                name=grad_path_name,
                value=0.,
                units=None,
                track=False,
            )
            calc_dydx_path = Function(
                name=f"calc_{dydx_path.name}",
                func = lambda *args: math.prod([*args]),
                parents=[dydx_dir_path,dydx_indir_path],
                children=dydx_path
            )
        grad_paths.append(dydx_path)
    return grad_paths


class GradientPaths:
     
    def __init__(self,
                 y,
                 x, 
                 sys_dag_for_grad,
        ):
        self.dir_paths = []
        self.indir_paths = []
        self.x, self.y = x, y
        self.sys_dag_for_grad = sys_dag_for_grad
        self.track_parents_set = set()
        self.termination_set= set()

        # simple paths from x to y. These are the paths of direct
        # influence from x to y.
        self.paths = [
            i for i in nx.all_simple_paths(
                                    self.sys_dag_for_grad,
                                    self.x, 
                                    self.y
                                    )
        ]
    
    # no. of dir_paths and indir_paths are same 
    # as a dir_path and indir_path form a path apart 
    # from simple paths
    def fetch_dir_indir_paths(self):
        for path in self.paths:
            for idx in range(len(path)-1,-2,-2):
                p = path[idx]
                self.update_dir_indir_paths(p=p)

    def track_parents(self, p, p_indir_paths):
        if p==self.x or p in self.track_parents_set: #if True stop track
            return False
        elif len(p_indir_paths)>0: # if True stop Track
            self.track_parents_set.add(p)
            return False
        elif len(p.parents)>0:
            self.track_parents_set.add(p)
            return True
        else:
            self.track_parents_set.add(p)
            return False

    def update_dir_indir_paths(self,p):
        p_indir_paths = [
            i for i in nx.all_simple_paths(self.sys_dag_for_grad, p, self.x)
        ]
        if self.track_parents(
            p=p,
            p_indir_paths=p_indir_paths,
        ):
            p_fn = p.parents[0]
            for p1 in p_fn.parents:
                self.update_dir_indir_paths(p1)

        else:
            if p in self.termination_set:
                pass
            elif len(p_indir_paths)>0:
                p_dir_paths = [
                    i for i in nx.all_simple_paths(
                    self.sys_dag_for_grad, p, self.y)
                ]
                for ind_pth in p_indir_paths:
                    for d_pth in p_dir_paths:
                        if self.x in d_pth:
                            continue
                        self.indir_paths.append(ind_pth)
                        self.dir_paths.append(d_pth)
                self.termination_set.add(p)


def total_derv_func(*args):
    args=[*args]

    if not hasattr(args[0],"shape"):
        # args[0] is scalar float/int object
        res = 0.
        for i in args:
            if hasattr(i, "shape"):
                assert len(i.shape)==0 or i.shape==(1,) or i.shape==(1,1)
            res += i
    elif len(args[0].shape)==0 or args[0].shape==(1,) or args[0].shape==(1,1):
        res = jnp.zeros_like(args[0])
        for i in args:
            if hasattr(i, "shape"):
                assert len(i.shape)==0 or i.shape==(1,) or i.shape==(1,1)
            res += i
    else:
        res = jnp.zeros_like(args[0])
        for i in args:
            if not res.shape==i.shape:
                raise Exception(f"""
                path jacobians should have same shape. detected shapes 
                {res.shape},{i.shape}
                """)
            res += i
    return res


def rec_prod_func(*args):
    temp = [1/i for i in [*args]]
    return math.prod(temp)


def print_dag_edges(dag):
    for i in dag.edges:
        if isinstance(i[0],str):
            if isinstance(i[1],str):
                print(f"{i[0], i[1]}")
            else:
                print(f"{i[0], i[1].name}")
        elif isinstance(i[1],str):
            print(f"{i[0].name, i[1]}")
        else:
            print(f"{i[0].name, i[1].name}")


def update_loss_grad(update_seq):
    for n in update_seq:
        n.forward()


def get_derivative_update_seq(sys, x, grad_name):
    update_sys_dag_for_grad(sys)
    x_to_dydx_paths = [
        i for i in nx.all_simple_paths(
                            sys.sys_dag_for_grad,
                            x, 
                            getattr(sys,grad_name)
                            )
    ]
    paths = x_to_dydx_paths
    update_seq = []
    update_seq.append(paths[0][-2])
    max_path_len = max([len(p) for p in paths])
    for i in range(max_path_len-2,-1, -2):
        for idx, p in enumerate(paths):
            if i<=len(p)-4:
                if p[i] not in update_seq:
                    update_seq.append(p[i])
    update_seq.reverse()
    return update_seq


def set_derivative(sys,y,x,grad_name,derivative_update_seq=False):

    """
    sets the derivative of cdcm node y w.r.t cdcm node x as a<br>
    cdcm Variable node to the System 'sys'. This Variable node is
    accessible with the 'grad_name' argument passed.
    Arguments:
        sys: CDCM system to which the gradient node should be added
        y: CDCM node of type Variable or State
        x: CDCM node of type Variable or Parameter or State.
        grad_name: The name with which derivative node can be accessed
                   from sys. Note the 'name' attribute of CDCM node
                   representing the total derivative need not be necessary
                   this one.
        derivative_update_seq: If True, this will return a list of CDCM Functions
            to be evaluated in order to evaluate the value of derivative 
            of y w.r.t x for a given value of x. Useful for Calibration
            purposes.
    Return: derivative_update_seq if update_seq==True else None.

    """

    
    if not hasattr(sys, 'sys_nodes_for_grad'):
        sys.sys_nodes_for_grad = set()
    sys.sys_nodes_for_grad =  get_sys_nodes_for_grad(
        sys, sys.sys_nodes_for_grad
    )
    update_sys_dag_for_grad(sys)
    
    if hasattr(sys, grad_name):
        if (
            getattr(sys, grad_name).name in 
            [i.name for i in sys.sys_nodes_for_grad]
        ):
            print(f"{grad_name} already set in the graph")
    else:
        if not isinstance(y, (Variable, State)):
            raise Exception("Derivative of Variable or State is set")
        else: 
            grad_paths_obj = GradientPaths(
                y=y,
                x=x, 
                sys_dag_for_grad=sys.sys_dag_for_grad,
            )
            paths = grad_paths_obj.paths
            grad_paths_obj.fetch_dir_indir_paths()
            dir_paths = grad_paths_obj.dir_paths
            indir_paths = grad_paths_obj.indir_paths

            assert len(indir_paths)==len(dir_paths)
            if len(paths)==0:
                raise Exception(
                    f"""no simple paths of dependency found
                    between nodes {x.name} and {y.name}"""
                    )
            if len(paths)==1 and len(indir_paths)==0:
                grad_path_edges = get_simple_path_gradients(
                        path=paths[0],
                        sys_nodes_for_grad=sys.sys_nodes_for_grad,
                        sys=sys,
                    )

                if len(grad_path_edges) == 1:
                    setattr(sys, grad_name, grad_path_edges[0])
                else:
                    with sys:
                        dydx = Variable(
                            name=grad_name,
                            value=0.,
                            units=None,
                            track=True,
                        )
                        calc_dydx = Function(
                            name=f"calc_{dydx.name}",
                            func=path_jac_fn,
                            parents=grad_path_edges,
                            children=dydx,
                        )
                    sys.sys_nodes_for_grad.add(dydx)
                    sys.sys_nodes_for_grad.add(calc_dydx)

            else:
                if len(indir_paths)>0:
                    raise Exception(
                        f"""
                    Looks like {x.name} is an intermediate variable for
                    setting the derivative of {y.name} w.r.t {x.name}.
                    Derivative w.r.t intermediate variable is not currently
                    supported."""
                    )
                else:
                    grad_paths, path_no = (
                    get_simple_path_grad_nodes(
                                    paths=paths,
                                    sys=sys,
                                    grad_paths=[],
                                    grad_name=grad_name,
                    )
                    )
                    with sys:
                        dydx = Variable(
                            name=grad_name,
                            value=0.,
                            units=None,
                            track=True,
                        )
                        calc_dydx = Function(
                            name=f"calc_{dydx.name}",
                            func=total_derv_func,
                            parents=grad_paths,
                            children=dydx,
                        )
                    sys.sys_nodes_for_grad.add(dydx)
                    sys.sys_nodes_for_grad.add(calc_dydx)
            if derivative_update_seq:
                return get_derivative_update_seq(sys, x, grad_name)