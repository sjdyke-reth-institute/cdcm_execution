""" The habitat model in the old code remodeled here.

Author: Amir Behjat

Date: 5/25/2022

"""

from cdcm import *
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import time
import pickle
import copy


class habitat_simulator_together_sys():
    def __init__(self):

        # ****************************
        #       All placeholders
        # ****************************
        place_holder_sim_time = copy.deepcopy(make_node(
            "V:place_holder_sim_time", units="sec",  description=""))
        place_holder_dt = copy.deepcopy(make_node(
            "V:place_holder_dt", units="sec",  description=""))

        place_holder_dust_rate = copy.deepcopy(make_node(
            "V:place_holder_dust_rate", units="", description=""))
        place_holder_irradiation = copy.deepcopy(make_node(
            "V:place_holder_irradiation", units="", description=""))
        place_holder_external_temp = copy.deepcopy(make_node(
            "V:place_holder_external_temp", units="K", description=""))

        place_holder_functional_covered = copy.deepcopy(make_node(
            "V:place_holder_functional_covered", units="", description=""))
        place_holder_available_en = copy.deepcopy(make_node(
            "V:place_holder_available_en", units="J", description=""))

        place_holder_en_used_heat = copy.deepcopy(make_node(
            "V:place_holder_en_used_heat", units="J", description=""))
        place_holder_en_needed_heat = copy.deepcopy(make_node(
            "V:place_holder_en_needed_heat", units="J", description=""))
        place_holder_en_used_pres = copy.deepcopy(make_node(
            "V:place_holder_en_used_pres", units="J", description=""))
        place_holder_en_needed_pres = copy.deepcopy(make_node(
            "V:place_holder_en_needed_pres", units="J", description=""))
        place_holder_power_cons = copy.deepcopy(make_node(
            "V:place_holder_power_cons", units="J", description=""))

        place_holder_structure_sec_1 = copy.deepcopy(make_node(
            "V:place_holder_structure_sec_1", units="", description=""))
        place_holder_structure_sec_2 = copy.deepcopy(make_node(
            "V:place_holder_structure_sec_2", units="", description=""))
        place_holder_structure_sec_3 = copy.deepcopy(make_node(
            "V:place_holder_structure_sec_3", units="", description=""))
        place_holder_structure_sec_4 = copy.deepcopy(make_node(
            "V:place_holder_structure_sec_4", units="", description=""))
        place_holder_structure_sec_5 = copy.deepcopy(make_node(
            "V:place_holder_structure_sec_5", units="", description=""))
        place_holder_int_str_temp = copy.deepcopy(make_node(
            "V:place_holder_int_str_temp", units="K", description=""))

        place_holder_int_env_temp = copy.deepcopy(make_node(
            "V:place_holder_int_env_temp", units="K", description=""))
        place_holder_int_env_pres = copy.deepcopy(make_node(
            "V:place_holder_int_env_pres", units="atm", description=""))

        # ****************************
        #       Simulator
        # ****************************

        #       constants
        # ****************************

        #        parameters
        # ****************************

        #       Simulator -> sim_time
        # ****************************
        dt = (make_node("P:dt",
                        value=3600.0,
                        units="second",
                        description="time step"))
        time_noise = (make_node("P:time_noise",
                                value=0.00,
                                units="second",
                                description="STD to measure noise of time"))
        #        states
        # ****************************

        #       Simulator -> sim_time
        # ****************************
        sim_time = (make_node("S:sim_time",
                              value=0.0,
                              units="second",
                              description="sim_time"))

        #         functions
        # ****************************

        @make_function(sim_time)
        def f_sim_time(sim_time_X=sim_time,
                       dt_X=dt):
            """Transition function for sim_time"""
            sim_time_new_X = sim_time_X + dt_X
            return sim_time_new_X

        #         system
        # ****************************
        simulator_sys = (System(
            name="simulator_sys",
            nodes=[sim_time,
                   dt,
                   f_sim_time]
        ))

        # ****************************
        #       disturbance
        # ****************************

        #       constants
        # ****************************

        #       Disturbances -> constants
        # ****************************

        meteorite_df = pd.read_csv("meteorite_impacts.csv")
        samp_meteor_data_impact = meteorite_df['energy'].to_numpy()
        samp_meteor_data_locations = meteorite_df['location'].to_numpy()
        mean_dust_rate_v = 1.0
        std_dust_rate_v = 0.25
        half_day_light_v = 29.5306 * 3600 * 12
        irradiation_max_v = 1450.0
        min_external_temp_v = 100.0
        max_external_temp_v = 400.0
        rate_of_meteor_hit_v = 15 / 1000 / 3600
        # dome_area_ratio = np.array([1 / 6, 1 / 6, 1 / 6, 1 / 6, 1 / 3])
        dome_radious = 2.9
        dome_surface_area_v = (2 * np.pi * np.power(dome_radious, 2))

        #       parameters
        # ****************************

        #       Disturbances -> dust
        # ****************************
        mean_dust_rate = (make_node("P:mean_dust_rate",
                                    value=mean_dust_rate_v,
                                    units="",
                                    description="mean_dust_rate"))
        std_dust_rate = (make_node("P:std_dust_rate",
                                   value=std_dust_rate_v,
                                   units="",
                                   description="std_dust_rate"))

        #       Disturbances -> irradiation
        # ****************************
        half_day_light = (make_node("P:half_day_light",
                                    value=half_day_light_v,
                                    units="sec",
                                    description="half_day_light"))
        irradiation_max = (make_node("P:irradiation_max",
                                     value=irradiation_max_v,
                                     units="W/m^2",
                                     description="irradiation_max"))

        #       Disturbances -> external_temp
        # ****************************
        min_external_temp = (make_node("P:min_external_temp",
                                       value=min_external_temp_v,
                                       units="K",
                                       description="min_external_temp"))
        max_external_temp = (make_node("P:max_external_temp",
                                       value=max_external_temp_v,
                                       units="K",
                                       description="max_external_temp"))

        #       Disturbances -> meteor_impacts
        # ****************************
        meteor_hit_rate = (make_node("P:meteor_hit_rate",
                                     value=rate_of_meteor_hit_v,
                                     units="",
                                     description="meteor_hit_rate"))
        meteor_samp_impact = (make_node("P:meteor_samp_impact",
                                        value=samp_meteor_data_impact,
                                        units="",
                                        description="meteor_samp_impact"))
        meteor_samp_location = (make_node("P:meteor_samp_location",
                                          value=samp_meteor_data_locations,
                                          units="",
                                          description="meteor_samp_location"))
        dome_surface_area = (make_node("P:dome_surface_area",
                                       value=dome_surface_area_v,
                                       units="m^2",
                                       description="dome_surface_area"))

        #        states
        # ****************************

        #       Disturbances -> dust_rate
        # ****************************
        dust_rate = (make_node("S:dust_rate",
                               value=0.0,
                               units="",
                               description="dust_rate"))

        #       Disturbances -> irradiation
        # ****************************
        irradiation = (make_node("S:irradiation",
                                 value=0.0,
                                 units="J/m^2/sec",
                                 description="irradiation"))

        #       Disturbances -> external_temp
        # ****************************
        external_temp = (make_node("S:external_temp",
                                   value=100.0,
                                   units="K",
                                   description="external_temp"))

        #       Disturbances -> meteor_impacts
        # ****************************
        meteor_impacts_1 = (make_node("S:meteor_impacts_1",
                                      value=0.0,
                                      units="",
                                      description="meteor_impacts_1"))
        meteor_impacts_2 = (make_node("S:meteor_impacts_2",
                                      value=0.0,
                                      units="",
                                      description="meteor_impacts_2"))
        meteor_impacts_3 = (make_node("S:meteor_impacts_3",
                                      value=0.0,
                                      units="",
                                      description="meteor_impacts_3"))
        meteor_impacts_4 = (make_node("S:meteor_impacts_4",
                                      value=0.0,
                                      units="",
                                      description="meteor_impacts_4"))
        meteor_impacts_5 = (make_node("S:meteor_impacts_5",
                                      value=0.0,
                                      units="",
                                      description="meteor_impacts_5"))

        #         functions
        # ****************************

        #       Disturbances -> dust_rate
        # ****************************
        @make_function(dust_rate)
        def f_dust_rate(mean_dust_rate_X=mean_dust_rate,
                        std_dust_rate_X=std_dust_rate,
                        sim_time_X=place_holder_sim_time):
            """Transition function for dust_rate"""
            if sim_time_X == 0.0:
                dust_rate_new_X = 0.0
            else:
                dust_rate_new_X = 0.1 * 0.2 * 0.005 * \
                                (mean_dust_rate_X +
                                 std_dust_rate_X * np.random.random())

            return dust_rate_new_X

        #         system
        # ****************************
        #       Disturbances -> dust_rate
        # ****************************

        dust_rate_sys = (System(
            name="dust_rate_sys",
            nodes=[mean_dust_rate,
                   std_dust_rate,
                   place_holder_sim_time,
                   dust_rate,
                   f_dust_rate]
        ))

        #       Disturbances -> irradiation
        # ****************************

        @make_function(irradiation)
        def f_irradiation(half_day_light_X=half_day_light,
                          irradiation_max_X=irradiation_max,
                          sim_time_X=place_holder_sim_time):
            """Transition function for irradiation"""
            if float(sim_time_X) % float(2 *
                                         half_day_light_X) > half_day_light_X:
                irradiation_new_X = 0.0  # night
            else:
                irradiation_new_X = (irradiation_max_X *
                                     np.sin(np.pi * sim_time_X /
                                            half_day_light_X)).item()

            return irradiation_new_X

        #         system
        # ****************************
        #       Disturbances -> irradiation
        # ****************************

        irradiation_sys = (System(
            name="irradiation_sys",
            nodes=[half_day_light,
                   irradiation_max,
                   place_holder_sim_time,
                   irradiation,
                   f_irradiation]
        ))

        #       Disturbances -> external_temp
        # ****************************

        @make_function(external_temp)
        def f_external_temp(half_day_light_X=half_day_light,
                            max_external_temp_X=max_external_temp,
                            min_external_temp_X=min_external_temp,
                            sim_time_X=place_holder_sim_time):
            """Transition function for external_temp"""
            if float(sim_time_X) % float(2 *
                                         half_day_light_X) > half_day_light_X:
                external_temp_new_X = min_external_temp_X  # night
            else:
                external_temp_new_X = ((max_external_temp_X -
                                        min_external_temp_X) *
                                       np.sin(np.pi * sim_time_X /
                                              half_day_light_X) +
                                       min_external_temp_X).item()

            return external_temp_new_X

        #         system
        # ****************************
        #       Disturbances -> external_temp
        # ****************************

        external_temp_sys = (System(
            name="external_temp_sys",
            nodes=[half_day_light,
                   max_external_temp,
                   min_external_temp,
                   place_holder_sim_time,
                   external_temp,
                   f_external_temp]
        ))

        #       Disturbances -> meteor_impacts
        # ****************************
        # @make_function(meteor_impacts)
        @make_function(meteor_impacts_1,
                       meteor_impacts_2,
                       meteor_impacts_3,
                       meteor_impacts_4,
                       meteor_impacts_5)
        def f_meteor_impacts(dome_surface_area_X=dome_surface_area,
                             meteor_hit_rate_X=meteor_hit_rate,
                             meteor_samp_location_X=meteor_samp_location,
                             meteor_samp_impact_X=meteor_samp_impact,
                             sim_time_X=place_holder_sim_time,
                             dt_X=place_holder_dt):
            """Transition function for meteor_impacts"""
            meteor_impacts_new_X = ([0.0, 0.0, 0.0, 0.0, 0.0])

            P_collide_based_on_dome_size = min(max(dome_surface_area_X /
                                                   (2 * np.pi *
                                                    np.power(20, 2)), 0.5), 1)

            np.random.seed(round(sim_time_X / dt_X))
            p_hit = np.random.random()
            if p_hit < meteor_hit_rate_X * P_collide_based_on_dome_size * dt_X:
                p_choice = np.random.randint(10000)
                location_hit = int(meteor_samp_location_X[p_choice] + 1)
                meteor_impacts_new_X[location_hit - 1] = \
                    meteor_samp_impact_X[p_choice]
            if sim_time == 0.0:
                meteor_impacts_new_X = ([0.0, 0.0, 0.0, 0.0, 0.0])
            print('random', np.random.random())

            return meteor_impacts_new_X[0],\
                meteor_impacts_new_X[1],\
                meteor_impacts_new_X[2],\
                meteor_impacts_new_X[3],\
                meteor_impacts_new_X[4]

        #         system
        # ****************************
        #       Disturbances -> meteor_impacts
        # ****************************

        meteor_impacts_sys = (System(
            name="meteor_impacts_sys",
            nodes=[dome_surface_area,
                   meteor_hit_rate,
                   meteor_samp_location,
                   meteor_samp_impact,
                   place_holder_sim_time,
                   place_holder_dt,
                   meteor_impacts_1,
                   meteor_impacts_2,
                   meteor_impacts_3,
                   meteor_impacts_4,
                   meteor_impacts_5,
                   f_meteor_impacts]
        ))

        #         system
        # ****************************
        #       Disturbances -> Combined
        # ****************************

        disturbance_sys = (System(
            name="disturbance_sys",
            nodes=[dust_rate_sys,
                   irradiation_sys,
                   external_temp_sys,
                   meteor_impacts_sys]
        ))

        # ****************************
        #       energy
        # ****************************

        #       constants
        # ****************************

        #       Energy -> constants
        # ****************************
        solar_cell_area_v = 0.08645881805490926
        solar_cell_capacity_v = 0.3
        nuclear_fuel_rate_v = 1.0
        nuclear_capacity_v = 2399.9999999432475
        battery_capacity_v = 7200000.0
        available_en_v = 7200000.0

        # IHM Manual Params ####
        cleaning_panels_v = 0.0 * 0.1
        cleaning_rads_v = 0.0 * 0.07
        covering_panels_v = 1.0

        #       Energy -> parameters
        # ****************************

        #       Energy -> accum_dust_COMBINED
        # ****************************
        cleaning_panels = (make_node("P:cleaning_panels",
                                     value=cleaning_panels_v,
                                     units="m^2/sec",
                                     description="cleaning_panels"))
        cleaning_rads = (make_node("P:cleaning_rads",
                                   value=cleaning_rads_v,
                                   units="m^2/sec",
                                   description="cleaning_rads"))

        #       Energy -> covering_panels_solar
        # ****************************
        covering_panels = (make_node("P:covering_panels",
                                     value=covering_panels_v,
                                     units="",
                                     description="covering_panels"))

        #       Energy -> gen_power_solar
        # ****************************
        solar_cell_area = (make_node("P:solar_cell_area",
                                     value=solar_cell_area_v,
                                     units="J",
                                     description="solar_cell_area"))
        solar_cell_capacity = (make_node("P:solar_cell_capacity",
                                         value=solar_cell_capacity_v,
                                         units="",
                                         description="solar_cell_capacity"))

        #       Energy -> gen_power_nuclear
        # ****************************
        nuclear_fuel_rate = (make_node("P:nuclear_fuel_rate",
                                       value=nuclear_fuel_rate_v,
                                       units="kg/sec",
                                       description="nuclear_fuel_rate"))
        nuclear_capacity = (make_node("P:nuclear_capacity",
                                      value=nuclear_capacity_v,
                                      units="J/kg",
                                      description="nuclear_capacity"))

        #       Energy -> gen_power_total
        # ****************************
        battery_capacity = (make_node("P:battery_capacity",
                                      value=battery_capacity_v,
                                      units="J",
                                      description="battery_capacity"))

        #        states
        # ****************************

        #       Energy -> accum_dust_COMBINED
        # ****************************
        accum_dust_solar = (make_node("S:accum_dust_solar",
                                      value=1.0,
                                      units="",
                                      description="accum_dust_solar"))
        accum_dust_nuclear = (make_node("S:accum_dust_nuclear",
                                        value=1.0,
                                        units="",
                                        description="accum_dust_nuclear"))

        #       Energy -> covering_panels_solar
        # ****************************
        functional_covered = (make_node("S:functional_covered",
                                        value=1.0,
                                        units="",
                                        description="functional_covered"))

        #       Energy -> gen_power_solar
        # ****************************
        gen_power_solar = (make_node("S:gen_power_solar",
                                     value=0.0,
                                     units="J",
                                     description="gen_power_solar"))

        #       Energy -> gen_power_nuclear
        # ****************************
        gen_power_nuclear = (make_node("S:gen_power_nuclear",
                                       value=0.0,
                                       units="J",
                                       description="gen_power_nuclear"))

        #       Energy -> gen_power_total
        # ****************************
        gen_power_total = (make_node("S:gen_power_total",
                                     value=0.0,
                                     units="J",
                                     description="gen_power_total"))

        #       Energy -> available_en
        # ****************************
        available_en = (make_node("S:available_en",
                                  value=available_en_v,
                                  units="J",
                                  description="available_en"))

        #         functions
        # ****************************

        #       Energy -> accum_dust_COMBINED
        # ****************************

        @make_function(accum_dust_solar,
                       accum_dust_nuclear)
        def f_accum_dust(accum_dust_solar_X=accum_dust_solar,
                         accum_dust_nuclear_X=accum_dust_nuclear,
                         cleaning_panels_X=cleaning_panels,
                         cleaning_rads_X=cleaning_rads,
                         dt_X=place_holder_dt,
                         dust_rate_X=place_holder_dust_rate,
                         functional_covered_X=place_holder_functional_covered):
            """Transition function for accum_dust s"""
            accum_dust_solar_new_X = min(max(accum_dust_solar_X +
                                             dt_X * (-dust_rate_X *
                                                     functional_covered_X +
                                                     cleaning_panels_X), 0.0),
                                         1.0)
            accum_dust_nuclear_new_X = min(max(accum_dust_nuclear_X +
                                               dt_X * (-dust_rate_X +
                                                       cleaning_rads_X), 0.0),
                                           1.0)
            return accum_dust_solar_new_X, accum_dust_nuclear_new_X

        #         system
        # ****************************
        #       Energy -> accum_dust_COMBINED
        # ****************************

        accum_dust_sys = (System(
            name="accum_dust_sys",
            nodes=[accum_dust_solar,
                   accum_dust_nuclear,
                   cleaning_panels,
                   cleaning_rads,
                   place_holder_dust_rate,
                   place_holder_dt,
                   place_holder_functional_covered,
                   f_accum_dust]
        ))

        #       Energy -> covering_panels_solar
        # ****************************

        @make_function(functional_covered)
        def f_functional_covered(covering_panels_X=covering_panels):
            """Transition function for covering_panels_solar"""
            functional_covered_new_X = covering_panels_X
            return functional_covered_new_X

        #         system
        # ****************************
        #       Energy -> cover
        # ****************************

        functional_covered_sys = (System(
            name="functional_covered_sys",
            nodes=[covering_panels,
                   functional_covered,
                   f_functional_covered]
        ))

        #       Energy -> gen_power_solar
        # ****************************

        @make_function(gen_power_solar)
        def f_gen_power_solar(accum_dust_solar_X=accum_dust_solar,
                              functional_covered_X=functional_covered,
                              solar_cell_capacity_X=solar_cell_capacity,
                              solar_cell_area_X=solar_cell_area,
                              dt_X=place_holder_dt,
                              irradiation_X=place_holder_irradiation):
            """Transition function for gen_power_solar"""

            gen_power_solar_new_X = max(accum_dust_solar_X *
                                        irradiation_X * functional_covered_X *
                                        solar_cell_capacity_X *
                                        solar_cell_area_X * dt_X, 0.0)
            return gen_power_solar_new_X

        #         system
        # ****************************
        #       Energy -> gen_power_solar
        # ****************************

        gen_power_solar_sys = (System(
            name="gen_power_solar_sys",
            nodes=[accum_dust_solar,
                   functional_covered,
                   solar_cell_capacity,
                   solar_cell_area,
                   place_holder_dt,
                   place_holder_irradiation,
                   gen_power_solar,
                   f_gen_power_solar]
        ))

        #       Energy -> gen_power_nuclear
        # ****************************

        @make_function(gen_power_nuclear)
        def f_gen_power_nuclear(accum_dust_nuclear_X=accum_dust_nuclear,
                                nuclear_capacity_X=nuclear_capacity,
                                nuclear_fuel_rate_X=nuclear_fuel_rate,
                                dt_X=place_holder_dt):
            """Transition function for gen_power_nuclear_new"""
            gen_power_nuclear_new_X = max(accum_dust_nuclear_X *
                                          nuclear_capacity_X,
                                          0.0) * nuclear_fuel_rate_X * dt_X
            return gen_power_nuclear_new_X

        #         system
        # ****************************
        #       Energy -> gen_power_nuclear
        # ****************************

        gen_power_nuclear_sys = (System(
            name="gen_power_nuclear_sys",
            nodes=[accum_dust_nuclear,
                   nuclear_capacity,
                   nuclear_fuel_rate,
                   place_holder_dt,
                   gen_power_nuclear,
                   f_gen_power_nuclear]
        ))

        #       Energy -> gen_power_total
        # ****************************
        @make_function(gen_power_total)
        def f_gen_power_total(gen_power_solar_X=gen_power_solar,
                              gen_power_nuclear_X=gen_power_nuclear):
            """Transition function for gen_power_total"""
            gen_power_total_new_X = gen_power_solar_X + gen_power_nuclear_X
            return gen_power_total_new_X

        #         system
        # ****************************
        #       Energy -> gen_power_total
        # ****************************

        gen_power_total_sys = (System(
            name="gen_power_total_sys",
            nodes=[gen_power_solar,
                   gen_power_nuclear,
                   gen_power_total,
                   f_gen_power_total]
        ))

        #       Energy -> available_en
        # ****************************
        @make_function(available_en)
        def f_available_en(available_en_X=available_en,
                           gen_power_total_X=gen_power_total,
                           battery_capacity_X=battery_capacity,
                           power_cons_X=place_holder_power_cons):
            """Transition function for available_en"""
            available_en_new_X = min(max(0.0, available_en_X +
                                         gen_power_total_X -
                                         power_cons_X),
                                     battery_capacity_X)
            return available_en_new_X

        #         system
        # ****************************
        #       Energy -> available_en
        # ****************************

        available_en_sys = (System(
            name="available_en_sys",
            nodes=[available_en,
                   gen_power_total,
                   battery_capacity,
                   place_holder_power_cons,
                   f_available_en]
        ))

        #         system
        # ****************************
        #       Energy -> Combined
        # ****************************

        energy_sys = (System(
            name="energy_sys",
            nodes=[accum_dust_sys,
                   functional_covered_sys,
                   gen_power_solar_sys,
                   gen_power_nuclear_sys,
                   gen_power_total_sys,
                   available_en_sys]
        ))

        # ****************************
        #       eclss
        # ****************************

        #       constants
        # ****************************

        #       ECLSS -> constants
        # ****************************
        air_heat_capac_v = 1.0035 * 1000
        int_conv_coef_v = 1.0 * 25 * 2
        efficiency_of_TM_v = 12.5
        efficiency_of_PM_v = 31.25
        air_leak_coeficent_v = 10.0 ** (-2)
        pres_capac_per_vol_v = 1.0035 * 1000

        # TEMPORARY CONSTANTS
        # IHM Manual Params ####
        lower_temp_setpo_v = 297.0
        upper_temp_setpo_v = 303.0
        lower_pressure_setpo_v = 0.95
        upper_pressure_setpo_v = 1.05

        #       ECLSS -> parameters
        # ****************************

        #       eclss -> heat
        # ****************************
        lower_temp_setpo = (make_node("P:lower_temp_setpo",
                                      value=lower_temp_setpo_v,
                                      units="K",
                                      description="lower_temp_setpo"))
        upper_temp_setpo = (make_node("P:upper_temp_setpo",
                                      value=upper_temp_setpo_v,
                                      units="K",
                                      description="upper_temp_setpo"))
        air_heat_capac = (make_node("P:air_heat_capac",
                                    value=air_heat_capac_v,
                                    units="J/(kg*K)",
                                    description="air_heat_capac"))
        int_conv_coef = (make_node("P:int_conv_coef",
                                   value=int_conv_coef_v,
                                   units="W/(m^2*K)",
                                   description="int_conv_coef"))
        efficiency_of_TM = (make_node("P:efficiency_of_TM",
                                      value=efficiency_of_TM_v,
                                      units="",
                                      description="efficiency_of_TM"))

        #       eclss -> pres
        # ****************************
        lower_pressure_setpo = (make_node("P:lower_pressure_setpo",
                                          value=lower_pressure_setpo_v,
                                          units="atm",
                                          description="lower_pressure_setpo"))
        upper_pressure_setpo = (make_node("P:upper_pressure_setpo",
                                          value=upper_pressure_setpo_v,
                                          units="atm",
                                          description="upper_pressure_setpo"))
        efficiency_of_PM = (make_node("P:efficiency_of_PM",
                                      value=efficiency_of_PM_v,
                                      units="",
                                      description="efficiency_of_PM"))
        pres_capac_per_vol = (make_node("P:pres_capac_per_vol",
                                        value=pres_capac_per_vol_v,
                                        units="J/atm",
                                        description="pres_capac_per_vol"))
        air_leak_coeficent = (make_node("P:air_leak_coeficent",
                                        value=air_leak_coeficent_v,
                                        units="atm/sec",
                                        description="air_leak_coeficent"))

        #        states
        # ****************************

        #       eclss -> heat
        # ****************************
        en_needed_heat = (make_node("S:en_needed_heat",
                                    value=0.0,
                                    units="J",
                                    description="en_needed_heat"))
        en_used_heat = (make_node("S:en_used_heat",
                                  value=0.0,
                                  units="J",
                                  description="en_used_heat"))

        #       eclss -> pres
        # ****************************
        en_needed_pres = (make_node("S:en_needed_pres",
                                    value=0.0,
                                    units="J",
                                    description="en_needed_pres"))
        en_used_pres = (make_node("S:en_used_pres",
                                  value=0.0,
                                  units="J",
                                  description="en_used_pres"))

        #       eclss -> power consumption
        # ****************************
        power_cons = (make_node("S:power_cons",
                                value=0.0,
                                units="J",
                                description="power_cons"))

        #         functions
        # ****************************

        #       eclss -> heat
        # ****************************

        @make_function(en_needed_heat,
                       en_used_heat)
        def f_eclss_heat(en_needed_heat_X=en_needed_heat,
                         lower_temp_setpo_X=lower_temp_setpo,
                         upper_temp_setpo_X=upper_temp_setpo,
                         air_heat_capac_X=air_heat_capac,
                         int_conv_coef_X=int_conv_coef,
                         efficiency_of_TM_X=efficiency_of_TM,
                         dt_X=place_holder_dt,
                         available_en_X=place_holder_available_en,
                         en_used_pres_X=place_holder_en_used_pres,
                         int_str_temp_X=place_holder_int_str_temp,
                         int_env_temp_X=place_holder_int_env_temp):
            """Transition function for ECLSS heat"""

            en_needed_heat_new_X = abs((((lower_temp_setpo_X +
                                          upper_temp_setpo_X) / 2 -
                                         int_env_temp_X) * air_heat_capac_X -
                                        dt_X * (int_str_temp_X -
                                                int_env_temp_X) *
                                        int_conv_coef_X) / efficiency_of_TM_X)
            en_used_heat_new_X = max(0.0,
                                     min(available_en_X -
                                         en_used_pres_X,
                                         en_needed_heat_X))
            return en_needed_heat_new_X,\
                en_used_heat_new_X

        #         system
        # ****************************
        #       eclss -> heat
        # ****************************

        eclss_heat_sys = (System(
            name="eclss_heat_sys",
            nodes=[en_needed_heat,
                   lower_temp_setpo,
                   upper_temp_setpo,
                   air_heat_capac,
                   int_conv_coef,
                   efficiency_of_TM,
                   place_holder_dt,
                   place_holder_available_en,
                   place_holder_en_used_pres,
                   place_holder_int_env_temp,
                   place_holder_int_str_temp,
                   en_used_heat,
                   f_eclss_heat]
        ))

        #       eclss -> pres
        # ****************************

        @make_function(en_needed_pres,
                       en_used_pres)
        def f_eclss_pres(lower_pressure_setpo_X=lower_pressure_setpo,
                         upper_pressure_setpo_X=upper_pressure_setpo,
                         pres_capac_per_vol_X=pres_capac_per_vol,
                         air_leak_coeficent_X=air_leak_coeficent,
                         efficiency_of_PM_X=efficiency_of_PM,
                         en_needed_pres_X=en_needed_pres,
                         available_en_X=place_holder_available_en,
                         structure_sec_1_X=place_holder_structure_sec_1,
                         structure_sec_2_X=place_holder_structure_sec_2,
                         structure_sec_3_X=place_holder_structure_sec_3,
                         structure_sec_4_X=place_holder_structure_sec_4,
                         structure_sec_5_X=place_holder_structure_sec_5,
                         int_env_pres_X=place_holder_int_env_pres):
            """Transition function for ECLSS heat"""
            latenet_structure_eclss = (structure_sec_1_X +
                                       structure_sec_2_X +
                                       structure_sec_3_X +
                                       structure_sec_4_X +
                                       structure_sec_5_X) / 5
            en_needed_pres_new_X = max(0.0, ((lower_pressure_setpo_X +
                                              upper_pressure_setpo_X) / 2 -
                                             int_env_pres_X) *
                                       pres_capac_per_vol_X + int_env_pres_X *
                                       air_leak_coeficent_X *
                                       ((1 - latenet_structure_eclss) + 0) /
                                       efficiency_of_PM_X)
            en_used_pres_new_X = max(0.0, min(available_en_X,
                                              en_needed_pres_X))
            return en_needed_pres_new_X,\
                en_used_pres_new_X

        #         system
        # ****************************
        #       eclss -> pres
        # ****************************

        eclss_pres_sys = (System(
            name="eclss_pres_sys",
            nodes=[lower_pressure_setpo,
                   upper_pressure_setpo,
                   pres_capac_per_vol,
                   air_leak_coeficent,
                   efficiency_of_PM,
                   en_needed_pres,
                   place_holder_available_en,
                   place_holder_structure_sec_1,
                   place_holder_structure_sec_2,
                   place_holder_structure_sec_3,
                   place_holder_structure_sec_4,
                   place_holder_structure_sec_5,
                   place_holder_int_env_pres,
                   en_used_pres,
                   f_eclss_pres]
        ))

        #       eclss -> power consumption
        # ****************************

        @make_function(power_cons)
        def f_power_consumption(en_used_heat_X=en_used_heat,
                                en_used_pres_X=en_used_pres,
                                available_en_X=place_holder_available_en):
            """Transition function for ECLSS heat"""
            power_cons_new_X = min(available_en_X,
                                   en_used_heat_X +
                                   en_used_pres_X)
            return power_cons_new_X

        #         system
        # ****************************
        #       eclss -> power consumption
        # ****************************

        power_cons_sys = (System(
            name="power_cons_sys",
            nodes=[en_used_heat,
                   en_used_pres,
                   place_holder_available_en,
                   power_cons,
                   f_power_consumption]
        ))

        #         system
        # ****************************
        #       eclss -> Combined
        # ****************************

        eclss_sys = (System(
            name="eclss_sys",
            nodes=[eclss_heat_sys,
                   eclss_pres_sys,
                   power_cons_sys]
        ))

        # ****************************
        #       struct
        # ****************************

        #       constants
        # ****************************

        #       struct -> constants
        # ****************************
        nominal_cond_coef_v = 2.25
        damaged_cond_coef_v = 2.25 * 20.0
        int_conv_coef_v = 1.0 * 25.0 * 2.0
        dom_thickness_v = 0.2
        surf_absorb_coef_v = 0.6
        ext_surf_absorp_v = (5.67 * np.float_power(10, -8))
        surf_emiss_coef_v = 0.9
        ext_surf_emiss_v = (5.67 * np.float_power(10, -8))
        ext_str_temp_v = 100.0
        int_str_temp_v = 320.0
        # TEMPORARY CONSTANTS
        # IHM Manual Params ####
        fix_structure_sec_1_v = 0.0 * 0.01
        fix_structure_sec_2_v = 0.0 * 0.01
        fix_structure_sec_3_v = 0.0 * 0.01
        fix_structure_sec_4_v = 0.0 * 0.01
        fix_structure_sec_5_v = 0.0 * 0.01

        #       struct -> parameters
        # ****************************

        #       struct -> health
        # ****************************
        fix_structure_sec_1 = (make_node("P:fix_structure_sec_1",
                                         value=fix_structure_sec_1_v,
                                         units="",
                                         description="fix_structure_sec_1"))
        fix_structure_sec_2 = (make_node("P:fix_structure_sec_2",
                                         value=fix_structure_sec_2_v,
                                         units="",
                                         description="fix_structure_sec_2"))
        fix_structure_sec_3 = (make_node("P:fix_structure_sec_3",
                                         value=fix_structure_sec_3_v,
                                         units="",
                                         description="fix_structure_sec_3"))
        fix_structure_sec_4 = (make_node("P:fix_structure_sec_4",
                                         value=fix_structure_sec_4_v,
                                         units="",
                                         description="fix_structure_sec_4"))
        fix_structure_sec_5 = (make_node("P:fix_structure_sec_5",
                                         value=fix_structure_sec_5_v,
                                         units="",
                                         description="fix_structure_sec_5"))

        #       struct -> temp
        # ****************************
        nominal_cond_coef = (make_node("P:nominal_cond_coef",
                                       value=nominal_cond_coef_v,
                                       units="W/(m*K)",
                                       description="nominal_cond_coef"))
        damaged_cond_coef = (make_node("P:damaged_cond_coef",
                                       value=damaged_cond_coef_v,
                                       units="W/(m*K)",
                                       description="damaged_cond_coef"))
        dom_thickness = (make_node("P:dom_thickness",
                                   value=dom_thickness_v,
                                   units="m",
                                   description="dom_thickness"))
        surf_absorb_coef = (make_node("P:surf_absorb_coef",
                                      value=surf_absorb_coef_v,
                                      units="",
                                      description="surf_absorb_coef"))
        ext_surf_absorp = (make_node("P:ext_surf_absorp",
                                     value=ext_surf_absorp_v,
                                     units="W/K^4",
                                     description="ext_surf_absorp"))
        surf_emiss_coef = (make_node("P:surf_emiss_coef",
                                     value=surf_emiss_coef_v,
                                     units="",
                                     description="surf_emiss_coef"))
        ext_surf_emiss = (make_node("P:ext_surf_emiss",
                                    value=ext_surf_emiss_v,
                                    units="W/K^4",
                                    description="ext_surf_emiss"))
        int_conv_coef = (make_node("P:int_conv_coef",
                                   value=int_conv_coef_v,
                                   units="W/(m^2*K)",
                                   description="int_conv_coef"))

        #        states
        # ****************************

        #       struct -> health
        # ****************************
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

        #       struct -> temp
        # ****************************
        ext_str_temp = (make_node("S:ext_str_temp",
                                  value=ext_str_temp_v,
                                  units="",
                                  description="ext_str_temp"))
        int_str_temp = (make_node("S:int_str_temp",
                                  value=int_str_temp_v,
                                  units="",
                                  description="int_str_temp"))

        #         functions
        # ****************************

        #       struct -> health
        # ****************************
        @make_function(structure_sec_1,
                       structure_sec_2,
                       structure_sec_3,
                       structure_sec_4,
                       structure_sec_5)
        def f_struct_health(structure_sec_1_X=structure_sec_1,
                            structure_sec_2_X=structure_sec_2,
                            structure_sec_3_X=structure_sec_3,
                            structure_sec_4_X=structure_sec_4,
                            structure_sec_5_X=structure_sec_5,
                            fix_structure_sec_1_X=fix_structure_sec_1,
                            fix_structure_sec_2_X=fix_structure_sec_2,
                            fix_structure_sec_3_X=fix_structure_sec_3,
                            fix_structure_sec_4_X=fix_structure_sec_4,
                            fix_structure_sec_5_X=fix_structure_sec_5,
                            meteor_impacts_1_X=meteor_impacts_1,
                            meteor_impacts_2_X=meteor_impacts_2,
                            meteor_impacts_3_X=meteor_impacts_3,
                            meteor_impacts_4_X=meteor_impacts_4,
                            meteor_impacts_5_X=meteor_impacts_5
                            ):

            """Transition function for f_struct_health"""
            #       struct -> health
            # ****************************

            meteorite_impact_sec_1 = meteor_impacts_1_X  # meteor_impacts[0]
            meteorite_impact_sec_2 = meteor_impacts_2_X  # meteor_impacts[1]
            meteorite_impact_sec_3 = meteor_impacts_3_X  # meteor_impacts[2]
            meteorite_impact_sec_4 = meteor_impacts_4_X  # meteor_impacts[3]
            meteorite_impact_sec_5 = meteor_impacts_5_X  # meteor_impacts[4]

            struct_1_T = min(max(structure_sec_1_X -
                                 meteorite_impact_sec_1 +
                                 fix_structure_sec_1_X, 0.001), 1.0)
            struct_2_T = min(max(structure_sec_2_X -
                                 meteorite_impact_sec_2 +
                                 fix_structure_sec_2_X, 0.001), 1.0)
            struct_3_T = min(max(structure_sec_3_X -
                                 meteorite_impact_sec_3 +
                                 fix_structure_sec_3_X, 0.001), 1.0)
            struct_4_T = min(max(structure_sec_4_X -
                                 meteorite_impact_sec_4 +
                                 fix_structure_sec_4_X, 0.001), 1.0)
            struct_5_T = min(max(structure_sec_5_X -
                                 meteorite_impact_sec_5 +
                                 fix_structure_sec_5_X, 0.001), 1.0)

            if isinstance(structure_sec_1_X, type(struct_1_T)):
                structure_sec_1_new_X = struct_1_T
            else:
                structure_sec_1_new_X = struct_1_T.item()
            if isinstance(structure_sec_2_X, type(struct_2_T)):
                structure_sec_2_new_X = struct_2_T
            else:
                structure_sec_2_new = struct_2_T.item()
            if isinstance(structure_sec_3_X, type(struct_3_T)):
                structure_sec_3_new_X = struct_3_T
            else:
                structure_sec_3_new_X = struct_3_T.item()
            if isinstance(structure_sec_4_X, type(struct_4_T)):
                structure_sec_4_new_X = struct_4_T
            else:
                structure_sec_4_new_X = struct_4_T.item()
            if isinstance(structure_sec_5_X, type(struct_5_T)):
                structure_sec_5_new_X = struct_5_T
            else:
                structure_sec_5_new = struct_5_T.item()

            struct_latent = (structure_sec_1_X +
                             structure_sec_2_X +
                             structure_sec_3_X +
                             structure_sec_4_X +
                             structure_sec_5_X) / 5.0
            return structure_sec_1_new_X, \
                structure_sec_2_new_X, \
                structure_sec_3_new_X, \
                structure_sec_4_new_X, \
                structure_sec_5_new_X

        #         system
        # ****************************
        #       struct -> accum_dust_COMBINED
        # ****************************

        struct_health_sys = (System(
            name="struct_health_sys",
            nodes=[structure_sec_1,
                   structure_sec_2,
                   structure_sec_3,
                   structure_sec_4,
                   structure_sec_5,
                   fix_structure_sec_1,
                   fix_structure_sec_2,
                   fix_structure_sec_3,
                   fix_structure_sec_4,
                   fix_structure_sec_5,
                   meteor_impacts_1,
                   meteor_impacts_2,
                   meteor_impacts_3,
                   meteor_impacts_4,
                   meteor_impacts_5,
                   f_struct_health]
        ))

        #       struct -> temp
        # ****************************

        @make_function(ext_str_temp, int_str_temp)
        def f_struct_temp(ext_str_temp_X=ext_str_temp,
                          int_str_temp_X=int_str_temp,
                          structure_sec_1_X=structure_sec_1,
                          structure_sec_2_X=structure_sec_2,
                          structure_sec_3_X=structure_sec_3,
                          structure_sec_4_X=structure_sec_4,
                          structure_sec_5_X=structure_sec_5,
                          nominal_cond_coef_X=nominal_cond_coef,
                          damaged_cond_coef_X=damaged_cond_coef,
                          dom_thickness_X=dom_thickness,
                          int_conv_coef_X=int_conv_coef,
                          surf_absorb_coef_X=surf_absorb_coef,
                          ext_surf_absorp_X=ext_surf_absorp,
                          surf_emiss_coef_X=surf_emiss_coef,
                          ext_surf_emiss_X=ext_surf_emiss,
                          irradiation_X=place_holder_irradiation,
                          external_temp_X=place_holder_external_temp,
                          int_env_temp_X=place_holder_int_env_temp):
            """Transition function for covering_panels_solar"""
            struct_latent = (structure_sec_1_X +
                             structure_sec_2_X +
                             structure_sec_3_X +
                             structure_sec_4_X +
                             structure_sec_5_X) / 5.0
            ext_str_temp_new_X = ((1.0 * int_str_temp_X *
                                   (0.001 + abs((int_str_temp_X -
                                                 ext_str_temp_X) *
                                                (nominal_cond_coef_X *
                                                 struct_latent +
                                                 damaged_cond_coef_X *
                                                 (1.0 - struct_latent)) /
                                                dom_thickness_X)) +
                                   1.0 * external_temp_X *
                                   (0.001 + abs((irradiation_X +
                                                 np.power(external_temp_X,
                                                          4)) *
                                                surf_absorb_coef_X *
                                                ext_surf_absorp_X -
                                                np.power(ext_str_temp_X, 4) *
                                                surf_emiss_coef_X *
                                                ext_surf_emiss_X))) /
                                  (1.0 * (0.001 + abs((int_str_temp_X -
                                                       ext_str_temp_X) *
                                                      (nominal_cond_coef_X *
                                                       struct_latent +
                                                       damaged_cond_coef_X *
                                                       (1.0 - struct_latent)) /
                                                      dom_thickness_X)) +
                                   1.0 * (0.001 +
                                          abs((irradiation_X +
                                               np.power(external_temp_X, 4)) *
                                              surf_absorb_coef_X *
                                              ext_surf_absorp_X -
                                              np.power(ext_str_temp_X, 4) *
                                              surf_emiss_coef_X *
                                              ext_surf_emiss_X)))).item()
            # ext_str_temp_new = 320.0
            int_str_temp_new_X = (1.0 * ext_str_temp_X *
                                  (nominal_cond_coef_X * struct_latent +
                                   damaged_cond_coef_X *
                                   (1.0 - struct_latent)) /
                                  dom_thickness_X + 1.0 * int_env_temp_X *
                                  int_conv_coef_X) / (1.0 *
                                                      (nominal_cond_coef_X *
                                                       struct_latent +
                                                       damaged_cond_coef_X *
                                                       (1.0 - struct_latent)) /
                                                      dom_thickness_X +
                                                      1.0 * int_conv_coef_X)
            # int_str_temp_new = 320.0
            return ext_str_temp_new_X,\
                int_str_temp_new_X

        #         system
        # ****************************
        #       struct -> temp
        # ****************************

        struct_temp_sys = (System(
            name="struct_temp_sys",
            nodes=[ext_str_temp,
                   int_str_temp,
                   structure_sec_1,
                   structure_sec_2,
                   structure_sec_3,
                   structure_sec_4,
                   structure_sec_5,
                   nominal_cond_coef,
                   damaged_cond_coef,
                   dom_thickness,
                   int_conv_coef,
                   surf_absorb_coef,
                   ext_surf_absorp,
                   surf_emiss_coef,
                   ext_surf_emiss,
                   place_holder_irradiation,
                   place_holder_external_temp,
                   place_holder_int_env_temp,
                   f_struct_temp]
        ))

        #         system
        # ****************************
        #       struct -> Combined
        # ****************************

        struct_sys = (System(
            name="struct_sys",
            nodes=[struct_health_sys,
                   struct_temp_sys]
        ))

        # ****************************
        #       interior environment
        # ****************************

        #       constants
        # ****************************

        #       interior_env -> CONSTANTS
        # ****************************

        out_of_str_pres_v = 0.0
        int_env_temp_v = 298.0
        int_env_pres_v = 1.0
        air_leak_coeficent_v = 10.0 ** (-2)

        # IHM Manual Params ####
        lower_temp_setpo_v = 297.0
        upper_temp_setpo_v = 303.0
        lower_pressure_setpo_v = 0.95
        upper_pressure_setpo_v = 1.05

        #       interior_env -> parameters
        # ****************************

        #       interior_env -> temp
        # ****************************
        lower_temp_setpo = (make_node("P:lower_temp_setpo",
                                      value=lower_temp_setpo_v,
                                      units="K",
                                      description="lower_temp_setpo"))
        upper_temp_setpo = (make_node("P:upper_temp_setpo",
                                      value=upper_temp_setpo_v,
                                      units="K",
                                      description="upper_temp_setpo"))

        #       interior_env -> pres
        # ****************************
        lower_pressure_setpo = (make_node("P:lower_pressure_setpo",
                                          value=lower_pressure_setpo_v,
                                          units="atm",
                                          description="lower_pressure_setpo"))
        upper_pressure_setpo = (make_node("P:upper_pressure_setpo",
                                          value=upper_pressure_setpo_v,
                                          units="atm",
                                          description="upper_pressure_setpo"))
        out_of_str_pres = (make_node("P:out_of_str_pres",
                                     value=out_of_str_pres_v,
                                     units="atm",
                                     description="out_of_str_pres"))
        air_leak_coeficent = (make_node("P:air_leak_coeficent",
                                        value=air_leak_coeficent_v,
                                        units="atm/sec",
                                        description="air_leak_coeficent"))

        #        states
        # ****************************

        #       interior_env -> temp
        # ****************************
        int_env_temp = (make_node("S:int_env_temp",
                                  value=int_env_temp_v,
                                  units="K",
                                  description="int_env_temp"))

        #       interior_env -> pres
        # ****************************
        int_env_pres = (make_node("S:int_env_pres",
                                  value=int_env_pres_v,
                                  units="atm",
                                  description="int_env_pres"))

        #         functions
        # ****************************

        #       interior_env -> heat
        # ****************************

        @make_function(int_env_temp)
        def f_interior_env_heat(lower_temp_setpo_X=lower_temp_setpo,
                                upper_temp_setpo_X=upper_temp_setpo,
                                en_used_heat_X=place_holder_en_used_heat,
                                en_needed_heat_X=place_holder_en_needed_heat,
                                int_str_temp_X=place_holder_int_str_temp):
            """Transition function for interior_env heat"""
            int_env_temp_new_X = max(100.0,
                                     min(400.0,
                                         1.0 * (min(1.0,
                                                    max(en_used_heat_X,
                                                        1 * 10 ** (-4)) /
                                                    max(en_needed_heat_X,
                                                        1 * 10 ** (-4)))) *
                                         ((lower_temp_setpo_X +
                                           upper_temp_setpo_X) / 2) + 1.0 *
                                         (1 - min(1.0,
                                                  (max(en_used_heat_X,
                                                       1 * 10 ** (-4)) /
                                                   max(en_needed_heat_X,
                                                       1 * 10 ** (-4))))) *
                                         int_str_temp_X))
            return int_env_temp_new_X

        #         system
        # ****************************
        #       interior_env -> heat
        # ****************************

        interior_env_heat_sys = (System(
            name="interior_env_heat_sys",
            nodes=[lower_temp_setpo,
                   upper_temp_setpo,
                   place_holder_en_used_heat,
                   place_holder_en_needed_heat,
                   place_holder_int_str_temp,
                   int_env_temp,
                   f_interior_env_heat]
        ))

        #       interior_env -> pres
        # ****************************

        @make_function(int_env_pres)
        def f_interior_env_pres(lower_pressure_setpo_X=lower_pressure_setpo,
                                upper_pressure_setpo_X=upper_pressure_setpo,
                                air_leak_coeficent_X=air_leak_coeficent,
                                out_of_str_pres_X=out_of_str_pres,
                                structure_sec_1_X=place_holder_structure_sec_1,
                                structure_sec_2_X=place_holder_structure_sec_2,
                                structure_sec_3_X=place_holder_structure_sec_3,
                                structure_sec_4_X=place_holder_structure_sec_4,
                                structure_sec_5_X=place_holder_structure_sec_5,
                                en_used_pres_X=place_holder_en_used_pres,
                                en_needed_pres_X=place_holder_en_needed_pres):

            """Transition function for interior_env heat"""
            latent_struct_int_env = (structure_sec_1_X +
                                     structure_sec_2_X +
                                     structure_sec_3_X +
                                     structure_sec_4_X +
                                     structure_sec_5_X) / 5
            int_env_pres_new_X = max(0.0, min(1.0,
                                              max(en_used_pres_X,
                                                  1 * 10 ** (-4)) /
                                              max(en_needed_pres_X,
                                                  1 * 10 ** (-4))) *
                                     ((lower_pressure_setpo_X +
                                       upper_pressure_setpo_X) / 2) +
                                     (1 - min(1.0, max(en_used_pres_X,
                                                       1 * 10 ** (-4)) /
                                              max(en_needed_pres_X,
                                                  1 * 10 ** (-4)))) *
                                     (((1 - latent_struct_int_env) *
                                       air_leak_coeficent_X + 0) *
                                      out_of_str_pres_X))
            return int_env_pres_new_X

        #         system
        # ****************************
        #       interior_env -> heat
        # ****************************

        interior_env_pres_sys = (System(
            name="interior_env_pres_sys",
            nodes=[lower_pressure_setpo,
                   upper_pressure_setpo,
                   air_leak_coeficent,
                   out_of_str_pres,
                   place_holder_structure_sec_1,
                   place_holder_structure_sec_2,
                   place_holder_structure_sec_3,
                   place_holder_structure_sec_4,
                   place_holder_structure_sec_5,
                   place_holder_en_used_pres,
                   place_holder_en_needed_pres,
                   int_env_pres,
                   f_interior_env_pres]
        ))

        #         system
        # ****************************
        #       interior_env -> Combined
        # ****************************

        interior_env_sys = (System(
            name="interior_env_sys",
            nodes=[interior_env_heat_sys, interior_env_pres_sys]
        ))

        # ****************************
        #   place_holder corrections
        # ****************************

        replace(place_holder_sim_time, sim_time)
        replace(place_holder_dt, dt)

        replace(place_holder_dust_rate, dust_rate)
        replace(place_holder_irradiation, irradiation)
        replace(place_holder_external_temp, external_temp)
        # replace(place_holder_meteor_impacts, meteor_impacts)

        replace(place_holder_available_en, available_en)
        replace(place_holder_functional_covered, functional_covered)

        replace(place_holder_en_used_heat, en_used_heat)
        replace(place_holder_en_needed_heat, en_needed_heat)
        replace(place_holder_en_used_pres, en_used_pres)
        replace(place_holder_en_needed_pres, en_needed_pres)
        replace(place_holder_power_cons, power_cons)

        replace(place_holder_structure_sec_1, structure_sec_1)
        replace(place_holder_structure_sec_2, structure_sec_2)
        replace(place_holder_structure_sec_3, structure_sec_3)
        replace(place_holder_structure_sec_4, structure_sec_4)
        replace(place_holder_structure_sec_5, structure_sec_5)
        replace(place_holder_int_str_temp, int_str_temp)

        replace(place_holder_int_env_temp, int_env_temp)
        replace(place_holder_int_env_pres, int_env_pres)

        # ****************************
        #   combines
        # ****************************

        self.hab_sys = (System(
            name="sys_all",
            nodes=[simulator_sys,
                   disturbance_sys,
                   energy_sys,
                   eclss_sys,
                   struct_sys,
                   interior_env_sys]
        ))
        return

    def show_graph(self):
        hab_sys = self.hab_sys

        g = hab_sys.dag  # original graph
        g_clean = nx.empty_graph(0, create_using=nx.DiGraph())
        list_to_add_nodes = []
        list_to_add_edges = []
        for v in g.nodes:
            if not(isinstance(v, str)):
                if not('place_holder' in v.name):
                    list_to_add_nodes.append(v.name)
                    for e in g.edges(v):
                        if not(isinstance(e[0], str)):
                            name_node_e_0 = e[0].name
                        else:
                            name_node_e_0 = e[0]
                        if not(isinstance(e[1], str)):
                            name_node_e_1 = e[1].name
                        else:
                            name_node_e_1 = e[1]
                        list_to_add_edges.append((name_node_e_0,
                                                  name_node_e_1))
            else:
                if not('place_holder' in v):
                    list_to_add_nodes.append(v)
                    for e in g.edges(v):
                        if not(isinstance(e[0], str)):
                            name_node_e_0 = e[0].name
                        else:
                            name_node_e_0 = e[0]
                        if not(isinstance(e[1], str)):
                            name_node_e_1 = e[1].name
                        else:
                            name_node_e_1 = e[1]
                        list_to_add_edges.append((name_node_e_0,
                                                  name_node_e_1))

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
                print(2 * '\n')
                print('Time:')
                print('t=', t_now)
                data_to_plot[idx_time]['time'] =\
                    hab_sys.simulator_sys.\
                    sim_time.value

                print(f"sim_time: "
                      f"{data_to_plot[idx_time]['time']:1.5f}")

                print('Disturbances:')
                data_to_plot[idx_time]['dust'] =\
                    hab_sys.disturbance_sys.\
                    dust_rate_sys.dust_rate.value
                data_to_plot[idx_time]['irradiation'] =\
                    hab_sys.disturbance_sys.\
                    irradiation_sys.irradiation.value
                data_to_plot[idx_time]['external_temp'] =\
                    hab_sys.disturbance_sys.\
                    external_temp_sys.external_temp.value
                data_to_plot[idx_time]['meteor_impacts_1'] =\
                    hab_sys.disturbance_sys.\
                    meteor_impacts_sys.meteor_impacts_1.value
                data_to_plot[idx_time]['meteor_impacts_2'] = \
                    hab_sys.disturbance_sys.\
                    meteor_impacts_sys.meteor_impacts_2.value
                data_to_plot[idx_time]['meteor_impacts_3'] = \
                    hab_sys.disturbance_sys.\
                    meteor_impacts_sys.meteor_impacts_3.value
                data_to_plot[idx_time]['meteor_impacts_4'] = \
                    hab_sys.disturbance_sys.\
                    meteor_impacts_sys.meteor_impacts_4.value
                data_to_plot[idx_time]['meteor_impacts_5'] = \
                    hab_sys.disturbance_sys.\
                    meteor_impacts_sys.meteor_impacts_5.value

                print(f"dust_rate: "
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

                print('Energies:')
                data_to_plot[idx_time]['accum_dust_solar'] =\
                    hab_sys.energy_sys.\
                    accum_dust_sys.accum_dust_solar.value
                data_to_plot[idx_time]['accum_dust_nuclear'] =\
                    hab_sys.energy_sys.\
                    accum_dust_sys.accum_dust_nuclear.value
                data_to_plot[idx_time]['functional_covered'] =\
                    hab_sys.energy_sys.\
                    functional_covered_sys.functional_covered.value
                data_to_plot[idx_time]['gen_power_solar'] =\
                    hab_sys.energy_sys.\
                    gen_power_solar_sys.gen_power_solar.value
                data_to_plot[idx_time]['gen_power_nuclear'] =\
                    hab_sys.energy_sys.\
                    gen_power_nuclear_sys.gen_power_nuclear.value
                data_to_plot[idx_time]['gen_power_total'] =\
                    hab_sys.energy_sys.\
                    gen_power_total_sys.gen_power_total.value
                data_to_plot[idx_time]['available_en'] =\
                    hab_sys.energy_sys.\
                    available_en_sys.available_en.value

                print(f"accum_dust_solar:"
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
                      f"{data_to_plot[idx_time]['available_en']:1.5f},")

                print('ECLSS:')
                data_to_plot[idx_time]['en_needed_heat'] =\
                    hab_sys.eclss_sys.\
                    eclss_heat_sys.en_needed_heat.value
                data_to_plot[idx_time]['en_used_heat'] =\
                    hab_sys.eclss_sys.\
                    eclss_heat_sys.en_used_heat.value
                data_to_plot[idx_time]['en_needed_pres'] =\
                    hab_sys.eclss_sys.\
                    eclss_pres_sys.en_needed_pres.value
                data_to_plot[idx_time]['en_used_pres'] =\
                    hab_sys.eclss_sys.\
                    eclss_pres_sys.en_used_pres.value
                data_to_plot[idx_time]['power_cons'] =\
                    hab_sys.eclss_sys.\
                    power_cons_sys.power_cons.value

                print(f"en_needed_heat:"
                      f"{data_to_plot[idx_time]['en_needed_heat']:1.5f},"
                      f"en_used_heat:"
                      f"{data_to_plot[idx_time]['en_used_heat']:1.5f},"
                      f"en_needed_pres:"
                      f"{data_to_plot[idx_time]['en_needed_pres']:1.5f},"
                      f"en_used_pres:"
                      f"{data_to_plot[idx_time]['en_used_pres']:1.5f},"
                      f"power_cons:"
                      f"{data_to_plot[idx_time]['power_cons']:1.5f},")

                print('Struct:')
                data_to_plot[idx_time]['structure_sec_1'] =\
                    hab_sys.struct_sys.\
                    struct_health_sys.structure_sec_1.value
                data_to_plot[idx_time]['structure_sec_2'] =\
                    hab_sys.struct_sys.\
                    struct_health_sys.structure_sec_2.value
                data_to_plot[idx_time]['structure_sec_3'] =\
                    hab_sys.struct_sys.\
                    struct_health_sys.structure_sec_3.value
                data_to_plot[idx_time]['structure_sec_4'] =\
                    hab_sys.struct_sys.\
                    struct_health_sys.structure_sec_4.value
                data_to_plot[idx_time]['structure_sec_5'] =\
                    hab_sys.struct_sys.\
                    struct_health_sys.structure_sec_5.value
                data_to_plot[idx_time]['ext_str_temp'] =\
                    hab_sys.struct_sys.\
                    struct_temp_sys.ext_str_temp.value
                data_to_plot[idx_time]['int_str_temp'] =\
                    hab_sys.struct_sys.\
                    struct_temp_sys.int_str_temp.value

                print(f"structure_sec_1:"
                      f"{data_to_plot[idx_time]['structure_sec_1']:1.5f},"
                      f"structure_sec_2:"
                      f"{data_to_plot[idx_time]['structure_sec_2']:1.5f},"
                      f"structure_sec_3:"
                      f"{data_to_plot[idx_time]['structure_sec_3']:1.5f},"
                      f"structure_sec_4:"
                      f"{data_to_plot[idx_time]['structure_sec_4']:1.5f},"
                      f"structure_sec_5:"
                      f"{data_to_plot[idx_time]['structure_sec_5']:1.5f},"
                      f"ext_str_temp:"
                      f"{data_to_plot[idx_time]['ext_str_temp']:1.5f},"
                      f"int_str_temp:"
                      f"{data_to_plot[idx_time]['int_str_temp']:1.5f},")

                print('Interior Environment:')
                data_to_plot[idx_time]['int_env_temp'] =\
                    hab_sys.interior_env_sys.\
                    interior_env_heat_sys.int_env_temp.value
                data_to_plot[idx_time]['int_env_pres'] =\
                    hab_sys.interior_env_sys.\
                    interior_env_pres_sys.int_env_pres.value

                print(f"int_env_temp:"
                      f"{data_to_plot[idx_time]['int_env_temp']:1.5f},"
                      f"int_env_pres:"
                      f"{data_to_plot[idx_time]['int_env_pres']:1.5f},")

            t_now += dt
            idx_time += 1

        print(time.time() - tt, " Seconds")
        filehandler = open("newest_NEW_sample.pkl", "wb")
        pickle.dump(data_to_plot, filehandler)
        filehandler.close()
        return


hab_sys = habitat_simulator_together_sys()
hab_sys.show_graph()
hab_sys.simulate()
print('GG')
