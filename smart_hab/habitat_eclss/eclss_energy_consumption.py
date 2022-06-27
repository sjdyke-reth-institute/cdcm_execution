"""An eclss_energy_consumption model.

variable :: TypeOfVariable

(variable) = optional variable

                                                              ___________________________
(available energy)           :: Energy                    => |                           |
                                                          => | eclssEnergyConsumptionEnv |  -> eclss_energy_consumption :: State
eclss_pressure               :: EclssPressure             => |                           |
eclss_temperature            :: EclssPressure             => |___________________________|


"""

__all__ = ["make_eclss_energy_consumption_env_0"]



from cdcm import *

def make_eclss_energy_consumption_env_0(available_en,
                                  eclss_pressure,
                                  eclss_temperature):
    with System(name="eclss_energy_consumption", description="The eclss_energy_consumption environment") as eclss_energy_consumption:
        energy_cons = (make_node("S:energy_cons",
                                value=0.0,
                                units="J",
                                description="energy_cons"))

        @make_function(energy_cons)
        def f_energy_consumption(en_used_heat=eclss_temperature.en_used_heat,
                                en_used_pres=eclss_pressure.en_used_pres,
                                available_en=available_en):
            """Transition function for ECLSS energy consumption"""
            energy_cons_new = min(available_en,
                                   en_used_heat +
                                   en_used_pres)
            return energy_cons_new
    return eclss_energy_consumption
