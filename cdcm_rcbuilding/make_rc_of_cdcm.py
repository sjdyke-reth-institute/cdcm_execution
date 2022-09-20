"""
make_rc_of_cdcm.py
This python file contains function which creates a building RC
CDCM system corresponding to a YABML building object.

Author(s):
    Sreehari Manikkan
Date:
    06/30/2022
"""

import numpy as np

from cdcm import *
from rc_system import RCBuildingSystem


def make_rc_of_cdcm(zone, neighbor, dt, weather_sys, T_cor, Q_int, u_t, name):
    """
    Makes an RC CDCM system corresponding to the YABML zone given.

    Arguments:
        zone    --  A zone object of the building. Its an instance of the Zone
                    class in YABML.
        neighbor    --  neighbor list of the zone provided. Its a list.
        dt  --  The timestep to use (must be a node.)
        weather_system  --  A weather system that includes:
                            Tout: outdoor air temperature
                            Qsg:  solar irradiance
                            T_gd: ground temperature
        T_cor   -- The temperature of corridor. Typically constant. It
                        can be replaced with sensor value in implemenation.
                        [C]
        Q_int   --  Internal heat gain calculated from other system
        u_t     -- Control variable. Input heat loads to the system.
                        [W]
        name    -- name of the RCBuildingSystem object to be created. It is a
                   string. 

    """
    R_list = []
    C_list = []
    trans_list = []
    Area_list = []
    cp_air = 1006  # J/Kg-C
    rho_air = 1.2  # Kg/m^3
    x = zone.edges[0].lx.value
    z = zone.edges[0].ly.value
    y = zone.edges[1].lx.value
    V = x * y * z
    Cp_room = V * rho_air * cp_air

    for e in zone.edges:
        lx = e.lx.value
        ly = e.ly.value
        Area = lx * ly
        Area_list.append(Area)
        U = 0
        C = 0
        sub_trans_list = []

        for seg in e.segments:
            area_ratio = seg.relative_area.value
            # indicator for whether the layer is transparent
            solar_trans = 1
            r = 0
            c = 0

            for layer in seg.segment.layers:
                thickness = layer.thickness.value
                conductivity = layer.conductivity.value
                density = layer.density.value
                specific_heat = layer.specific_heat.value
                solar_transmittance = layer.solar_transmittance.value
                # if one layer is not transparent,the segment is not
                # transparent
                solar_trans = min(solar_trans, solar_transmittance)

                # calculate R and C for layers
                r += thickness / conductivity
                c += thickness * density * specific_heat
            U += 1 / (r / (area_ratio * Area))
            C += c * area_ratio * Area
            sub_trans_list.append(solar_trans)

        R_list.append(1 / U)
        C_list.append(C)
        trans_list.append(sub_trans_list)

    # check nodal condition and return corresponding RC model
    out = True
    ground = False
    cor = False

    if neighbor[5] == 0:
        # the model has ground node
        ground = True

    if not all(v == 0 for v in neighbor):
        cor = True

    if all(v != 0 for v in neighbor[0:5]):
        out = False

    # Setup 5R3C model parameter placeholders
    R_oe = 0
    Cp_env = 0
    R_er = 0
    R_gr = 0
    R_ge = 0
    Cp_genv = 0
    R_rc = 0

    # By checking out, ground, cor, set RC model accordingly
    if out is False:
        Cp_env = np.inf
        R_gr = np.inf
    else:
        for i in range(5):
            if neighbor[i] == 0:
                # add the R and C of all exterior surfaces except floor
                R_oe += 1 / R_list[i]
                Cp_env += C_list[i]
                R_er += 0.87 * 5.678 / Area_list[i]  # film coefficeint
        R_oe = 1 / R_oe

    # 3R2C case
    if ground is False:
        Cp_genv = np.inf
        R_gr = np.inf
        R_ge = np.inf
    else:
        Cp_genv = C_list[5]
        R_gr += 0.87 * 5.678 / Area_list[5]
        R_ge = R_list[5]

    if cor is True:
        for i in range(6):
            if neighbor[i] != 0:
                # add the R
                R_rc += 1 / R_list[i]
                R_rc += 0.87 * 5.678 / Area_list[i]  # film coefficeint.
        R_rc = 1 / R_rc
    else:
        R_rc = np.inf

    with RCBuildingSystem(
        dt,
        weather_sys,
        T_cor,
        Q_int,
        u_t,
        name=name,
    ) as zone_rc_sys:
        """
        we parse the information from YABML to CDCM system by setting
        the values of C and R parameters of CDCM RC system with the values
        we obtained.
        """
        zone_rc_sys.C_room.value = Cp_room
        zone_rc_sys.C_env.value = Cp_env
        zone_rc_sys.C_genv.value = Cp_genv
        zone_rc_sys.R_rc.value = R_rc
        zone_rc_sys.R_oe.value = R_oe
        zone_rc_sys.R_er.value = R_er
        zone_rc_sys.R_gr.value = R_gr
        zone_rc_sys.R_ge.value = R_ge
    # return Cp_room, Cp_env, Cp_genv, R_rc, R_oe, R_er, R_gr, R_ge
