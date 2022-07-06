"""
This is a simple occupancy model with 1 occupant
that interact with rc system and hvac.
If the current room temperature is out of occupancy endurability,
there is a chace that occupant may override the setpoint temperature.
Please find the complete documentation here:
https://github.com/nsf-cps-purdue/documentation/blob/main/systems/Occupant_model.ipynb
In this system, we will return the action of setpoint, on/off of
lighting and devices system.

Author:
    Ting-Chun Kuo

Date:
    5/5/2022
    5/18/2022
    7/06/2022

"""

__all__ = ["OccupantSystem"]


from cdcm import *
import numpy as np
import scipy.stats as st


class OccupantSystem(System):
    """
    This is a simple occupancy behavior model.

    Arguements:
    clock           --  The clock system
    T_room          --  The room air temperature [C] from rc system

    States:
    T_sp            --  The setpoint temperature [C]
    Occ_t           --  A boolean indicator of occupancy presence to the room
    action          --  A boolean indicator of whether the
                        occupant changes the setpoint

    Variables:
    p_action        --  Probability of act
    IHG_occ         --  The internal heat gain casud by occupant
    lgt_on          --  The ON/OFF indicator of lighting
    dev_on          --  The ON/OFF indicator of devices

    Parameters:
    T_p             --  actual preference temperature of the occupant[C]
    action_noise    --  action noise of the occupants
    gamma           --  occupancy sensitivity of the room temperature
    mu_heat         --  heating mode action parameter of occupants
    mu_cool         --  cooling mode action parameter of occupants
    T_sp_ub         --  upper bound of thermal control
    T_sp_lb         --  lower bound of thermal control

    Function nodes:
    check_occ       --  check occupancy presence and turn on/off light
                        and devices
    cal_act_prob    --  calculate action probability
    occ_tansition   --  Determine the next state

    """
    def define_internal_nodes(self,
                              clock=None,
                              T_room=None,
                              **kwargs):

        T_sp = State(
            name="T_sp",
            value=23,
            units="degC",
            description="The setpoint temperature to hvac system"
        )

        Occ_t = State(
            name="Occ_t",
            value=0,
            units=None,
            description="A boolean indicator of occupancy presence to the room"
        )

        action = State(
            name="action",
            value=0,
            units=None,
            description="Setpoint occupant changed"
        )

        T_p = Parameter(
            name="T_p",
            value=20.0,
            units="degC",
            description="Actual preference temperature of the occupant"
        )

        action_noise = Parameter(
            name="action_noise",
            value=1.0,
            units="degC",
            description="action noise of the occupants"
        )

        gamma = Parameter(
            name="gamma",
            value=0.5,
            units=None,
            description="occupancy sensitivity of the room temperature"
        )

        mu_heat = Parameter(
            name="mu_heat",
            value=2.0,
            units=None,
            description="heating mode action parameter of occupant"
        )

        mu_cool = Parameter(
            name="mu_cool",
            value=1.5,
            units=None,
            description="cooling mode action parameter of occupant"
        )

        T_sp_ub = Parameter(
            name="T_sp_ub",
            value=28.0,
            units="degC",
            description="upper bound of thermal control"
        )

        T_sp_lb = Parameter(
            name="T_sp_lb",
            value=18.0,
            units="degC",
            description="lower bound of thermal control"
        )

        p_action = Variable(
            name="p_action",
            value=0.1,
            units=None,
            description="The probability of the occupant to act"
        )

        lgt_on = Variable(
            name="lgt_on",
            value=1.0,
            units=None,
            description="The use percentage of ligting"
        )

        dev_on = Variable(
            name="dev_on",
            value=1.0,
            units=None,
            description="The use percentage of devices"
        )

        ihg_occ_base = Variable(
            name="ihg_occ_base",
            value=350.0,
            units="W",
            description="The base internal heat gain casud by occupant"
        )

        IHG_occ = Variable(
            name="IHG_occ",
            value=0.0,
            units="W",
            description="The internal heat gain casud by occupant"
        )

        @make_function(Occ_t)
        def check_occ(time=clock.t):
            """
            Calculate if occupancy is in the office by clock time
            """
            hour = time/3600 % 24
            occ = 0
            if (hour >= 8) and (hour <= 17):
                # This part can be replace with occupancy schedule
                occ = 1
            return occ

        @make_function(p_action)
        def cal_act_prob(T_room=T_room, T_p=T_p, gamma=gamma):
            """
            Determine probability to act or not by temperature difference
            and a sigmoid function.

            """
            x = gamma*(T_room - T_p)**2
            return 1/(1 + np.exp(-x))

        @make_function(lgt_on, dev_on, IHG_occ)
        def turnONOFF(Occ_t=Occ_t, ihg_occ_base=ihg_occ_base):
            # This part can be replace with other control type
            occ_ihg = np.random.normal(loc=ihg_occ_base, scale=ihg_occ_base/4)
            return Occ_t, Occ_t, occ_ihg

        @make_function(action)
        def occ_tansition(Occ_t=Occ_t,
                          T_room=T_room,
                          T_p=T_p,
                          T_sp=T_sp,
                          p_action=p_action,
                          mu_cool=mu_cool,
                          mu_heat=mu_heat,
                          T_sp_ub=T_sp_ub,
                          T_sp_lb=T_sp_lb,
                          action_noise=action_noise):
            """Determine the setpoint that changed by the occupant"""
            if Occ_t == 1:
                u = np.random.random()
                if u <= p_action:
                    rv_cool = st.poisson(mu_cool)
                    rv_heat = st.poisson(mu_heat)
                    action = T_room
                    if T_room > T_p:
                        # want to cool down
                        action = T_sp - rv_cool.rvs()
                    elif T_room < T_p:
                        # want to heat up
                        action = T_sp + rv_heat.rvs()
                    # Add clip function here
                    action = np.clip(action, T_sp_lb, T_sp_ub)
                else:
                    action = -1
            else:
                action = -1
            return action
