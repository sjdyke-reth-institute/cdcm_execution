"""
This python file contains various utilites for creating a vector field 
corresponding to a CDCM System which can be passed to diffrax.

Author:
    Sreehari Manikkan

Date:
    02/25/2024
"""

import networkx as nx
import jax
from jax import jit, lax
import jax.numpy as jnp
import diffrax as dfx
from typing import Set, List, Dict

from cdcm import *

__all__ = ["get_sys_nodes_for_diffrax",
           "get_sys_dag_for_diffrax",
           "get_params_vars_input_states_set",
           "get_ordered_fn_list",
           "get_fn_args_res_info",
           "interpolate_Texts",
           "get_vector_field",

           ]


def get_sys_nodes_for_diffrax(
        sys: System,
        sys_nodes_for_diffrax: Set
    ):
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


def get_sys_dag_for_diffrax(sys: System):
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


def get_params_vars_input_states_set(
        cdcm_sys: System,
        states: List,
    ):
    """This function fetches the information of the subgraph represented
    by 'states' from the CDCM System DAG. The function gets the set of
    Parameter, Variable with Forward functions, Varibale part of
    DataSystem and State (states passed and additional states required if any).
    These sets represent the subgraph of
    CDCM System corresponding to the `states` passed.
    Subgraph is fetched by collecting all the simple paths from all parameters
    to the 'states' of CDCM System.

    Note: The `states_set` may contain additional states which are part
    of the subgraph.

    Arguments:
        cdcm_sys: CDCM System Object
        states: List of State nodes of cdcm_sys
    
    Return:
        param_set: Set of Parameter nodes
        vars_set: Set of Variable nodes with Forward functions
        input_set: Set of Varibale nodes part of DataSystem
        states_set: Set of State nodes
    """
    params_set = set()
    vars_set = set()
    input_set = set()
    states_set = set()

    if not hasattr(cdcm_sys, 'sys_nodes_for_diffrax'):
        cdcm_sys.sys_nodes_for_diffrax = set()
    cdcm_sys.sys_nodes_for_diffrax =  get_sys_nodes_for_diffrax(
        cdcm_sys, cdcm_sys.sys_nodes_for_diffrax
    )
    get_sys_dag_for_diffrax(cdcm_sys)

    for s in states:
        for p in cdcm_sys.parameters:
            simple_paths = [i for i in
                   nx.all_simple_paths(
                    cdcm_sys.sys_dag_for_diffrax,
                    p,
                    s,
                    )]
            if len(simple_paths)>0:
                params_set.add(p)
            for path in simple_paths:
                all_vars = [i for i in path if type(i) is Variable]
                input_vars = [i for i in all_vars if i.parents[0].name in ["read"]]
                vars = [i for i in all_vars if i.parents[0].name not in ["read"]]
                vars_set.update(vars)
                input_set.update(input_vars)
                states_set.update([i for i in path if type(i) is State])
    
    data_node = [i for i in params_set if i.name == "data_node"][0]
    params_set.remove(data_node)
    row_node = [i for i in states_set if i.name == "row"]
    t_node = [i for i in states_set if i.name == "t"]
    if row_node: states_set.remove(row_node[0])
    if t_node: states_set.remove(t_node[0])
    return params_set, vars_set, input_set, states_set


def get_ordered_fn_list(
        cdcm_sys: System,
        vars_set: Set,
        states_set: Set,
    ):
    """
    This function obtains the topological order of
    Forward and Transition functions of a subgraph of CDCM System object
    `cdcm_sys` consisting of Variables specified by `vars_set` and States
    specified by `states_set`.

    Arguments:
        cdcm_sys: CDCM System Object.
        vars_set: Set of Variable nodes with Forward functions
        states_set: Set of State nodes with Transition functions.
    Return:
        ordered_fn_list: A List consisting of the Forward and 
            Transition python functions sorted in topological order.
    """
    eval_order = cdcm_sys.evaluation_order
    ordered_fn_list = [
        i.parents[0] for i in list(vars_set)+list(states_set)
    ]
    ordered_fn_list = list(set(ordered_fn_list))
    order_index = [
        eval_order.index(fn) for fn in  ordered_fn_list
    ]
    ordered_fn_list = [
        f for _,f in sorted(zip(order_index,ordered_fn_list),
        key = lambda of:of[0])
    ]
    return ordered_fn_list


