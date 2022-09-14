"""

Author: Amir Behjat

Date:
    7/12/2022


Make the battery system.

"""


from cdcm import *
from disturbances import *
from battery_design import *
from battery_health import *

import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import time
import pickle
import copy
import os

# from placeholder_handelers.place_holder_handeler import PlaceHolders


class BatterySimulatorTogetherSys:
    def __init__(self):
        np.random.seed(0)

        with System(
            name="everything", description="Everything that goes in the simulation"
        ) as everything:

            # place_holder_0 = PlaceHolders()  # Define the placeholder object
            # Define the placeholder states for coupled systems.
            # place_holder_0.define_place_holder()

            # Make a clock
            clock = make_clock(3600.0)  # 1 Hour

            battery_specs = make_battery_specs()
            disturbances = make_shocks(clock, battery_specs)
            battery_health = make_battery_health(
                clock, battery_specs, disturbances.current_shock.high_current
            )

        self.battery_sys = everything
        # print(everything)

    def show_graph(self):
        battery_sys = self.battery_sys

        g = battery_sys.dag  # original graph
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

        battery_sys = self.battery_sys
        max_steps = 24 * 365 * 10

        dt = battery_sys.clock.dt.value
        t_now = 0
        t_max = max_steps * dt
        tt = time.time()

        print_it = True
        data_to_plot = dict()  # for plotting only
        idx_time = 0  # for plotting only
        while t_now < t_max:
            battery_sys.forward()
            battery_sys.transition()
            data_to_plot[idx_time] = dict()
            if print_it:
                print(2 * "\n")
                print("Time:")
                print("t=", t_now)

            data_to_plot[idx_time]["time"] = battery_sys.clock.t.value / 3600.0
            if print_it:
                print(f"sim_time: " f"{data_to_plot[idx_time]['time']:1.5f}")
            if print_it:
                print("Disturbances:")

            data_to_plot[idx_time][
                "high_current"
            ] = battery_sys.shocks.current_shock.high_current.value
            if print_it:
                print(
                    f"high_current: " f"{data_to_plot[idx_time]['high_current']:1.5f}"
                )
            if print_it:
                print("Battery:")

            data_to_plot[idx_time][
                "battery_degeradation_state"
            ] = (
                battery_sys.battery_health.battery_degerade.battery_degeradation_state.value
            )
            data_to_plot[idx_time][
                "battery_shock_current_state"
            ] = (
                battery_sys.battery_health.battery_shocked.battery_shock_current_state.value
            )
            data_to_plot[idx_time][
                "battery_overal_state"
            ] = battery_sys.battery_health.battery_overal.battery_overal_state.value
            if print_it:
                print(
                    f"battery_degeradation_state: "
                    f"{data_to_plot[idx_time]['battery_degeradation_state']:1.5f},"
                    f"battery_shock_current_state: "
                    f"{data_to_plot[idx_time]['battery_shock_current_state']:1.5f},"
                    f"battery_overal_state: "
                    f"{data_to_plot[idx_time]['battery_overal_state']:1.5f}"
                )

            t_now += dt
            idx_time += 1

        print(time.time() - tt, " Seconds")
        filehandler = open("Battery_sample.pkl", "wb")
        pickle.dump(data_to_plot, filehandler)
        filehandler.close()
        # print(data_to_plot)
        return


np.random.seed(0)
battery_sys = BatterySimulatorTogetherSys()
# battery_sys.show_graph()
battery_sys.simulate()
print("GG-S")
