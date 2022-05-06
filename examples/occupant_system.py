"""
This is a simple occupants model that interact with rc system and hvac.
If the current room temperature is out of occupancy endurability,
there is a chace that occupant may override the setpoint temperature.

Author:
    Ting-Chun Kuo

Date:
    5/5/2022

"""

__all__ = ["OccupantSystem"]


from cdcm import *
import numpy as np


class OccupantSystem(System):
    """
    This is a simple occupancy behavior model.

    Arguements:
    dt              --  The timestep to use (must be a node.)
    rc_system       --  A rc system that includes:
                        T_room: The room air temperature [C]
    hvac_system     --  A hvac system that includes:
                        T_sp: The setpoint temperature [C]

    Variables:
    T_sp_occ        --  The setpoint that changed by the occupant [C]
    action          --  A boolean indicator of whether the
                        occupant changes the setpoint

    Parameters:
    T_p             --  actual preference temperature of the occupant[C]
    action_noise    --  action noise of the occupants

    Function nodes:
    cal_action      --  calculate action
    cal_T_sp_occ    --  Determine the setpoint occupant changes
    act_T_sp        --  The actual setpoint of the next time step



    """
    def __init__(self,
                 dt: Parameter,
                 T_room: Variable,
                 T_sp: Variable,
                 **kwargs):
        super().__init__(**kwargs)

        T_sp_occ = Variable(
            name="T_sp_occ",
            value=23,
            units="degC",
            description="The setpoint that changed by the occupant"
        )

        action = Variable(
            name="action",
            value=0,
            units=None,
            description="A boolean indicator of whether the \
                         occupant changes the setpoint"
        )

        T_p = Parameter(
            name="T_p",
            value=20,
            units="degC",
            description="Actual preference temperature of the occupant"
        )

        action_noise = Parameter(
            name="action_noise",
            value=1.0,
            units="degC",
            description="action noise of the occupants"
        )

        @make_function(action)
        def cal_action(T_room=T_room, T_p=T_p):
            """
            Determine to act or not by temperature difference
            and a sigmoid function.

            """
            x = T_room - T_p
            return 1 / (1 + np.exp(x))

        @make_function(T_sp_occ)
        def cal_T_sp_occ(T_p=T_p, action_noise=action_noise):
            """Determine the setpoint that changed by the occupant"""
            return np.exp(np.random.normal(loc=T_p,
                                           scale=action_noise**2))

        @make_function(T_sp)
        def act_T_sp(action=action, T_sp=T_sp, T_sp_occ=T_sp_occ):
            """Determine the actual setpoint of the next time step"""
            return action * T_sp_occ + (1 - action)*T_sp

        self.add_nodes(
            [
                T_sp_occ,
                action,
                T_p,
                action_noise,
                cal_action,
                cal_T_sp_occ,
                act_T_sp
            ]
        )