def get_fn_args_res_info(
    params_set: Set,
    input_set: Set,
    vars_set: Set,
    states_set: Set,
    ordered_fn_list: List,
):
    """
    This function obtains the information of Arguments (input) and Return
    (output) of the functions in `ordered_fn_list`.

    Arguments:
        param_set: Set of Parameter nodes
        input_set: Set of Varibale nodes part of DataSystem
        vars_set: Set of Variable nodes with Forward functions
        states_set: Set of State nodes with Transition functions.
        ordered_fn_list: A List consisting of the Forward and 
            Transition python functions sorted in topological order.
    Return:
        dict_of_fn_args_info_dict: 
            A Python dictionary consisting of 
            seperate python dictionary for each function in `ordered_fn_list`.
            key of this dictionary is the name of the function in the
            ordered list and 
            value is a seperate python dictionary of the function.
            The syntax of the i^th separate dictionary corresponding to 
            the i^th function in `ordered_fn_list` is:
            {
                0(index of the 1st argument): {"parent_type": local_idx}
                ...
                j(index of the j^th argument): {"parent_type": local_idx},
                ...
                len(arguments of i^th function)-1: {"parent_type": local_idx},
                
            }
            "parent_type" can be any of ["params", "input", "vars", "states"]
            local_idx: This is the location inside param_set or input_set or
            vars_set or states_set (depending on "parent_type") where the
            parent of the function is located.


        dict_of_fn_res_info_dict:
            A Python dictionary consisting of 
            seperate python dictionary for each function in `ordered_fn_list`.
            key of this dictionary is the name of the function in the
            ordered list and 
            value is a seperate python dictionary of the function.
            The syntax of the separate i^th dictionary corresponding to 
            the i^th function in `ordered_fn_list` is:
            {
                0(index of the 1st ouput): {"child_type": local_idx}
                ...
                j(index of the j^th output): {"child_type": local_idx},
                ...
                len(output of i^th function)-1: {"child_type": local_idx},
                
            }
            "child_type" can be any of ["vars", "next_state"]
            local_idx: This is the location inside vars_set or states_set 
            (depending on "parent_type") where the child of the function
            is located.
    """
    
    param_input_var_state_set_dict = {
        "params":list(params_set),
        "input":list(input_set),
        "vars":list(vars_set), 
        "states":list(states_set),
    }

    dict_of_fn_args_info_dict = {}
    dict_of_fn_res_info_dict = {}
    for fn in ordered_fn_list:
        fn_args_info_dict = {}
        fn_res_info_dict = {}
        
        for idx, parent in enumerate(fn.parents):
            if parent in params_set:
                parent_type = "params" 
            elif parent in input_set:
                parent_type = "input"
            elif parent in vars_set:
                parent_type = "vars"
            elif parent in states_set:
                parent_type = "states"
            local_idx = param_input_var_state_set_dict[parent_type].index(parent)
            fn_args_info_dict[idx] = {
                "parent_type":parent_type,"local_idx":local_idx}
        
        for idx, child in enumerate(fn.children):
            if child in vars_set:
                child_type = "vars"
                local_idx = param_input_var_state_set_dict[child_type].index(child)
            elif child in states_set:
                child_type = "next_state"
                local_idx = param_input_var_state_set_dict["states"].index(child)
            fn_res_info_dict[idx] = {
                "child_type":child_type,"local_idx":local_idx}
            
        dict_of_fn_args_info_dict[fn.name] = fn_args_info_dict
        dict_of_fn_res_info_dict[fn.name] = fn_res_info_dict

    return dict_of_fn_args_info_dict, dict_of_fn_res_info_dict


def interpolate_Texts(
        t_data,
        input_data,
    ):
    """
    This creates a LinearInterpolation object of Diffrax corresponding to
    the time series signal passed.
    For more details please refer: 
    https://docs.kidger.site/diffrax/api/interpolation/
    """
    return dfx.LinearInterpolation(ts=t_data,ys=input_data)


