"""An eclss_temperature model.


variable :: TypeOfVariable

(variable) = optional variable

                                                           _________________________
clock                     :: Clock                     => |                        | ->  en_needed_heat  :: State
design                    :: DomeSpec                  => |                        |
(available energy)        :: Energy                    => |                        |
(strucure_temp_innerside) :: Struct                    => |  EclssTemperatureEnv   |
(int_temperature)         :: InteriorEnv               => |                        |
(temperature setpoints)   :: HM                        => |                        | ->  en_needed_heat  :: State
eclss_pressure            :: EclssPressure             =>  _________________________


"""

__all__ = ["make_eclss_temperature_env_0"]



from cdcm import *

def make_eclss_temperature_env_0(clock,
                                 dome_specs,
                                 eclss_pressure,
                                 energy_available_energy,
                                 structure_int_struct_temp,
                                 interior_env_temp,
                                 HM_temperature_lower_setpoint,
                                 HM_temperature_upper_setpoint):
    with System(name="eclss_temperature", description="The eclss_temperature environment") as eclss_temperature:
        en_needed_heat = State(name="en_needed_heat",
                                    value=0.0,
                                    units="J",
                                    description="Energy needed to control temperature")
        en_used_heat = State(name="en_used_heat",
                                  value=0.0,
                                  units="J",
                                  description="Energy used to control temperature")

        @make_function(en_needed_heat,
                       en_used_heat)
        def f_eclss_heat(en_needed_heat=en_needed_heat,
                         dt=clock.dt,
                         available_en=energy_available_energy,
                         en_used_pres=eclss_pressure.en_used_pres,
                         int_str_temp=structure_int_struct_temp,
                         int_env_temp=interior_env_temp,
                         air_heat_capac=dome_specs.air_heat_capac,
                         int_conv_coef=dome_specs.int_conv_coef,
                         efficiency_of_TM=dome_specs.efficiency_of_TM,
                         lower_temp_setpo=HM_temperature_lower_setpoint,
                         upper_temp_setpo=HM_temperature_upper_setpoint,
                         ):
            """Transition function for ECLSS heat"""

            en_needed_heat_new = abs((((lower_temp_setpo +
                                          upper_temp_setpo) / 2 -
                                         int_env_temp) * air_heat_capac -
                                        dt * (int_str_temp -
                                                int_env_temp) *
                                        int_conv_coef) / efficiency_of_TM)
            en_used_heat_new = max(0.0,
                                     min(available_en -
                                         en_used_pres,
                                         en_needed_heat))
            return en_needed_heat_new, \
                   en_used_heat_new
    return eclss_temperature
