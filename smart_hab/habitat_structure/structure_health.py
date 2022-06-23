"""A structure_health model.


                                               _________________________
Agents             :: Dome Repair          => |                        |
                                              |   StructureHealthEnv   | ->  structure_health [for thermal/pressure isolation equations i.e. conduction & convection coefficents]
disturbance        :: meteor model         => |                        |
Design             :: Dome design & specs  => _________________________

"""


__all__ = ["make_structure_health_env_0"]



from cdcm import *
import numpy as np

def make_structure_health_env_0(moon, agent_repair_struct):
    with System(name="structure_health", description="The structure_health environment") as structure_health:
        structure_sec_1 = (make_node("S:structure_sec_1",
                                     value=1.0,
                                     units="",
                                     description="structure_sec_1"))
        structure_sec_2 = (make_node("S:structure_sec_2",
                                     value=1.0,
                                     units="",
                                     description="structure_sec_2"))
        structure_sec_3 = (make_node("S:structure_sec_3",
                                     value=1.0,
                                     units="",
                                     description="structure_sec_3"))
        structure_sec_4 = (make_node("S:structure_sec_4",
                                     value=1.0,
                                     units="",
                                     description="structure_sec_4"))
        structure_sec_5 = (make_node("S:structure_sec_5",
                                     value=1.0,
                                     units="",
                                     description="structure_sec_5"))
        print(moon)
        @make_function(structure_sec_1,
                       structure_sec_2,
                       structure_sec_3,
                       structure_sec_4,
                       structure_sec_5)
        def f_struct_health(structure_sec_1=structure_sec_1,
                            structure_sec_2=structure_sec_2,
                            structure_sec_3=structure_sec_3,
                            structure_sec_4=structure_sec_4,
                            structure_sec_5=structure_sec_5,
                            fix_structure_sec=agent_repair_struct,
                            meteor_impacts_1=moon.meteor.meteor_impacts_1,
                            meteor_impacts_2=moon.meteor.meteor_impacts_2,
                            meteor_impacts_3=moon.meteor.meteor_impacts_3,
                            meteor_impacts_4=moon.meteor.meteor_impacts_4,
                            meteor_impacts_5=moon.meteor.meteor_impacts_5
                            ):

            """Transition function for f_struct_health"""

            fix_structure_sec_1 = agent_repair_struct[0],
            fix_structure_sec_2 = agent_repair_struct[1],
            fix_structure_sec_3 = agent_repair_struct[2],
            fix_structure_sec_4 = agent_repair_struct[3],
            fix_structure_sec_5 = agent_repair_struct[4],

            meteorite_impact_sec_1 = meteor_impacts_1  # meteor_impacts[0]
            meteorite_impact_sec_2 = meteor_impacts_2  # meteor_impacts[1]
            meteorite_impact_sec_3 = meteor_impacts_3  # meteor_impacts[2]
            meteorite_impact_sec_4 = meteor_impacts_4  # meteor_impacts[3]
            meteorite_impact_sec_5 = meteor_impacts_5  # meteor_impacts[4]

            struct_1_T = min(max(structure_sec_1 -
                                 meteorite_impact_sec_1 +
                                 fix_structure_sec_1, 0.001), 1.0)
            struct_2_T = min(max(structure_sec_2 -
                                 meteorite_impact_sec_2 +
                                 fix_structure_sec_2, 0.001), 1.0)
            struct_3_T = min(max(structure_sec_3 -
                                 meteorite_impact_sec_3 +
                                 fix_structure_sec_3, 0.001), 1.0)
            struct_4_T = min(max(structure_sec_4 -
                                 meteorite_impact_sec_4 +
                                 fix_structure_sec_4, 0.001), 1.0)
            struct_5_T = min(max(structure_sec_5 -
                                 meteorite_impact_sec_5 +
                                 fix_structure_sec_5, 0.001), 1.0)

            if isinstance(structure_sec_1, type(struct_1_T)):
                structure_sec_1_new = struct_1_T
            else:
                structure_sec_1_new = struct_1_T.item()
            if isinstance(structure_sec_2, type(struct_2_T)):
                structure_sec_2_new = struct_2_T
            else:
                structure_sec_2_new = struct_2_T.item()
            if isinstance(structure_sec_3, type(struct_3_T)):
                structure_sec_3_new = struct_3_T
            else:
                structure_sec_3_new = struct_3_T.item()
            if isinstance(structure_sec_4, type(struct_4_T)):
                structure_sec_4_new = struct_4_T
            else:
                structure_sec_4_new = struct_4_T.item()
            if isinstance(structure_sec_5, type(struct_5_T)):
                structure_sec_5_new = struct_5_T
            else:
                structure_sec_5_new = struct_5_T.item()

            return structure_sec_1_new, \
                   structure_sec_2_new, \
                   structure_sec_3_new, \
                   structure_sec_4_new, \
                   structure_sec_5_new
    return structure_health
