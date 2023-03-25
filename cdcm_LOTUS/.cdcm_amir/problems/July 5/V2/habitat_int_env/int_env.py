"""
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


__all__ = ["make_int_env"]


from cdcm import *
from . import make_int_env_pressure_env_0
from . import make_int_env_temperature_env_0


from dome_design import *


def make_int_env(
    dome_specs,
    eclss_en_used_heat=None,
    eclss_en_needed_heat=None,
    eclss_en_used_pres=None,
    eclss_en_needed_pres=None,
    struct_health=None,
    struct_inside_temperature=None,
    HM_temperature_lower_setpoint=None,
    HM_temperature_upper_setpoint=None,
    HM_pressure_lower_setpoint=None,
    HM_pressure_upper_setpoint=None,
    make_int_env_pressure_env=make_int_env_pressure_env_0,
    make_int_env_temperature_env=make_int_env_temperature_env_0,
):
    """
    Make an interior environment system.

    Arguments
    moon
    dome_specs,
    agent_clean_panel , agent_clean_plant, agent_cover_panel

    """
    with System(name="int_env", description="The int_env system") as int_env:

        # if eclss_en_used_heat is None:
        #     eclss_en_used_heat = Variable(name="place_holder_en_used_heat", value=0.0, units="J", description="Used energy to control the temperature")
        # if eclss_en_needed_heat is None:
        #     eclss_en_needed_heat = Variable(name="place_holder_en_needed_heat", value=0.0, units="J", description="Needed energy to control the temperature")
        # if eclss_en_used_pres is None:
        #     eclss_en_used_pres = Variable(name="place_holder_en_used_pres", value=0.0, units="J", description="Used energy to control the pressure")
        # if eclss_en_needed_pres is None:
        #     eclss_en_needed_pres = Variable(name="place_holder_en_needed_pres", value=0.0, units="J", description="Needed energy to control the pressure")
        # if struct_health is None:
        #     struct_health = Variable(name="place_struct_health", value=[1.0, 1.0, 1.0, 1.0, 1.0], units="", description="The array of how much healthy is each dome section")
        # if struct_inside_temperature is None:
        #     struct_inside_temperature = Variable(name="place_holder_int_str_temp", units="K", description="Temparature of the inner side of the structure")
        # if HM_temperature_lower_setpoint is None:
        #     HM_temperature_lower_setpoint = Variable(name="place_holder_HM_lower_temparature_setpoint", units="", description="The lower temperature set point from HM to int_env")
        # if HM_temperature_upper_setpoint is None:
        #     HM_temperature_upper_setpoint = Variable(name="place_holder_HM_upper_temparature_setpoint", units="", description="The upper temperature set point from HM to int_env")
        # if HM_pressure_lower_setpoint is None:
        #     HM_pressure_lower_setpoint = Variable(name="place_holder_HM_lower_pressure_setpoint", units="", description="The lower pressure set point from HM to int_env")
        # if HM_pressure_upper_setpoint is None:
        #     HM_pressure_upper_setpoint = Variable(name="place_holder_HM_upper_pressure_setpoint", units="", description="The upper pressure set point from HM to int_env")

        # print('struct_health', struct_health)
        # input('vvvvvbbb')
        int_env_pressure = make_int_env_pressure_env(
            dome_specs,
            eclss_en_used_pres,
            eclss_en_needed_pres,
            struct_health,
            HM_pressure_lower_setpoint,
            HM_pressure_upper_setpoint,
        )

        int_env_temperature = make_int_env_temperature_env(
            eclss_en_used_heat,
            eclss_en_needed_heat,
            struct_inside_temperature,
            HM_temperature_lower_setpoint,
            HM_temperature_upper_setpoint,
        )

    return int_env
