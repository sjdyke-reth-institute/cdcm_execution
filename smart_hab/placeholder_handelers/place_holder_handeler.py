"""
Makes the place_holders as a class
Two methods:
    1) Define the place holders
    2) Replace the place holders

"""


from cdcm import *
import inspect


class place_holders():
    """
    Make make_place_holders

    Arguments

    """

    def __init__(self):

        return

    def define_place_holder(self):

        self.place_holder_sim_time = make_node(
            "V:place_holder_sim_time", units="sec", description="")
        self.place_holder_dt = make_node(
            "V:place_holder_dt", units="sec", description="")

        self.place_holder_dust_rate = make_node(
            "V:place_holder_dust_rate", units="", description="")
        self.place_holder_irradiation = make_node(
            "V:place_holder_irradiation", units="", description="")
        self.place_holder_external_temp = make_node(
            "V:place_holder_external_temp", units="K", description="")

        self.place_holder_functional_covered = make_node(
            "V:place_holder_functional_covered", units="", description="")
        self.place_holder_available_en = make_node(
            "V:place_holder_available_en", units="J", description="")

        self.place_holder_en_used_heat = make_node(
            "V:place_holder_en_used_heat", units="J", description="")
        self.place_holder_en_needed_heat = make_node(
            "V:place_holder_en_needed_heat", units="J", description="")
        self.place_holder_en_used_pres = make_node(
            "V:place_holder_en_used_pres", units="J", description="")
        self.place_holder_en_needed_pres = make_node(
            "V:place_holder_en_needed_pres", units="J", description="")
        self.place_holder_power_cons = make_node(
            "V:place_holder_power_cons", units="J", description="")

        self.place_holder_structure_sec_1 = make_node(
            "V:place_holder_structure_sec_1", units="", description="")
        self.place_holder_structure_sec_2 = make_node(
            "V:place_holder_structure_sec_2", units="", description="")
        self.place_holder_structure_sec_3 = make_node(
            "V:place_holder_structure_sec_3", units="", description="")
        self.place_holder_structure_sec_4 = make_node(
            "V:place_holder_structure_sec_4", units="", description="")
        self.place_holder_structure_sec_5 = make_node(
            "V:place_holder_structure_sec_5", units="", description="")
        self.place_holder_int_str_temp = make_node(
            "V:place_holder_int_str_temp", units="K", description="")

        self.place_holder_int_env_temp = make_node(
            "V:place_holder_int_env_temp", units="K", description="")
        self.place_holder_int_env_pres = make_node(
            "V:place_holder_int_env_pres", units="atm", description="")


        self.place_holder_agent_repair_struct = make_node(
            "V:place_holder_agent_repair_struct", units="", description="")
        self.place_holder_agent_clean_panel = make_node(
            "V:place_holder_agent_clean_panel", units="", description="")
        self.place_holder_agent_clean_plant = make_node(
            "V:place_holder_agent_clean_plant", units="", description="")
        self.place_holder_agent_cover_panel = make_node(
            "V:place_holder_agent_cover_panel", units="", description="")

        #
        # cl = make_clock(3600.0)
        # print(type(inspect.getmembers(self, lambda a:not(inspect.isroutine(a)))))
        # for item in inspect.getmembers(self, lambda a:not(inspect.isroutine(a))):
        #     print(type(item),item)
        #     if isinstance(item, tuple):
        #         print('xxcc')
        #         replace(item, cl.dt)
        # for item in inspect.getmembers(self, lambda a:not(inspect.isroutine(a))):
        #     print(type(item),item)
        # sdsada
        return

    def replace_place_holder(self):
        print(self.keys)
        sdsad
        return