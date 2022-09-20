"""
Make the entire system.

"""


from cdcm import *
from disturbances import *
from dome_design import *
from habitat_energy import *
from habitat_eclss import *
from habitat_structure import *
from habitat_int_env import *

import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import time
import pickle
import copy

from placeholder_handelers.place_holder_handeler import place_holders


class habitat_simulator_together_sys:
    def __init__(self):
        path_data_files = "./data_files/"

        with System(
            name="everything", description="Everything that goes in the simulation"
        ) as everything:

            place_holder_0 = place_holders()
            place_holder_0.define_place_holder()

            # Make a clock
            clock = make_clock(3600.0)

            dome_specs = make_dome_specs()
            moon = make_moon(path_data_files, clock, dome_specs)
            energy = make_energy(
                clock,
                moon,
                place_holder_0.place_holder_energy_cons,
                place_holder_0.place_holder_agent_clean_panel,
                place_holder_0.place_holder_agent_clean_plant,
                place_holder_0.place_holder_HM_cover_panel,
            )
            # # energy = make_energy(clock, moon)
            # # print(place_holder_0.place_holder_struct_health)
            eclss = make_eclss(
                clock,
                dome_specs,
                energy_available_energy=place_holder_0.place_holder_available_en,
                struct_health=place_holder_0.place_holder_struct_health,
                struct_inside_temperature=place_holder_0.place_holder_int_str_temp,
                interior_env_temperature=place_holder_0.place_holder_int_env_temp,
                int_env_pres=place_holder_0.place_holder_int_env_pres,
                HM_temperature_lower_setpoint=place_holder_0.place_holder_HM_pressure_lower_setpoint,
                HM_temperature_upper_setpoint=place_holder_0.place_holder_HM_pressure_upper_setpoint,
                HM_pressure_lower_setpoint=place_holder_0.place_holder_HM_pressure_lower_setpoint,
                HM_pressure_upper_setpoint=place_holder_0.place_holder_HM_pressure_upper_setpoint,
            )
            # # eclss = make_eclss(clock, dome_specs)
            struct = make_structure(
                moon,
                dome_specs,
                place_holder_0.place_holder_int_env_temp,
                place_holder_0.place_holder_agent_repair_struct,
            )
            # # struct = make_structure(moon, dome_specs)
            int_env = make_int_env(
                dome_specs,
                eclss_en_used_heat=place_holder_0.place_holder_en_used_heat,
                eclss_en_needed_heat=place_holder_0.place_holder_en_needed_heat,
                eclss_en_used_pres=place_holder_0.place_holder_en_used_pres,
                eclss_en_needed_pres=place_holder_0.place_holder_en_needed_pres,
                struct_health=place_holder_0.place_holder_struct_health,
                struct_inside_temperature=place_holder_0.place_holder_int_str_temp,
                HM_temperature_lower_setpoint=place_holder_0.place_holder_HM_pressure_lower_setpoint,
                HM_temperature_upper_setpoint=place_holder_0.place_holder_HM_pressure_upper_setpoint,
                HM_pressure_lower_setpoint=place_holder_0.place_holder_HM_pressure_lower_setpoint,
                HM_pressure_upper_setpoint=place_holder_0.place_holder_HM_pressure_upper_setpoint,
            )
            # int_env = make_int_env(dome_specs)
        # input('placeholdings')
        everything = place_holder_0.replace_place_holder(everything)
        self.hab_sys = everything
        # print(everything)

    def show_graph(self):
        hab_sys = self.hab_sys

        g = hab_sys.dag  # original graph
        g_clean = nx.empty_graph(0, create_using=nx.DiGraph())
        list_to_add_nodes = []
        list_to_add_edges = []
        for v in g.nodes:
            if not (isinstance(v, str)):
                if not ("place_holder" in v.name):
                    list_to_add_nodes.append(v.name)
                    for e in g.edges(v):
                        if not (isinstance(e[0], str)):
                            name_node_e_0 = e[0].name
                        else:
                            name_node_e_0 = e[0]
                        if not (isinstance(e[1], str)):
                            name_node_e_1 = e[1].name
                        else:
                            name_node_e_1 = e[1]
                        list_to_add_edges.append((name_node_e_0, name_node_e_1))
            else:
                if not ("place_holder" in v):
                    list_to_add_nodes.append(v)
                    for e in g.edges(v):
                        if not (isinstance(e[0], str)):
                            name_node_e_0 = e[0].name
                        else:
                            name_node_e_0 = e[0]
                        if not (isinstance(e[1], str)):
                            name_node_e_1 = e[1].name
                        else:
                            name_node_e_1 = e[1]
                        list_to_add_edges.append((name_node_e_0, name_node_e_1))

        for v in list_to_add_nodes:
            g_clean.add_node(v)
        for e in list_to_add_edges:
            g_clean.add_edges_from([e])

        nx.draw(g_clean, with_labels=True)  # remove graphviz in windows
        plt.show()
        return

    def simulate(self):

        hab_sys = self.hab_sys

        dt = 3600
        t_now = 0
        t_max = 100 * 3600
        tt = time.time()
        np.random.seed(0)
        print_it = True
        data_to_plot = dict()  # for plottig only
        idx_time = 0  # for plottig only
        while t_now < t_max:
            hab_sys.forward()
            hab_sys.transition()
            data_to_plot[idx_time] = dict()
            if print_it:
                print(2 * "\n")
                print("Time:")
                print("t=", t_now)
                data_to_plot[idx_time]["time"] = hab_sys.clock.t.value

                print(f"sim_time: " f"{data_to_plot[idx_time]['time']:1.5f}")

                print("Disturbances:")
                data_to_plot[idx_time]["dust"] = hab_sys.moon.dust.dust_rate.value
                data_to_plot[idx_time][
                    "irradiation"
                ] = hab_sys.moon.radiation.irradiance.value
                data_to_plot[idx_time][
                    "external_temp"
                ] = hab_sys.moon.thermal.surface_temperature.value
                data_to_plot[idx_time][
                    "meteor_impacts_1"
                ] = hab_sys.moon.meteor.meteor_impacts_1.value
                data_to_plot[idx_time][
                    "meteor_impacts_2"
                ] = hab_sys.moon.meteor.meteor_impacts_2.value
                data_to_plot[idx_time][
                    "meteor_impacts_3"
                ] = hab_sys.moon.meteor.meteor_impacts_3.value
                data_to_plot[idx_time][
                    "meteor_impacts_4"
                ] = hab_sys.moon.meteor.meteor_impacts_4.value
                data_to_plot[idx_time][
                    "meteor_impacts_5"
                ] = hab_sys.moon.meteor.meteor_impacts_5.value

                print(
                    f"dust_rate: "
                    f"{data_to_plot[idx_time]['dust']:1.5f},"
                    f" irradiation: "
                    f"{data_to_plot[idx_time]['irradiation']:1.5f},"
                    f" external_temp :"
                    f"{data_to_plot[idx_time]['external_temp']:1.5f},"
                    f"meteor_impacts_1: "
                    f"{data_to_plot[idx_time]['meteor_impacts_1']:1.5f},"
                    f" meteor_impacts_2: "
                    f"{data_to_plot[idx_time]['meteor_impacts_2']:1.5f},"
                    f" meteor_impacts_3: "
                    f"{data_to_plot[idx_time]['meteor_impacts_3']:1.5f},"
                    f" meteor_impacts_4: "
                    f"{data_to_plot[idx_time]['meteor_impacts_4']:1.5f},"
                    f" meteor_impacts_5: "
                    f"{data_to_plot[idx_time]['meteor_impacts_5']:1.5f}"
                )

                print("Energies:")
                data_to_plot[idx_time][
                    "accum_dust_solar"
                ] = hab_sys.energy.energy_performance.accum_dust_solar.value
                data_to_plot[idx_time][
                    "accum_dust_nuclear"
                ] = hab_sys.energy.energy_performance.accum_dust_nuclear.value
                data_to_plot[idx_time][
                    "functional_covered"
                ] = hab_sys.energy.energy_performance.functional_covered.value
                data_to_plot[idx_time][
                    "gen_power_solar"
                ] = hab_sys.energy.energy_generate.gen_energy_solar.value
                data_to_plot[idx_time][
                    "gen_power_nuclear"
                ] = hab_sys.energy.energy_generate.gen_energy_nuclear.value
                data_to_plot[idx_time][
                    "gen_power_total"
                ] = hab_sys.energy.energy_generate.gen_energy_total.value
                data_to_plot[idx_time][
                    "available_en"
                ] = hab_sys.energy.energy_store.available_en.value

                print(
                    f"accum_dust_solar:"
                    f"{data_to_plot[idx_time]['accum_dust_solar']:1.5f},"
                    f"accum_dust_nuclear:"
                    f"{data_to_plot[idx_time]['accum_dust_nuclear']:1.5f},"
                    f"functional_covered:"
                    f"{data_to_plot[idx_time]['functional_covered']:1.5f},"
                    f"gen_power_solar:"
                    f"{data_to_plot[idx_time]['gen_power_solar']:1.5f},"
                    f"gen_power_nuclear:"
                    f"{data_to_plot[idx_time]['gen_power_nuclear']:1.5f},"
                    f"gen_power_total:"
                    f"{data_to_plot[idx_time]['gen_power_total']:1.5f},"
                    f"available_en:"
                    f"{data_to_plot[idx_time]['available_en']:1.5f},"
                )

                print("ECLSS:")
                data_to_plot[idx_time][
                    "en_needed_heat"
                ] = hab_sys.eclss.eclss_temperature.en_needed_heat.value
                data_to_plot[idx_time][
                    "en_used_heat"
                ] = hab_sys.eclss.eclss_temperature.en_used_heat.value
                data_to_plot[idx_time][
                    "en_needed_pres"
                ] = hab_sys.eclss.eclss_pressure.en_needed_pres.value
                data_to_plot[idx_time][
                    "en_used_pres"
                ] = hab_sys.eclss.eclss_pressure.en_used_pres.value
                data_to_plot[idx_time][
                    "power_cons"
                ] = hab_sys.eclss.eclss_energy_consumption.energy_cons.value

                print(
                    f"en_needed_heat:"
                    f"{data_to_plot[idx_time]['en_needed_heat']:1.5f},"
                    f"en_used_heat:"
                    f"{data_to_plot[idx_time]['en_used_heat']:1.5f},"
                    f"en_needed_pres:"
                    f"{data_to_plot[idx_time]['en_needed_pres']:1.5f},"
                    f"en_used_pres:"
                    f"{data_to_plot[idx_time]['en_used_pres']:1.5f},"
                    f"power_cons:"
                    f"{data_to_plot[idx_time]['power_cons']:1.5f},"
                )

                # print('Struct:')
                # print('hab_sys.struct.struct_health', hab_sys.struct.struct_health)
                #
                # print('hab_sys.struct.struct_health.structure_secs.value', hab_sys.struct.struct_health.structure_secs.value)
                # input('sdasdasdasdasd')
                # data_to_plot[idx_time]['structure_sec_1'] =\
                #     hab_sys.struct.struct_health.structure_secs[0].value
                # data_to_plot[idx_time]['structure_sec_2'] =\
                #     hab_sys.struct.struct_health.structure_secs[1].value
                # data_to_plot[idx_time]['structure_sec_3'] =\
                #     hab_sys.struct.struct_health.structure_secs[2].value
                # data_to_plot[idx_time]['structure_sec_4'] =\
                #     hab_sys.struct.struct_health.structure_secs[3].value
                # data_to_plot[idx_time]['structure_sec_5'] =\
                #     hab_sys.struct.struct_health.structure_secs[4].value
                # data_to_plot[idx_time]['ext_str_temp'] =\
                #     hab_sys.struct.struct_temp.ext_str_temp.value
                # data_to_plot[idx_time]['int_str_temp'] =\
                #     hab_sys.struct.struct_temp.int_str_temp.value
                #
                # print(f"structure_sec_1:"
                #       f"{data_to_plot[idx_time]['structure_sec_1']:1.5f},"
                #       f"structure_sec_2:"
                #       f"{data_to_plot[idx_time]['structure_sec_2']:1.5f},"
                #       f"structure_sec_3:"
                #       f"{data_to_plot[idx_time]['structure_sec_3']:1.5f},"
                #       f"structure_sec_4:"
                #       f"{data_to_plot[idx_time]['structure_sec_4']:1.5f},"
                #       f"structure_sec_5:"
                #       f"{data_to_plot[idx_time]['structure_sec_5']:1.5f},"
                #       f"ext_str_temp:"
                #       f"{data_to_plot[idx_time]['ext_str_temp']:1.5f},"
                #       f"int_str_temp:"
                #       f"{data_to_plot[idx_time]['int_str_temp']:1.5f},")
                #
                # print('Interior Environment:')
                # data_to_plot[idx_time]['int_env_temp'] =\
                #     hab_sys.int_env.int_env_temperature.int_env_temp.value
                # data_to_plot[idx_time]['int_env_pres'] =\
                #     hab_sys.int_env.int_env_pressure.int_env_pres.value
                #
                # print(f"int_env_temp:"
                #       f"{data_to_plot[idx_time]['int_env_temp']:1.5f},"
                #       f"int_env_pres:"
                #       f"{data_to_plot[idx_time]['int_env_pres']:1.5f},")

            t_now += dt
            idx_time += 1

        print(time.time() - tt, " Seconds")
        filehandler = open("newest_NEW_sample.pkl", "wb")
        pickle.dump(data_to_plot, filehandler)
        filehandler.close()
        return


hab_sys = habitat_simulator_together_sys()
# hab_sys.show_graph()
hab_sys.simulate()
print("GG-S")
