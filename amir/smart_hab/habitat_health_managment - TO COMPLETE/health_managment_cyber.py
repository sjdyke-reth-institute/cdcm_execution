"""An health_managment_cyber model.

variable :: TypeOfVariable

(variable) = optional variable


                                                                      _______________________________
moon                               :: Moon                        => |                               |
energy                             :: Energy                      => |                               |
eclss                              :: Eclss                       => |                               |
struct                             :: Struct                      => |                               |
interior_env                       :: InteriorEnv                 => |   health_managment_cyberEnv   |
agents                             :: Agents                      => |                               |
health_managment_detection         :: Health_managment_detection  => |                               | -> temprature_set_points :: State[array]
clock                              :: Clock                       => |                               | -> pressurre_set_points :: State[array]
design                             :: DomeSpec                    => |_______________________________|


"""

__all__ = ["make_health_managment_cyber_env_0"]



from cdcm import *

def make_health_managment_cyber_env_0(clock,
                        dome_specs,
                        moon,
                        energy,
                        eclss,
                        struct,
                        interior_env,
                        agents,
                        health_managment_detection):
    with System(name="health_managment_cyber", description="The health_managment_cyber environment") as health_managment_cyber:
        health_managment_temperature_lower_setpoint = State(name="health_managment_temperature_lower_setpoint",
                                                            value=280.0,
                                                            units="K",
                                                            description="The lower temperature set point from health_managment to ECLSS")
        health_managment_temperature_upper_setpoint = State(name="health_managment_temperature_upper_setpoint",
                                                            value=310.0,
                                                            units="K",
                                                            description="The upper temperature set point from health_managment to ECLSS")
        health_managment_pressure_lower_setpoint = State(name="health_managment_pressure_lower_setpoint",
                                                         value=0.80,
                                                         units="atm",
                                                         description="The lower pressure set point from health_managment to ECLSS")
        health_managment_pressure_upper_setpoint = State(name="health_managment_pressure_upper_setpoint",
                                                         value=1.05,
                                                         units="atm",
                                                         description="The upper pressure set point from health_managment to ECLSS")
        health_managment_functional_covered = State(name="functional_covered",
                                                    value=1.0,
                                                    units="",
                                                    description="functionality of the solar panel; 1 is functional, 0 is covered")

        @make_function(health_managment_temperature_lower_setpoint,
                       health_managment_temperature_upper_setpoint,
                       health_managment_pressure_lower_setpoint,
                       health_managment_pressure_upper_setpoint,
                       health_managment_functional_covered)
        def f_cyber(clock=clock,
                    dome_specs=dome_specs,
                    moon=moon,
                    energy=energy,
                    eclss=eclss,
                    struct=struct,
                    interior_env=interior_env,
                    agents=agents,
                    health_managment_detection=health_managment_detection,
                    health_managment_temperature_lower_setpoint=health_managment_temperature_lower_setpoint,
                    health_managment_temperature_upper_setpoint=health_managment_temperature_upper_setpoint,
                    health_managment_pressure_lower_setpoint=health_managment_pressure_lower_setpoint,
                    health_managment_pressure_upper_setpoint=health_managment_pressure_upper_setpoint
                    ):
            """Transition function for health_managment cyber"""
            health_managment_functional_covered_new = False
            if moon.dust_rate > dome_specs.max_allowed_dust or moon.irradiance == 0:
                health_managment_functional_covered_new = True
            for fault in health_managment_detection:
                if fault['cyber_physical'] == 'Cyber':
                    #  in theory we must decide bas d on energy but we lack adequate health managment
                    if fault['current_value'] < fault['min_acceptable_value']:
                        if fault['name_state'] == 'int_env_temp':
                            if energy.available_energy >= energy.battery_capacity/4:
                                health_managment_temperature_lower_setpoint =  health_managment_temperature_lower_setpoint + (health_managment_temperature_upper_setpoint - health_managment_temperature_lower_setpoint) * 0.1
                            else:
                                health_managment_temperature_upper_setpoint = health_managment_temperature_upper_setpoint + (health_managment_temperature_upper_setpoint - health_managment_temperature_lower_setpoint) * 0.1
                        if fault['name_state'] == 'int_env_pres':
                            if energy.available_energy >= energy.battery_capacity/4:
                                health_managment_pressure_lower_setpoint =  health_managment_pressure_lower_setpoint + (health_managment_pressure_upper_setpoint - health_managment_pressure_lower_setpoint) * 0.1
                            else:
                                health_managment_pressure_upper_setpoint = health_managment_pressure_upper_setpoint + (health_managment_temperature_upper_setpoint - health_managment_temperature_lower_setpoint) * 0.1
                    if fault['current_value'] > fault['max_acceptable_value']:
                        if fault['name_state'] == 'int_env_temp':
                            if energy.available_energy >= energy.battery_capacity/4:
                                health_managment_temperature_upper_setpoint =  health_managment_temperature_upper_setpoint - (health_managment_temperature_upper_setpoint - health_managment_temperature_lower_setpoint) * 0.1
                            else:
                                health_managment_temperature_lower_setpoint = health_managment_temperature_lower_setpoint + (health_managment_temperature_upper_setpoint - health_managment_temperature_lower_setpoint) * 0.1
                        if fault['name_state'] == 'int_env_pres':
                            if energy.available_energy >= energy.battery_capacity/4:
                                health_managment_pressure_upper_setpoint =  health_managment_pressure_upper_setpoint - (health_managment_pressure_upper_setpoint - health_managment_pressure_lower_setpoint) * 0.1
                            else:
                                health_managment_pressure_lower_setpoint = health_managment_pressure_lower_setpoint + (health_managment_temperature_upper_setpoint - health_managment_temperature_lower_setpoint) * 0.1
            return health_managment_temperature_lower_setpoint, \
                health_managment_temperature_upper_setpoint, \
                health_managment_pressure_lower_setpoint, \
                health_managment_pressure_upper_setpoint, \
                health_managment_functional_covered_new
