"""
Author: Amir Behjat

Date:
    7/08/2022


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

from cdcm import *
from . import make_eclss_pressure_env_0
from . import make_eclss_temperature_env_0
from . import make_eclss_energy_consumption_env_0

from dome_design import *

__all__ = ["make_eclss"]


def make_eclss(
    clock,
    dome_specs,
    # energy,
    energy_available_energy,
    structure_sec_1=None,
    structure_sec_2=None,
    structure_sec_3=None,
    structure_sec_4=None,
    structure_sec_5=None,
    struct_inside_temperature=None,
    int_env_temp=None,
    int_env_pres=None,
    HM_temperature_lower_setpoint=None,
    HM_temperature_upper_setpoint=None,
    HM_pressure_lower_setpoint=None,
    HM_pressure_upper_setpoint=None,
    make_eclss_pressure_env=make_eclss_pressure_env_0,
    make_eclss_temperature_env=make_eclss_temperature_env_0,
    make_eclss_energy_consumption_env=make_eclss_energy_consumption_env_0,
):
    """
    Make an eclss system.

    Arguments
    moon
    dome_specs,
    agent_clean_panel , agent_clean_plant, agent_cover_panel

    """
    with System(name="eclss", description="The eclss system") as eclss:
        # energy_available_energy = energy.energy_store.available_en

        if structure_sec_1 is None:
            structure_sec_1 = Variable(
                name="place_holder_structure_sec_1",
                value=1.0,
                units="",
                description="how much healthy is dome section 1",
            )
        if structure_sec_2 is None:
            structure_sec_2 = Variable(
                name="place_holder_structure_sec_2",
                value=1.0,
                units="",
                description="how much healthy is dome section 2",
            )
        if structure_sec_3 is None:
            structure_sec_3 = Variable(
                name="place_holder_structure_sec_3",
                value=1.0,
                units="",
                description="how much healthy is dome section 3",
            )
        if structure_sec_4 is None:
            structure_sec_4 = Variable(
                name="place_holder_structure_sec_4",
                value=1.0,
                units="",
                description="how much healthy is dome section 4",
            )
        if structure_sec_5 is None:
            structure_sec_5 = Variable(
                name="place_holder_structure_sec_4",
                value=1.0,
                units="",
                description="how much healthy is dome section 5",
            )
        if struct_inside_temperature is None:
            struct_inside_temperature = Variable(
                name="place_holder_int_str_temp",
                units="K",
                value=300.0,
                description="Temparature of the inner side of the structure",
            )
        if int_env_temp is None:
            int_env_temp = Variable(
                name="place_holder_int_env_temp",
                units="K",
                value=280.0,
                description="Temparature of the interior environment",
            )
        if int_env_pres is None:
            int_env_pres = Variable(
                name="place_holder_int_env_pres",
                units="atm",
                value=1.0,
                description="Pressure of the interior environment",
            )
        if HM_temperature_lower_setpoint is None:
            HM_temperature_lower_setpoint = Variable(
                name="place_holder_HM_lower_temparature_setpoint",
                units="",
                value=297.0,
                description="The lower temperature set point from HM to ECLSS",
            )
        if HM_temperature_upper_setpoint is None:
            HM_temperature_upper_setpoint = Variable(
                name="place_holder_HM_upper_temparature_setpoint",
                units="",
                value=303.0,
                description="The upper temperature set point from HM to ECLSS",
            )
        if HM_pressure_lower_setpoint is None:
            HM_pressure_lower_setpoint = Variable(
                name="place_holder_HM_lower_pressure_setpoint",
                units="",
                value=0.95,
                description="The lower pressure set point from HM to ECLSS",
            )
        if HM_pressure_upper_setpoint is None:
            HM_pressure_upper_setpoint = Variable(
                name="place_holder_HM_upper_pressure_setpoint",
                units="",
                value=1.05,
                description="The upper pressure set point from HM to ECLSS",
            )

        eclss_pressure = make_eclss_pressure_env(
            dome_specs,
            energy_available_energy,
            structure_sec_1,
            structure_sec_2,
            structure_sec_3,
            structure_sec_4,
            structure_sec_5,
            int_env_pres,
            HM_pressure_lower_setpoint,
            HM_pressure_upper_setpoint,
        )

        eclss_temperature = make_eclss_temperature_env(
            clock,
            dome_specs,
            eclss_pressure,
            energy_available_energy,
            struct_inside_temperature,
            int_env_temp,
            HM_temperature_lower_setpoint,
            HM_temperature_upper_setpoint,
        )

        eclss_energy_consumption = make_eclss_energy_consumption_env(
            energy_available_energy, eclss_pressure, eclss_temperature
        )

    return eclss
