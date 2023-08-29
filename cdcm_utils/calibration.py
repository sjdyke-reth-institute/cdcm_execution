"""python file containing functions for setting nodes required
for calibration in cdcm system

Author:
    Sreehari Manikkan
Date:
    08/27/2023
"""

__all__ = [
           "calibrate_parameters"
           ]


from typing import Dict, List
import jax.numpy as jnp
import pandas as pd
import numpy as np
import scipy.optimize as optimize

from cdcm import *
from .derivatives import set_derivative


def setup_error_and_grad_nodes(
    sys: node,
    data_dict: Dict,
    parameter: node,
):
    """
    sets error nodes and gradient nodes w.r.t parameter associated with
    the given CDCM nodes.
    Arguments:
        sys: CDCM System. Derivative nodes will be added to this System.
        data_dict: A dict with syntax {cdcm_node: data as an iterable object}
        parameter: CDCM Parameter w.r.t which derivative nodes will be setup.
    Return:
        sn_err_nodes: A Dict of the form 
            {cdcm_node: error_node associated with cdcm_node}. cdcm_nodes
            are the keys of data_dict.
        sn_err_grad_nodes:A Dict of the form 
            {cdcm_node: error_gradient_node associated with cdcm_node}. cdcm_nodes
            are the keys of data_dict.
        sn_err_grad_update_seqs:A Dict of the form 
            {cdcm_node: derivateive_update_seq of error_gradient_node
            associated with cdcm_node}. cdcm_nodes
            are the keys of data_dict.
    """
    sns = list(data_dict.keys())
    sn_err_nodes = {}
    sn_err_grad_nodes, sn_err_grad_update_seqs = {}, {}
    for sn in sns:
        with sn.owner:
            sn_sensor = Variable(
                name=sn.name+"_sensor",
                value=0.,
                units=sn.units,
            )

            calc_sn_sensor = Function(
                name="calc_"+sn_sensor.name,
                func=lambda x: x,
                parents=sn,
                children=sn_sensor,
            )
            
            sn_error = Variable(
                name=sn.name+"_error",
                value=0.,
                units=None,
            )

            sn_obs = Parameter(
                name=sn.name+"_obs",
                value=0.,
                units=sn.units,
            )

            def calc_error_sn_fn(sn_sensor, sn_obs):
                return jnp.square(sn_sensor - sn_obs).sum()
            
            calc_sn_error = Function(
                name="calc_"+sn_error.name,
                func= calc_error_sn_fn,
                parents=[sn_sensor, sn_obs],
                children=sn_error,
            )
            
            sn_err_nodes[sn] = sn_error

        sn_err_grad_name = f"d{sn_error.absname}d{parameter.absname}"
        sn_err_grad_update_seq = set_derivative(
            sys=sys,
            y=sn_error,
            x=parameter,
            grad_name=sn_err_grad_name,
            derivative_update_seq=True,
        )
        sn_err_grad_nodes[sn] = getattr(sys,sn_err_grad_name)
        sn_err_grad_update_seqs[sn] = sn_err_grad_update_seq

    return sn_err_nodes, sn_err_grad_nodes, sn_err_grad_update_seqs

def get_vals(ns):
    return [i.value for i in ns]

