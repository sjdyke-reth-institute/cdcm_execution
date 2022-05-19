"""
This python file can be used to create a RCBuildingSystem object in CDCM using
the Building object from YABML.

Author(s):
    Sreehari Manikkan
Date:
    05/11/2022
"""

from distutils.command.build_clib import build_clib
import pandas as pd
import numpy as np
from pint import UnitRegistry as ureg

from cdcm import *
from yabml import *

from hvac_system import HVACSystem
from rc_system import RCBuildingSystem

Q_ = ureg().Quantity


def rc_of_zone(zone, neighbor):
    """
    Returns the R and C parameters of a zone modelled in YABML required
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
    cp_air = 1006 #J/Kg-C
    rho_air = 1.2 #Kg/m^3
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
            #inidicator for whether the layer is transparent
            solar_trans = 1
            r = 0
            c = 0
            for l in seg.segment.layers:
                thickness = Q_(l.thickness.value, l.thickness.units)
                conductivity = Q_(l.conductivity.value, l.conductivity.units)
                density = Q_(l.density.value, l.density.units)
                specific_heat = Q_(l.specific_heat.value, l.specific_heat.units)
                solar_transmittance = l.solar_transmittance.value
                # if one layer is not transparent,the segment is not
                # transparent
                solar_trans = min(solar_trans, solar_transmittance) 
                
                # calculate R and C for layers
                r += thickness/conductivity
                c += thickness*density*specific_heat
            U += 1 / ( r /(area_ratio * Area))
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
    if out == False:
        Cp_env = np.inf
        R_gr = np.inf
    else:
        for i in range(5):
            if neighbor[i]==0:
                # add the R and C of all exterior surfaces except floor
                R_oe += 1/R_list[i]
                Cp_env += C_list[i]
                R_er += 0.87*5.678/Area_list[i]# film coefficeint
        R_er = 1/R_er
    if ground == False:
        Cp_genv = np.inf
        R_gr = np.inf
        R_ge = np.inf
    else:
        Cp_genv = C_list[5]
        R_gr += 0.87*5.678/Area_list[5]
        R_ge = R_list[5]
    if cor == True:
        for i in range(6):
            if neighbor[i]!=0:
                # add the R
                R_rc += 1/R_list[i]
                R_rc += 0.87*5.678/Area_list[i]# film coefficeint
        R_rc = 1/ R_rc
    else:
        R_rc = np.inf

    return Cp_room, Cp_env, Cp_genv, R_rc, R_oe, R_er, R_gr, R_ge


def building_sys(building, weather_sys, clock):
    """
    Returns a system corresponding to the building given.

    Arguments:
        building: A YABML Building class object of which rc system is 
                  required.
        weather_system: A weather system that includes:
                        Tout: outdoor air temperature
                        Qsg:  solar irradiance
                        Qint: internal heat gain
                        T_gd: ground temperature.
                        Its is a 
        clock: A system that keeps track of time. It is a clock class
               object.

    Return:
        building_system: A list containing systems of each zone of
                         the building given. It is a list.
    """
    build_system = []
    for z,n in zip(building.zones, building.neighbor):
        zone_rc_sys = RCBuildingSystem(clock.dt,
                                       weather_sys,
                                       name="zone_rc_sys"
        )
        Cp_room, Cp_env, Cp_genv, R_rc, R_oe, R_er, R_gr, R_ge = \
            rc_of_zone(z,n)
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
                                   name="hvac_sys"
        )
        sys = System(
            name="everything",
            nodes=[clock, weather_sys, zone_rc_sys, zone_hvac_sys]
        )
        build_system.append(sys)
    return build_system




