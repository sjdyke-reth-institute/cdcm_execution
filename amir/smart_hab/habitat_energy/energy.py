"""
Author: Amir Behjat

Date:
    7/08/2022


Defines the Energy interface/type/system/concept.

A `energyEnvironment` is `System` that exposes the following interface:


variable :: TypeOfVariable

(variable) = optional variable

clock                 :: Clock     =>  _________________
moon                  :: Moon      => |                 | -> energy_performance  :: State[for HM]
(used-energy)         :: ECLSS     => |                 |
(cleaning_panel)      :: Agents    => |    EnergyEnv    |
(cleaning_radiator)   :: Agents    => |                 |
(covering_panel)      :: HM        => |                 |
design                :: DomeSpec  => |_________________| -> store_energy :: State


"""

from cdcm import *
from . import make_energy_performance_env_0
from . import make_energy_generate_env_0
from . import make_energy_store_env_0

from dome_design import *

__all__ = ["make_energy"]


def make_energy(
    clock,
    dust_rate,
    irradiance,
    ecless_energy_cons=None,
    agent_clean_panel=None,
    agent_clean_plant=None,
    HM_cover_panel=None,
    make_energy_performance_env=make_energy_performance_env_0,
    make_energy_generate_env=make_energy_generate_env_0,
    make_energy_store_env=make_energy_store_env_0,
):
    """
    Make a struct system.

    Arguments
    moon
    dome_specs,
    agent_clean_panel , agent_clean_plant, HM_cover_panel

    """
    with System(name="energy", description="The energy system") as energy:

        if ecless_energy_cons is None:
            ecless_energy_cons = Variable(
                name="place_holder_energy_cons",
                units="J",
                value=0.0,
                description="Total energy consumption in ECLSS",
            )
        if agent_clean_panel is None:
            agent_clean_panel = Variable(
                name="place_holder_agent_clean_panel",
                units="",
                value=0.0,
                description="Cleaning the panel value in one time step",
            )
        if agent_clean_plant is None:
            agent_clean_plant = Variable(
                name="place_holder_agent_clean_plant",
                units="",
                value=0.0,
                description="Cleaning the nuclear plant radiator value in one time step",
            )
        if HM_cover_panel is None:
            HM_cover_panel = Variable(
                name="place_holder_HM_cover_panel",
                units="",
                value=True,
                description="1= Solar panel is functional, 0= solar panel is covered against dust",
            )

        energy_performance = make_energy_performance_env(
            clock, dust_rate, agent_clean_panel, agent_clean_plant, HM_cover_panel
        )

        energy_generate = make_energy_generate_env(
            clock, irradiance, energy_performance
        )

        energy_store = make_energy_store_env(energy_generate, ecless_energy_cons)

    return energy
