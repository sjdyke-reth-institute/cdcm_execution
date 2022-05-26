"""
building_system.py
This python file contains functions which are required for creating a building
CDCM system corresponding to a YABML building object.

Author(s):
    Sreehari Manikkan
Date:
    05/23/2022
"""

import pandas as pd
import numpy as np
from pint import UnitRegistry as ureg

from cdcm import *
from yabml import *

from hvac_system import HVACSystem
from rc_system import RCBuildingSystem

Q_ = ureg().Quantity


def make_rc_of_cdcm(zone, neighbor):
    """
    Returns the R and C parameters of the zone required
    for RCBuildingSystem in CDCM.

    Arguments:
        zone: A zone object of the building. Its an instance of the Zone
            class in YABML.
        neighbor: neighbor list of the zone provided. Its a list.

    Return:
        Cp_room: Capacitance of the air inside the zone
        Cp_env: Capacitance of the envelopes of zone
        Cp_genv: Heat capacity of ground envelope of zone
        R_rc: Thermal resistance between room and corridor for the zone
        R_oe: Thermal resistance between outdoor and envelope for the
            zone
        R_er: Thermal resistance between room and envelope for the zone
        R_gr: Thermal resistance between room and ground for the zone
        R_ge: Thermal resistance between ground and envelope for the
            zone

    """
    R_list = []
    C_list = []
    trans_list = []
    Area_list = []
    cp_air = 1006  # J/Kg-C
    rho_air = 1.2  # Kg/m^3
    x = Q_(zone.edges[0].lx.value, zone.edges[0].lx.units)
    z = Q_(zone.edges[0].ly.value, zone.edges[0].ly.units)
    y = Q_(zone.edges[1].lx.value, zone.edges[1].lx.units)
    V = (x*y*z)
    Cp_room = (V*rho_air*cp_air).magnitude

    for e in zone.edges:
        lx = Q_(e.lx.value, e.lx.units)
        lx.ito_base_units()
        ly = Q_(e.ly.value, e.ly.units)
        ly.ito_base_units()
        Area = lx * ly
        Area_list.append(Area.magnitude)
        U = 0
        C = 0
        sub_trans_list = []

        for seg in e.segments:
            area_ratio = seg.relative_area.value
            # inidicator for whether the layer is transparent
            solar_trans = 1
            r = 0
            c = 0

            for layer in seg.segment.layers:
                thickness = Q_(layer.thickness.value,
                               layer.thickness.units)
                conductivity = Q_(layer.conductivity.value,
                                  layer.conductivity.units)
                density = Q_(layer.density.value,
                             layer.density.units)
                specific_heat = Q_(layer.specific_heat.value,
                                   layer.specific_heat.units)
                solar_transmittance = layer.solar_transmittance.value
                # if one layer is not transparent,the segment is not
                # transparent
                solar_trans = min(solar_trans, solar_transmittance)

                # calculate R and C for layers
                r += thickness/conductivity
                c += thickness*density*specific_heat
            U += 1 / (r / (area_ratio * Area))
            C += c * area_ratio * Area
            sub_trans_list.append(solar_trans)

        R_list.append(1/U.magnitude)
        C_list.append(C.magnitude)
        trans_list.append(sub_trans_list)

    # check nodal condition and return corresponding RC model
    out = True
    ground = False
    cor = False

    if (neighbor[5] == 0):
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
    if out is False:  # here R_oe = Cp_env = R_er = inf ??
        Cp_env = np.inf
        R_gr = np.inf
    else:
        for i in range(5):
            if neighbor[i] == 0:
                # add the R and C of all exterior surfaces except floor
                R_oe += 1/R_list[i]
                Cp_env += C_list[i]
                R_er += 0.87*5.678/Area_list[i]  # film coefficeint
        R_oe = 1/R_oe

    # 3R2C case
    if ground is False:
        Cp_genv = np.inf
        R_gr = np.inf
        R_ge = np.inf
    else:
        Cp_genv = C_list[5]
        R_gr += 0.87*5.678/Area_list[5]
        R_ge = R_list[5]

    if cor is True:
        for i in range(6):
            if neighbor[i] != 0:
                # add the R
                R_rc += 1/R_list[i]
                R_rc += 0.87*5.678/Area_list[i]  # film coefficeint
        R_rc = 1 / R_rc
    else:
        R_rc = np.inf
    return Cp_room, Cp_env, Cp_genv, R_rc, R_oe, R_er, R_gr, R_ge


def make_building_cdcm_system(building, weather_sys, clock):
    """
    Returns a cdcm system corresponding to the building given.

    Arguments:
        building: A YABML Building class object.
        weather_system: A weather system.
        clock: A system that keeps track of time. It is a CDCM Clock
               class object.

    Return:
        building_system: A list containing CDCM system of each zone of
                         the building given. It is a list.
    """
    building_cdcm_system = []
    for z, n in zip(building.zones, building.neighbor):
        Q_int = Variable(
            name="Q_int",
            units="W",
            value=150,
            description="Sum of internal heat gain"
        )
        T_cor = Variable(
            name="T_cor",
            units="degC",
            value=23,
            description="Corridor temperature"
        )
        zone_rc_sys = RCBuildingSystem(clock.dt,
                                       weather_sys,
                                       T_cor,
                                       Q_int,
                                       name="zone_rc_system")
        Cp_room, Cp_env, Cp_genv, R_rc, R_oe, R_er, R_gr, R_ge = \
            make_rc_of_cdcm(z, n)
        zone_rc_sys.C_room.value = Cp_room
        zone_rc_sys.C_env.value = Cp_env
        zone_rc_sys.C_genv.value = Cp_genv
        zone_rc_sys.R_rc.value = R_rc
        zone_rc_sys.R_oe.value = R_oe
        zone_rc_sys.R_er.value = R_er
        zone_rc_sys.R_gr.value = R_gr
        zone_rc_sys.R_ge.value = R_ge

        T_out_sensor = Variable(
            name="T_out_sensor",
            units="degC",
            description="Measurement of external temperature."
        )
        T_out_sensor_sigma = Parameter(
            name="T_out_sensor_sigma",
            units="degC",
            value=0.01
        )
        T_sp = Variable(
            name="T_sp",
            units="degC",
            value=23
        )

        @make_function(T_out_sensor)
        def g_T_out_sensor(T_out=weather_sys.Tout, sigma=T_out_sensor_sigma):
            """Sample the T_out sensor."""
            return T_out + sigma * np.random.randn()

        zone_hvac_sys = HVACSystem(clock.dt,
                                   T_out_sensor,
                                   zone_rc_sys.T_room_sensor,
                                   zone_rc_sys.u,
                                   T_sp,
                                   name="zone_hvac_system")
        zone_cdcm_sys = System(
            name="zone_cdcm_system",
            nodes=[clock, weather_sys, T_cor, zone_rc_sys, zone_hvac_sys]
        )
        building_cdcm_system.append(zone_cdcm_sys)
    return building_cdcm_system
