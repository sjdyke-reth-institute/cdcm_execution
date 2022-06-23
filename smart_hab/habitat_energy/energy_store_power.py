"""A structure_temp model.

                                      _________________________
ECLSS        :: used-energy     => |                        |
                                     |   StructureTempEnv     | ->  Energy stored power
Energy       :: generated power   => |                        |
                                     _________________________

"""

__all__ = ["make_energy_store_power_env_0"]



from cdcm import *

def make_energy_store_power_env_0(energy_generate,
                                  ecless_power_cons):
    with System(name="energy_store_power", description="The energy_store_power environment") as energy_store_power:
        battery_capacity_0 = 7200000.0

        battery_capacity = (make_node("P:battery_capacity",
                                      value=battery_capacity_0,
                                      units="J",
                                      description="battery_capacity"))
        available_en = (make_node("S:available_en",
                                  value=battery_capacity_0,
                                  units="J",
                                  description="available_en"))

        @make_function(available_en)
        def f_available_en(available_en=available_en,
                           gen_power_total=energy_generate.gen_power_total,
                           battery_capacity=battery_capacity,
                           power_cons=ecless_power_cons):
            """Transition function for available_en"""
            available_en_new = min(max(0.0, available_en +
                                         gen_power_total -
                                         power_cons),
                                     battery_capacity)
            return available_en_new
    return energy_store_power
