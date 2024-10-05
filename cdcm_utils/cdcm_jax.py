"""
This python file contains various utilites for creating a vector field 
corresponding to a CDCM System which can be passed to diffrax.

Author:
    Sreehari Manikkan

Date:
    09/24/2024
"""

import networkx as nx
import jax
from jax import jit, lax
import jax.numpy as jnp
import diffrax as dfx
from typing import Set, List, Dict
import copy

from cdcm import *

__all__ = ["make_cdcm_to_jaxvf"
           ]


class CDCMtoJAXVF():

    def __init__(self) -> None:
        self.get_names = lambda x: [i.name for i in x]
        self.get_absnames = lambda x:[i.absname for i in x]


    def is_var_with_empty_parents(self,node):
        is_var = type(node) is Variable
        is_par = len(node.parents) == 0
        return is_var and is_par


    def is_var_with_non_empty_parents(self,node):
        is_var = type(node) is Variable
        is_not_par = len(node.parents) != 0
        return is_var and is_not_par


    def get_sys_nodes_for_diffrax(
            self,
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
                        self.get_sys_nodes_for_diffrax(
                            node, sys_nodes_for_diffrax)
                    )
                else:
                    sys_nodes_for_diffrax.add(node)
        return  sys_nodes_for_diffrax


    def is_input_var(self,n):
        if len(n.parents) == 0:
            return False
        is_var = type(node) is Variable
        is_input = n.parents[0].name in ["read"]
        return is_var and is_input


    def is_type(self,n,typ):
        return type(n) is typ


    def set_sys_nodes_for_diffrax(self,cdcm_sys: System):
        """
        sets an attribute `sys_nodes_for_diffrax` to the 
        cdcm_sys passed by calling get_sys_nodes_for_diffrax()
        function
        
        """
        if not hasattr(cdcm_sys, 'sys_nodes_for_diffrax'):
            cdcm_sys.sys_nodes_for_diffrax = set()
        cdcm_sys.sys_nodes_for_diffrax =  self.get_sys_nodes_for_diffrax(
            cdcm_sys, cdcm_sys.sys_nodes_for_diffrax
        )


    def get_params_vars_input_states_set(
            self,
            cdcm_sys: System,
            states_to_remove: List = ["row","t"],
            params_to_remove: List = ["data_node",],
            vars_to_remove: List = ["read"],
        ):
        """This The function gets the set of
        Parameter, Variable with Forward functions, Varibale part of
        DataSystem and all State of cdcm_sys.
        These sets represent the graph of
        CDCM System.

        Arguments:
            cdcm_sys: CDCM System Object
            states_to_remove: 
                List of absnames of state nodes to be excluded in states_set
            params_to_remove: 
                List of absnames of parameter nodes to be excluded in params_set
            vars_to_remove: 
                List of absnames of variable nodes to be excluded in vars_set or input_set
        
        Return:
            param_set: 
                Set of Parameter nodes and Variable nodes with no parent (Forward function)
            vars_set: Set of Variable nodes with Forward functions
            input_set: Set of Varibale nodes part of DataSystem
            states_set: Set of all State nodes
        """
        self.set_sys_nodes_for_diffrax(cdcm_sys)
        cdcm_sys.sys_starting_nodes = set()
        for n in cdcm_sys.sys_nodes_for_diffrax:
            if (
                self.is_var_with_empty_parents(n) 
                or self.is_input_var(n) 
                or self.is_type(n,Parameter)
            ):
                cdcm_sys.sys_starting_nodes.add(n)

        params_set = set()
        vars_set = set()
        input_set = set()
        states_set = set()

        all_vars = [
            i for i in cdcm_sys.sys_nodes_for_diffrax 
            if self.is_type(i,Variable) and i not in cdcm_sys.sys_starting_nodes
            ]
        input_vars = [i for i in all_vars if i.parents[0].name in ["read"]]
        vars = [i for i in all_vars if i not in input_vars]
        
        params_set.update(cdcm_sys.sys_starting_nodes)
        states_set.update(
            [i for i in cdcm_sys.sys_nodes_for_diffrax if self.is_type(i,State)])
        vars_set.update(vars)
        input_set.update(input_vars)

        for p in params_to_remove:
            for p_node in list(params_set):
                if p_node.name == p: params_set.remove(p_node)
        for v in vars_to_remove:
            for v_node in list(vars_set):
                if v_node.name == v: vars_set.remove(v_node)
            for v_node in list(input_set):
                if v_node.name == v: input_set.remove(v_node)
        for s in states_to_remove:
            for s_node in list(states_set):
                if s_node.name == s: states_set.remove(s_node)
        return params_set, vars_set, input_set, states_set



    def get_ordered_fn_list(
            self,
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
        self,
        params_set:set, 
        vars_set:set,
        input_set:set,
        states_set:set,
        param_input_var_state_set_dict: Dict,
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
            param_input_var_state_set_dict: Dict with content as follow
                param_input_var_state_set_dict = {
                    "params":list(params_set),
                    "input":list(input_set),
                    "vars":list(vars_set), 
                    "states":list(states_set),
                }
            ordered_fn_list: A List consisting of the Forward and 
                Transition python functions sorted in topological order.
        Return:
            dict_of_fn_args_info_dict: 
                A Python dictionary consisting of 
                seperate python dictionary for each function in `ordered_fn_list`.
                key of this dictionary is the absname of the function in the
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
                key of this dictionary is the absname of the function in the
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

        dict_of_fn_args_info_dict = {}
        dict_of_fn_res_info_dict = {}
        for fn in ordered_fn_list:
            fn_args_info_dict = {}
            fn_res_info_dict = {}
            
            for idx, parent in enumerate(fn.parents):
                parent_type = None
                if parent in params_set:
                    parent_type = "params" 
                elif parent in input_set:
                    parent_type = "input"
                elif parent in vars_set:
                    parent_type = "vars"
                elif parent in states_set:
                    parent_type = "states"
                if parent_type is None:
                    raise Exception("cannot determine the parent type of",parent.absname)
                local_idx = param_input_var_state_set_dict[parent_type].index(parent)
                fn_args_info_dict[idx] = {
                    "parent_type":parent_type,"local_idx":local_idx}
            
            for idx, child in enumerate(fn.children):
                child_type = None
                if child in vars_set:
                    child_type = "vars"
                    local_idx = param_input_var_state_set_dict[child_type].index(child)
                elif child in states_set:
                    child_type = "next_state"
                    local_idx = param_input_var_state_set_dict["states"].index(child)
                elif child_type is None:
                    raise Exception("cannot determine the child type of",child.absname)
                fn_res_info_dict[idx] = {
                    "child_type":child_type,"local_idx":local_idx}
                
            dict_of_fn_args_info_dict[fn.absname] = fn_args_info_dict
            dict_of_fn_res_info_dict[fn.absname] = fn_res_info_dict

        return dict_of_fn_args_info_dict, dict_of_fn_res_info_dict


    def interpolate_Texts(
            self,
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
            self,
            cdcm_sys: System,
            input_dict: Dict = None,
            dt: float = None,
            states_to_remove: List = ["row"],
            params_to_remove: List = ["data_node"],
            vars_to_remove: List = ["read"],
        ):
        """
        This function constructes the vector_field of all states (python function return
        ing temporal derivatives of states) corresponding to an
        arbitrary `cdcm_sys`.

        Arguments:
            cdcm_sys: CDCM System object of which vector field is required
            input_dict: Dictionary containing Input signals.it is of the form:
            {
                cdcm_data_node.name : {"data":data as array, "t_data": time data}
                ....
            }
            t_data is the time instants at which input signals are available
            dt: time step value of the cdcm_sys clock. Note THIS IS NOT THE
                TIME STEP VALUE TO BE USED FOR DIFFERENTIABLE SOLVER.
            states_to_remove: 
                List of absnames of state nodes to be excluded in states_set.
            params_to_remove: 
                List of absnames of parameter nodes to be excluded in params_set.
            vars_to_remove: 
                List of absnames of variable nodes to be excluded in vars_set or 
                input_set.
        
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

        """
        
        self.input_signal = {}

        if input_dict is not None:
            for input, data in input_dict.items():
                self.input_signal[input]= self.interpolate_Texts(
                    data["t_data"],
                    data["data"],
                    )
        
        (
            self.params_set, 
            self.vars_set,
            self.input_set,
            self.states_set,
        ) = self.get_params_vars_input_states_set(
            cdcm_sys,
            states_to_remove=states_to_remove,
            params_to_remove=params_to_remove,
            vars_to_remove=vars_to_remove,
            )

        self.ordered_fn_list = self.get_ordered_fn_list(
            cdcm_sys,
            self.vars_set,
            self.states_set
            )
        self.param_input_var_state_set_dict = {
            "params":list(self.params_set),
            "input":list(self.input_set),
            "vars":list(self.vars_set), 
            "states":list(self.states_set),
        }
        (self.dict_of_fn_args_info_dict,
        self.dict_of_fn_res_info_dict) = self.get_fn_args_res_info(
                                        self.params_set, 
                                        self.vars_set,
                                        self.input_set,
                                        self.states_set,
                                        self.param_input_var_state_set_dict,
                                        self.ordered_fn_list,
                                    )
        
        self.saved_vars = []

        # @jit 
        def vector_field(t,states,args):
            """
            states are as per states_set
            given to get_dynamical_syst(). This function returns temporal
            derivatives of the states present in the states_set.
            """
            
            '''param_input_var_state_value_dict = {
                "params":[*args],
                "input":[
                    input_signal[i.absname].evaluate(t)
                    for i in input_set],
                "vars":[None]*len(vars_set),
                "states":states,
                "next_state":[None]*len(states_set)
            }
            for fn in ordered_fn_list:
                fn_args_info = dict_of_fn_args_info_dict[fn.absname]
                fn_args = []
                for _,v in fn_args_info.items():
                    parent_type = v["parent_type"]
                    local_idx = v["local_idx"]
                    fn_arg = param_input_var_state_value_dict\
                    [parent_type][local_idx]
                    fn_args.append(fn_arg)
                fn_res = jnp.array([fn.func(*fn_args)]).reshape(-1,)
                fn_res_info = dict_of_fn_res_info_dict[fn.absname]
                
                for k,v in fn_res_info.items():
                    child_type = v["child_type"]
                    local_idx = v["local_idx"]
                    param_input_var_state_value_dict\
                    [child_type][local_idx] = fn_res[k]

            self.saved_vars.append(param_input_var_state_value_dict["vars"])'''
            self.get_param_input_var_state_value_dict(t,states,args)
            next_states = jnp.array(
                self.param_input_var_state_value_dict['next_state']
                )
            
            def get_time_derivs_lax(carry,x):
                new_state = next_states[x]
                state = self.param_input_var_state_value_dict['states'][x]
                time_deriv = (new_state-state)/dt
                return carry,time_deriv

            time_derivs = lax.scan(
                get_time_derivs_lax,None,xs=jnp.arange(len(states)))[1]
            return time_derivs
                        
        return vector_field
    

    def get_param_input_var_state_value_dict(self,t,states,args):
        self.param_input_var_state_value_dict = {
            "params":[*args],
            "input":[
                self.input_signal[i.absname].evaluate(t)
                for i in self.input_set],
            "vars":[None]*len(self.vars_set),
            "states":states,
            "next_state":[None]*len(self.states_set)
        }
        for fn in self.ordered_fn_list:
            fn_args_info = self.dict_of_fn_args_info_dict[fn.absname]
            fn_args = []
            for _,v in fn_args_info.items():
                parent_type = v["parent_type"]
                local_idx = v["local_idx"]
                fn_arg = self.param_input_var_state_value_dict\
                [parent_type][local_idx]
                fn_args.append(fn_arg)
            fn_res = jnp.array([fn.func(*fn_args)]).reshape(-1,)
            fn_res_info = self.dict_of_fn_res_info_dict[fn.absname]
            
            for k,v in fn_res_info.items():
                child_type = v["child_type"]
                local_idx = v["local_idx"]
                self.param_input_var_state_value_dict\
                [child_type][local_idx] = fn_res[k]
    

    def get_state_and_vars(self,t,states,args):
        self.get_param_input_var_state_value_dict(t,states,args)
        vars_array = jnp.array(self.param_input_var_state_value_dict["vars"])
        return states,vars_array
    
    def get_idx_of_qty_at_path(self,qty_set,path):
        return self.get_absnames(qty_set).index(path)



def make_cdcm_to_jaxvf():
    return CDCMtoJAXVF()