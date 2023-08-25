"""python file containing functions for setting nodes required
for calibration in cdcm system

Author:
    Sreehari Manikkan
Date:
    08/24/2023
"""
from typing import Dict
import jax.numpy as jnp

from cdcm import *
from .derivatives import set_derivative

def setup_calibration(
        sys: node,
        data: Dict,
        parameter: node,
    ):
    state_nodes = sys.get_nodes_of_type(State)

    for sn in state_nodes:
        with sys:
            sn_sensor = Variable(
                name=sn.name+"_sensor",
                value=0.,
                units=sn.units,
            )

            @make_function(sn_sensor)
            def calc_sn_sensor(sn=sn):
                return sn
            
            error_sn = Variable(
                name="error_"+sn.name,
                value=0.,
                units=None,
            )

            sn_data = data[sn]
            @make_function(error_sn)
            def calc_error_sn(sn=sn):
                return jnp.square(sn - sn_data).mean()
        set_derivative(
            sys,
            error_sn,
            parameter,
            f"d{error_sn.absname}d{parameter.absname}",
        )


