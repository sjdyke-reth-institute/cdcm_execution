"""
Author: Amir Behjat

Date:
    7/08/2022


Defines the int_env interface/type/system/concept.

A `int_envEnvironment` is `System` that exposes the following interface:

variable :: TypeOfVariable

(variable) = optional variable

                                                    ___________________
(eclss_used_energy_heat)    :: EClSS            => |                  |
(eclss_needed_energy_heat)  :: EClSS            => |                  | -> int_env_temperature  ::  State
(eclss_used_energy_pres)    :: EClSS            => |                  |
(eclss_needed_energy_pres)  :: EClSS            => |                  |
(strucure_health)           :: Struct           => |    int_envEnv    |
(strucure_temp_innerside)   :: Struct           => |                  |
(temperature setpoints)     :: HM               => |                  |
(pressure setpoints)        :: HM               => |                  | -> int_env_pressure     ::  State
design                      :: DomeSpec         => |__________________|

"""

from cdcm import *
from . import make_int_env_pressure_env_0
from . import make_int_env_temperature_env_0

from dome_design import *

__all__ = ["make_int_env"]


def make_int_env(dome_specs,
                 eclss_en_used_heat,
                 eclss_en_needed_heat,
                 eclss_en_used_pres,
                 eclss_en_needed_pres,
                 structure_sec_1,
                 structure_sec_2,
                 structure_sec_3,
                 structure_sec_4,
                 structure_sec_5,
                 struct_inside_temperature,
                 HM_temperature_lower_setpoint=None,
                 HM_temperature_upper_setpoint=None,
                 HM_pressure_lower_setpoint=None,
                 HM_pressure_upper_setpoint=None,
                 make_int_env_pressure_env=make_int_env_pressure_env_0,
                 make_int_env_temperature_env=make_int_env_temperature_env_0
                 ):
    """
    Make an interior environment system.

    Arguments
    moon
    dome_specs,
    agent_clean_panel , agent_clean_plant, agent_cover_panel

    """
    with System(name="int_env", description="The int_env system") as int_env:

        if HM_temperature_lower_setpoint is None:
            HM_temperature_lower_setpoint = Variable(
                name="place_holder_HM_lower_temparature_setpoint",
                units="",
                value=297.0,
                description="The lower temperature set point from HM to ECLSS")
        if HM_temperature_upper_setpoint is None:
            HM_temperature_upper_setpoint = Variable(
                name="place_holder_HM_upper_temparature_setpoint",
                units="",
                value=303.0,
                description="The upper temperature set point from HM to ECLSS")
        if HM_pressure_lower_setpoint is None:
            HM_pressure_lower_setpoint = Variable(
                name="place_holder_HM_lower_pressure_setpoint",
                units="",
                value=0.95,
                description="The lower pressure set point from HM to ECLSS")
        if HM_pressure_upper_setpoint is None:
            HM_pressure_upper_setpoint = Variable(
                name="place_holder_HM_upper_pressure_setpoint",
                units="",
                value=1.05,
                description="The upper pressure set point from HM to ECLSS")

        int_env_pressure = make_int_env_pressure_env(
            dome_specs,
            eclss_en_used_pres,
            eclss_en_needed_pres,
            structure_sec_1,
            structure_sec_2,
            structure_sec_3,
            structure_sec_4,
            structure_sec_5,
            HM_pressure_lower_setpoint,
            HM_pressure_upper_setpoint)

        int_env_temperature = make_int_env_temperature_env(
            eclss_en_used_heat,
            eclss_en_needed_heat,
            struct_inside_temperature,
            HM_temperature_lower_setpoint,
            HM_temperature_upper_setpoint)

    return int_env
