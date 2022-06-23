"""
Defines the Energy interface/type/system/concept.

A `energyEnvironment` is `System` that exposes the following interface:

                                               _________________
disturbance        :: dust                 => |                 | -> energy_performanec        ::  energy healet [for HM]
ECLSS              :: used-energy        => |                 |
Agent              :: cleaning panels      => |    EnergyEnv    | 
                                              |                 |
Design             :: Dome design & specs  => |_________________| -> energy_store_power        :: stored power


"""



__all__ = ["make_energy"]


from cdcm import *
from . import make_energy_performance_env_0
from . import make_energy_generate_power_env_0
from . import make_energy_store_power_env_0


from dome_design import *


def make_energy(clock,
                moon,
                ecless_power_cons,
                agent_clean_panel,
                agent_clean_plant,
                agent_cover_panel,
                make_energy_performance_env=make_energy_performance_env_0,
                make_energy_generate_power_env=make_energy_generate_power_env_0,
                make_energy_store_power_env=make_energy_store_power_env_0,
                ):
    """
    Make a struct system.

    Arguments
    moon
    dome_specs,
    agent_clean_panel , agent_clean_plant, agent_cover_panel

    """
    with System(name="energy", description="The energy system") as energy:

        energy_performance = make_energy_performance_env(clock, moon, agent_clean_panel, agent_clean_plant, agent_cover_panel)

        energy_generate = make_energy_generate_power_env(clock, moon, energy_performance)

        energy_store = make_energy_store_power_env(energy_generate, ecless_power_cons)

    return energy