def calibrate_parameters(
        simulator: Simulator,
        dt: float,
        max_steps: int,
        data_dict: Dict,
        parameters: List,
        optimizer: str,
        tval: float,
        gd_tol: float,
        gd_max_iter: int,
        lr: float,
):
    """
    function which calibrates the parameters of a cdcm system.
    Arguments:
        simulator: CDCM Simulator object. simulator.owner will be taken
            as the CDCM system to which the derivative nodes will be added.
        dt: time step. float value.
        max_steps: no. of time steps the simulator will be simulated.
            float value.
        data_dict: A dict with syntax {cdcm_node: data as an iterable object}
        parameters: A List of cdcm parameters to calibrate. These parameters
            should be part of the system corresponding to the simulator.
        optimizer: A string. 
            'GD' for Stochastic Gradient Descent.
            Optimizers available under scipy.minimize can also be passed.
            reference:
            https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.minimize.html#scipy.optimize.minimize
        tval: A float. The time instant at which the calibration happens. During
            optimization, the cdcm system will be reset to this time instant
            after each gradient evaluation and descent.
        gd_tol: tolerance value for loss incase optimizer = 'GD'. A float.
        gd_max_iter: maximum iteration for gradient descent optimizer. A float.
        lr: learning rate for gradient descent. A float.
    Return:
        loss_vals: A List containing sequence of loss values during optimization.
    """
    loss_vals = []
    sns = list(data_dict.keys())
    sys = simulator.system
    (
        sn_err_nodes,
        sn_err_grad_nodes,
        sn_err_grad_update_seqs) = setup_error_and_grad_nodes(
            sys=sys,
            data_dict=data_dict,
            parameter=parameters[0],
        )
    
    def set_ts(new_ts):
        def event():
            for idx, theta in enumerate(parameters):
                theta.value = new_ts[idx]
        return event
    
    def get_mean_error():
        return np.mean(get_vals(list(sn_err_nodes.values())))
    
    def get_mean_err_grad():
        return np.mean(get_vals(list(sn_err_grad_nodes.values())))
    
    def set_ic():
        for sn in sns:
            sn.value = data_dict[sn][0]
    
    def reset_sys():
        simulator.system.clock.t.value = tval
    
    def set_obs_values(t):
        def event():
            for sn in sns:
                sn_obs_node = getattr(sn.owner, sn.name+"_obs")
                sn_obs_node.value = data_dict[sn][t]
        return event
    
    def get_avg_loss_and_grad():
        err_grads = []
        errors = []
        rand_js = np.random.randint(0,max_steps,size=(int(0.5*max_steps),))
        for j in range(max_steps):
            simulator.add_event(j*dt,set_obs_values(j))
            simulator.forward()
            simulator.transition()
            if j in rand_js:
                err_grads.append(get_mean_err_grad())
                errors.append(get_mean_error())
        return np.mean(errors), np.mean(err_grads)
    
    def get_new_thetas_loss_grad(lr):
        ts = get_vals(parameters)
        loss_val,grad_val = get_avg_loss_and_grad()
        new_ts = ts - np.multiply(lr,grad_val)
        return new_ts, loss_val, grad_val

    def objective_fn(ts):
        simulator.add_event(tval,set_ic)
        simulator.add_event(tval,set_ts(ts))
        simulator.forward()
        loss_val,grad_val = get_avg_loss_and_grad()
        loss_vals.append(loss_val)
        print('loss',loss_val)
        curr_t = simulator.system.clock.t.value
        simulator.add_event(curr_t, reset_sys)
        simulator.forward()
        return loss_val,grad_val
    

    print(f'calibration starts at t = {tval}')
    if optimizer=='GD':
        itern=1
        loss = 100.
        while loss>gd_tol and itern<gd_max_iter:
            simulator.add_event(tval,set_ic)
            new_ts, loss, grad_val = get_new_thetas_loss_grad(lr)
            curr_t = simulator.system.clock.t.value
            simulator.add_event(curr_t,set_ts(new_ts))
            simulator.forward()
            if itern%1==0:
                loss_vals.append(loss)
                print('loss, grad',loss, grad_val)
            itern += 1
            curr_t = simulator.system.clock.t.value
            simulator.add_event(curr_t, reset_sys)
            simulator.forward()
        print(f"calibration over with {itern} iterations")
        print('loss, parameters',loss,get_vals(parameters))
    else:
        sol = optimize.minimize(
            objective_fn,
            get_vals(parameters),
            jac=True,
            method=optimizer,
            options={'disp':True},
        )
        print('parameters:',sol.x)
    return loss_vals
    


