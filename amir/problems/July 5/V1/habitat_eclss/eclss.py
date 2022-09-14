"""
Defines the eclss interface/type/system/concept.

A `eclssEnvironment` is `System` that exposes the following interface:


variable :: TypeOfVariable

(variable) = optional variable

                                                            _________________
(available energy)        :: Energy                    => |                 |
(int_temperature)         :: InteriorEnv               => |                 |
(int_pressure)            :: InteriorEnv               => |                 |
(strucure_health)         :: Struct                    => |                 |
(strucure_temp_innerside) :: Struct                    => |     eclssEnv    |  -> eclss_energy_consumption :: State
(temperature setpoints)   :: HM                        => |                 |
(pressure setpoints)      :: HM                        => |                 |
clock                     :: Clock                     => |                 |
design                    :: DomeSpec                  => |_________________|


"""



__all__ = ["make_eclss"]


from cdcm import *
from . import make_eclss_pressure_env_0
from . import make_eclss_temperature_env_0
from . import make_eclss_energy_consumption_env_0


from dome_design import *


def make_eclss(clock,
               dome_specs,
               energy_available_energy=None,
               struct_health=None,
               struct_inside_temperature=None,
               interior_env_temperature=None,
               int_env_pres=None,
               HM_temperature_lower_setpoint=None,
               HM_temperature_upper_setpoint=None,
               HM_pressure_lower_setpoint=None,
               HM_pressure_upper_setpoint=None,
               make_eclss_pressure_env=make_eclss_pressure_env_0,
               make_eclss_temperature_env=make_eclss_temperature_env_0,
               make_eclss_energy_consumption_env=make_eclss_energy_consumption_env_0
              ):
    """
    Make an eclss system.

    Arguments
    moon
    dome_specs,
    agent_clean_panel , agent_clean_plant, agent_cover_panel

    """
    with System(name="eclss", description="The eclss system") as eclss:

        # if energy_available_energy is None:
        #     energy_available_energy = Variable(name="place_holder_available_en", value=0.0, units="J", description="Available battery")
        # if struct_health is None:
        #     struct_health = Variable(name="place_holder_struct_health", value=[1.0, 1.0, 1.0, 1.0, 1.0], units="", description="The array of how much healthy is each dome section")
        # if struct_inside_temperature is None:
        #     struct_inside_temperature = Variable(name="place_holder_int_str_temp", units="K", description="Temparature of the inner side of the structure")
        # if interior_env_temperature is None:
        #     interior_env_temperature = Variable(name="place_holder_int_env_temp", units="K", description="Temparature of the interior environment")
        # if int_env_pres is None:
        #     interior_env_pressure = Variable(name="place_holder_int_env_pres", units="K", description="Pressure of the interior environment")
        # if HM_temperature_lower_setpoint is None:
        #     HM_temperature_lower_setpoint = Variable(name="place_holder_HM_lower_temparature_setpoint", units="K", description="The lower temperature set point from HM to ECLSS")
        # if HM_temperature_upper_setpoint is None:
        #     HM_temperature_upper_setpoint = Variable(name="place_holder_HM_upper_temparature_setpoint", units="K", description="The upper temperature set point from HM to ECLSS")
        # if HM_pressure_lower_setpoint is None:
        #     HM_pressure_lower_setpoint = Variable(name="place_holder_HM_lower_pressure_setpoint", units="atm", description="The lower pressure set point from HM to ECLSS")
        # if HM_pressure_upper_setpoint is None:
        #     HM_pressure_upper_setpoint = Variable(name="place_holder_HM_upper_pressure_setpoint", units="atm", description="The upper pressure set point from HM to ECLSS")


        # print('inside main eclss struct_health ', struct_health)
        eclss_pressure = make_eclss_pressure_env(dome_specs,
                                                 energy_available_energy,
                                                 struct_health,
                                                 int_env_pres,
                                                 HM_pressure_lower_setpoint,
                                                 HM_pressure_upper_setpoint)

        eclss_temperature = make_eclss_temperature_env(clock,
                                                       dome_specs,
                                                       eclss_pressure,
                                                       energy_available_energy,
                                                       struct_inside_temperature,
                                                       interior_env_temperature,
                                                       HM_temperature_lower_setpoint,
                                                       HM_temperature_upper_setpoint)

        eclss_energy_consumption = make_eclss_energy_consumption_env(energy_available_energy,
                                                                     eclss_pressure,
                                                                     eclss_temperature)

    return eclss

