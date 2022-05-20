"""
This is a simple occupancy model with 1 occupant
that interact with rc system and hvac.
If the current room temperature is out of occupancy endurability,
there is a chace that occupant may override the setpoint temperature.
# TODO: ADD Equations here and change the code
In this system, we will return the action of setpoint, on/off of
lighting and devices system.

Author:
    Ting-Chun Kuo

Date:
    5/5/2022
    5/18/2022

"""

__all__ = ["OccupantSystem"]


from cdcm import *
import numpy as np


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
    sensitivity     --  occupancy sensitivity of the room temperature
    time            --  temperary time holding place

    Function nodes:
    check_occ       --  check occupancy presence and turn on/off light
                        and devices
    cal_act_prob    --  calculate action probability
    occ_tansition   --  Determine the next state

    """
    def __init__(self,
                 dt: Parameter,
                 T_room: Variable,
                 **kwargs):
        super().__init__(**kwargs)

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
            description="A boolean indicator of whether the\
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

        sensitivity = Parameter(
            name="sensitivity",
            value=0.5,
            units=None,
            description="occupancy sensitivity of the room temperature"
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

        occ_ihg_base = Variable(
            name="occ_ihg_base",
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

        time = State(
            name="time",
            value=0.0,
            units="s",
            description="Current time in sec"
            )

        @make_function(time)
        def move_time(time=time, dt=dt):
            """
            move time
            """
            return time + dt

        @make_function(Occ_t)
        def check_occ(time=time):
            """
            Calculate if occupancy is in the office by clock time
            """
            hour = time/3600 % 24
            occ = 0
            if (hour >= 8) and (hour <= 17):
                occ = 1
            return occ

        @make_function(p_action)
        def cal_act_prob(T_room=T_room, T_p=T_p, sensitivity=sensitivity):
            """
            Determine probability to act or not by temperature difference
            and a sigmoid function.

            """
            x = sensitivity*(T_room - T_p)**2
            return 1/(1 + np.exp(-x))

        @make_function(lgt_on, dev_on, IHG_occ)
        def turnONOFF(Occ_t=Occ_t, occ_ihg_base=occ_ihg_base):
            occ_ihg = np.random.normal(loc=occ_ihg_base, scale=occ_ihg_base/4)
            return Occ_t, Occ_t, occ_ihg

        @make_function(action, T_sp)
        def occ_tansition(Occ_t=Occ_t,
                          T_p=T_p,
                          T_sp=T_sp,
                          p_action=p_action,
                          action_noise=action_noise):
            """Determine the setpoint that changed by the occupant"""
            if Occ_t == 1:
                u = np.random.random()
                theta = np.random.normal(loc=0.0, scale=action_noise)
                if u <= p_action:
                    T_sp = round((T_p + theta), 2)
                    action = T_sp
                else:
                    action = -1
            else:
                occ_ihg = 0
                action = -1
                T_sp = T_sp
            return action, T_sp

        self.add_nodes(
            [
                T_sp,
                Occ_t,
                action,
                lgt_on,
                dev_on,
                IHG_occ,
                occ_ihg_base,
                T_p,
                action_noise,
                sensitivity,
                time,
                move_time,
                check_occ,
                cal_act_prob,
                turnONOFF,
                occ_tansition
            ]
        )
