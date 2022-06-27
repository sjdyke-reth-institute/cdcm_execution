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
    Arguments

    """

    def __init__(self):

        return

    def define_place_holder(self):
        """
            add the place holders

        """
        self.place_holder_available_en = make_node(
            "V:place_holder_available_en", units="J", description=" Total available energy in batteries")
        self.place_holder_en_used_heat = make_node(
            "V:place_holder_en_used_heat", units="J", description="Used energy to control the temperature")
        self.place_holder_en_needed_heat = make_node(
            "V:place_holder_en_needed_heat", units="J", description="Needed energy to control the temperature")
        self.place_holder_en_used_pres = make_node(
            "V:place_holder_en_used_pres", units="J", description="Used energy to control the pressure")
        self.place_holder_en_needed_pres = make_node(
            "V:place_holder_en_needed_pres", units="J", description="Needed energy to control the pressure")
        self.place_holder_energy_cons = make_node(
            "V:place_holder_energy_cons", units="J", description="Total energy consumption in ECLSS")
        self.place_holder_int_str_temp = make_node(
            "V:place_holder_int_str_temp", units="K", description="Temparature of the inner side of the structure")
        self.place_holder_int_env_temp = make_node(
            "V:place_holder_int_env_temp", units="K", description="Temparature of the interior environment")
        self.place_holder_int_env_pres = make_node(
            "V:place_holder_int_env_pres", units="atm", description="Pressure of the interior environment")


        self.place_holder_struct_health = make_node(
            "V:place_holder_struct_health", value=[1.0, 1.0, 1.0, 1.0, 1.0], units="", description="The array of how much healthy is each dome section")
        self.place_holder_agent_repair_struct = make_node(
            "V:place_holder_agent_repair_struct", units="", description="The array of how much repair is given to each dome section in unit of time step")
        self.place_holder_agent_clean_panel = make_node(
            "V:place_holder_agent_clean_panel", units="", description="Cleaning the panel value in one time step")
        self.place_holder_agent_clean_plant = make_node(
            "V:place_holder_agent_clean_plant", units="", description="Cleaning the nuclear plant radiator value in one time step")
        self.place_holder_HM_cover_panel = make_node(
            "V:place_holder_HM_cover_panel", units="", description="1= Solar panel is functional, 0= solar panel is covered against dust")

        self.place_holder_HM_temperature_lower_setpoint = make_node(
            "V:place_holder_HM_lower_temparature_setpoint", units="", description="The lower temperature set point from HM to ECLSS")
        self.place_holder_HM_temperature_upper_setpoint = make_node(
            "V:place_holder_HM_upper_temparature_setpoint", units="", description="The upper temperature set point from HM to ECLSS")
        self.place_holder_HM_pressure_lower_setpoint = make_node(
            "V:place_holder_HM_lower_pressure_setpoint", units="", description="The lower pressure set point from HM to ECLSS")
        self.place_holder_HM_pressure_upper_setpoint = make_node(
            "V:place_holder_HM_upper_pressure_setpoint", units="", description="The upper pressure set point from HM to ECLSS")

        return

    def replace_place_holder(self, everything):
        """
            Replace Place holders
            Argument
                everything -- The habitat system which will get states replaced
        """

        replace(everything.place_holder_available_en, everything.energy.energy_store_energy.available_en)
        replace(everything.place_holder_en_used_heat, everything.eclss.eclss_temperature.en_used_heat)
        replace(everything.place_holder_en_needed_heat, everything.eclss.eclss_temperature.en_needed_heat)
        replace(everything.place_holder_en_used_pres, everything.eclss.eclss_pressure.en_used_pres)
        replace(everything.place_holder_en_needed_pres, everything.eclss.eclss_pressure.en_needed_pres)
        replace(everything.place_holder_energy_cons, everything.eclss.eclss_energy_consumption.energy_cons)
        replace(everything.place_holder_int_str_temp, everything.struct.structure_temp.int_str_temp)
        replace(everything.place_holder_struct_health, everything.struct.structure_health.structure_secs)

        return everything