def get_vector_field(
        cdcm_sys: System,
        t_data: jax.Array,
        input_dict: Dict,
        dt: float,
        states=None,
    ):
    """
    This function constructes the vector_field (python function return
    ing temporal derivatives of states) corresponding to an
    arbitrary `cdcm_sys`.

    Arguments:
        cdcm_sys: CDCM System object of which vector field is required
        t_data: time instants at which input signals are available
        input_dict: Dictionary containing Input signals.it is of the form:
            {
                cdcm_data_node.name : data as array
                ....
            }
        dt: time step value for diffrax system
        states: (optional) A list of State nodes of `cdcm_sys` representing
            subgraph of the `cdcm_sys`. vector_field corresponding to this 
            function will be created. By default all state of `cdcm_sys` is
            considered.
    
    Return:
        vector_field: Callable Python function which returns temporal
            derivatives for diffrax.
        param_set: Set of Parameter nodes of the vector field
        vars_set: Set of Variable nodes with Forward functions of
            the vector field
        states_set: Set of State nodes with Transition functions
            of the vector field
        ordered_fn_list: A List consisting of the Forward and 
            Transition python functions sorted in topological order.

    Note
    state set may have more states than those in arg: states
    in a different order

    """
    

    #{"cdcm_data_node_name":interpolate_Texts(t_input,input_attr}
    input_signal = {}

    for input, data in input_dict.items():
        input_signal[input]= interpolate_Texts(t_data,data)
    if states is None:
        states = cdcm_sys.states
        row_state, t_state = [i for i in states if i.name in ["row", "t"]]
        states.remove(row_state)
        states.remove(t_state)
    print('names of the states',[i.name for i in states])
    
    (
        params_set, 
         vars_set,
         input_set,
         states_set,
    ) = get_params_vars_input_states_set(cdcm_sys,states)
    data_node = [i for i in params_set if i.name == "data_node"][0]
    params_set.remove(data_node)
    ordered_fn_list = get_ordered_fn_list(cdcm_sys,vars_set,states_set)
    (dict_of_fn_args_info_dict,
     dict_of_fn_res_info_dict) = get_fn_args_res_info(
                                    params_set,
                                    input_set,
                                    vars_set,
                                    states_set,
                                    ordered_fn_list,
                                )

    @jit 
    def vector_field(t,states,args):
        """
        states are as per states_set not the states
        given to get_dynamical_syst()
        """
        
        param_input_var_state_value_dict = {
            "params":[*args],
            "input":[
            input_signal[i.name].evaluate(t)
            for i in input_set],
            "vars":[None]*len(vars_set),
            "states":jnp.array(states), #[*states], #given
            "next_state":[None]*len(states_set)
        }
        for fn in ordered_fn_list:
            fn_args_info = dict_of_fn_args_info_dict[fn.name]
            fn_args = []
            for _,v in fn_args_info.items():
                parent_type = v["parent_type"]
                local_idx = v["local_idx"]
                fn_arg = param_input_var_state_value_dict\
                [parent_type][local_idx]
                fn_args.append(fn_arg)
            fn_res = fn.func(*fn_args)
            fn_res_info = dict_of_fn_res_info_dict[fn.name]
            
            if len(fn_res_info.items())==1:
                v=fn_res_info[0]
                child_type = v["child_type"]
                local_idx = v["local_idx"]
                param_input_var_state_value_dict\
                [child_type][local_idx] = fn_res
            else:
                for k,v in fn_res_info.items():
                    child_type = v["child_type"]
                    local_idx = v["local_idx"]
                    param_input_var_state_value_dict\
                    [child_type][local_idx] = fn_res[k]

        next_states = jnp.array(param_input_var_state_value_dict['next_state'])
        
        def get_time_derivs_lax(carry,x):
            new_state = next_states[x]
            state = param_input_var_state_value_dict['states'][x]
            time_deriv = (new_state-state)/dt
            return carry,time_deriv

        time_derivs = lax.scan(get_time_derivs_lax,None,xs=jnp.arange(len(states)))[1]
        return time_derivs
                    
    return vector_field, params_set, vars_set, states_set, ordered_fn_list


