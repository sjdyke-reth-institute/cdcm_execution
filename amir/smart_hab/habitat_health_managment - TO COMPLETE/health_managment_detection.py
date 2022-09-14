"""An health_managment_detection model.


variable :: TypeOfVariable

(variable) = optional variable

                                          _______________________________
moon          :: Moon                 => |                               |
energy        :: Energy               => |                               |
eclss         :: Eclss                => |                               |
struct        :: Struct               => |                               |
interior_env  :: InteriorEnv          => | health_managment_detectionEnv | -> fault_list :: State[array]
agents        :: Agents               => |                               |
clock         :: Clock                => |                               |
design        :: DomeSpec             => |_______________________________|


"""

from cdcm import *

__all__ = ["make_health_managment_detection_env_0"]



def make_health_managment_detection_env_0(clock,
                                          dome_specs,
                                          moon,
                                          energy,
                                          eclss,
                                          struct,
                                          interior_env,
                                          agents):
    with System(name="health_managment_detection", description="The health_managment_detection environment") as health_managment_detection:

        fault_list = State(name="energy_cons",
                           value=[],
                           units="J",
                           description="list of faults needed to be addressed by the ")

        @make_function(fault_list)
        def f_detection():
            """Transition function for health_managment fault detection"""
            fault_list_new = []
            return fault_list_new
    return health_managment_detection
