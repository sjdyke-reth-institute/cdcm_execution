"""A structure_temp model.

                                                _________________________
disturbance        :: iradiance             => |                        |
Interior-En        :: Interior-Env_temp     => |   StructureTempEnv     | ->  structure internal wall temperature
disturbance        :: surface temperature   => |                        |
Design             :: Dome design & specs   => _________________________

"""

__all__ = ["make_structure_temp_env_0"]



from cdcm import *
import numpy as np

def make_structure_temp_env_0(struct_health,
                              dome_specs, moon,
                              int_env_temp):
    with System(name="structure_temp", description="The structure_temp environment") as structure_temp:
        ext_str_temp = (make_node("S:ext_str_temp",
                                  value=100.0,
                                  units="",
                                  description="ext_str_temp"))
        int_str_temp = (make_node("S:int_str_temp",
                                  value=320.0,
                                  units="",
                                  description="int_str_temp"))
        @make_function(ext_str_temp, int_str_temp)
        def f_struct_temp(ext_str_temp=ext_str_temp,
                          int_str_temp=int_str_temp,
                          structure_sec_1=struct_health.structure_sec_1,
                          structure_sec_2=struct_health.structure_sec_2,
                          structure_sec_3=struct_health.structure_sec_3,
                          structure_sec_4=struct_health.structure_sec_4,
                          structure_sec_5=struct_health.structure_sec_5,
                          nominal_cond_coef=dome_specs.nominal_cond_coef,
                          damaged_cond_coef=dome_specs.damaged_cond_coef,
                          dom_thickness=dome_specs.dom_thickness,
                          int_conv_coef=dome_specs.int_conv_coef,
                          surf_absorb_coef=dome_specs.surf_absorb_coef,
                          surf_emiss_coef=dome_specs.surf_emiss_coef,
                          stefan_boltzmann_constant=dome_specs.stefan_boltzmann_constant,
                          irradiation=moon.radiation.irradiance,
                          external_temp=moon.thermal.surface_temperature,
                          int_env_temp=int_env_temp):
            """Transition function for covering_panels_solar"""
            struct_latent = (structure_sec_1 +
                             structure_sec_2 +
                             structure_sec_3 +
                             structure_sec_4 +
                             structure_sec_5) / 5.0
            ext_str_temp_new = ((1.0 * int_str_temp *
                                   (0.001 + abs((int_str_temp -
                                                 ext_str_temp) *
                                                (nominal_cond_coef *
                                                 struct_latent +
                                                 damaged_cond_coef *
                                                 (1.0 - struct_latent)) /
                                                dom_thickness)) +
                                   1.0 * external_temp *
                                   (0.001 + abs((irradiation +
                                                 np.power(external_temp,
                                                          4)) *
                                                surf_absorb_coef *
                                                stefan_boltzmann_constant -
                                                np.power(ext_str_temp, 4) *
                                                surf_emiss_coef *
                                                stefan_boltzmann_constant))) /
                                  (1.0 * (0.001 + abs((int_str_temp -
                                                       ext_str_temp) *
                                                      (nominal_cond_coef *
                                                       struct_latent +
                                                       damaged_cond_coef *
                                                       (1.0 - struct_latent)) /
                                                      dom_thickness)) +
                                   1.0 * (0.001 +
                                          abs((irradiation +
                                               np.power(external_temp, 4)) *
                                              surf_absorb_coef *
                                              stefan_boltzmann_constant -
                                              np.power(ext_str_temp, 4) *
                                              surf_emiss_coef *
                                              stefan_boltzmann_constant)))).item()
            # ext_str_temp_new = 320.0
            int_str_temp_new = (1.0 * ext_str_temp *
                                  (nominal_cond_coef * struct_latent +
                                   damaged_cond_coef *
                                   (1.0 - struct_latent)) /
                                  dom_thickness + 1.0 * int_env_temp *
                                  int_conv_coef) / (1.0 *
                                                      (nominal_cond_coef *
                                                       struct_latent +
                                                       damaged_cond_coef *
                                                       (1.0 - struct_latent)) /
                                                      dom_thickness +
                                                      1.0 * int_conv_coef)
            # int_str_temp_new = 320.0
            return ext_str_temp_new, \
                   int_str_temp_new
    return structure_temp
