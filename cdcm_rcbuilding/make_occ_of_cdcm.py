"""
make_occ_of_cdcm.py
This python file contains function which creates a building Occupant
CDCM system corresponding to a YABML Occupant object.

Author(s):
    Sreehari Manikkan
Date:
    06/30/2022
"""

import numpy as np

from cdcm import *
from occupant_system import OccupantSystem


def make_occ_of_cdcm(occ, clock, zone_rc_sys, name):
    """
    Makes an occupant CDCM system corresponding to the YABML Occupant object
    of a zone given.

    Arguments:

        occ: YABML occupant object of a zone.
        clock: CDCM clock system.
        zone_rc_sys: CDCM RCBuildingSystem object of the zone considered.
        name: name of the OccupantSystem object to be created. It is a
                   string.

    """

    with OccupantSystem(
        clock, zone_rc_sys.T_room_sensor, name=name
    ) as zone_occ_sys:
        #  parsing information from YABML to CDCM system
        zone_occ_sys.T_p.value = occ.T_p.value
        zone_occ_sys.action_noise.value = occ.action_noise.value
        zone_occ_sys.sensitivity.value = occ.sensitivity.value
        zone_occ_sys.occ_ihg_base.value = occ.occ_ihg_base.value
