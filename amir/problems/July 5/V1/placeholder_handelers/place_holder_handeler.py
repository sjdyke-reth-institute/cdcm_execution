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
        self.place_holder_available_en = Variable(name="place_holder_available_en", units="J", value=7200000.0, description=" Total available energy in batteries")
        self.place_holder_en_used_heat = Variable(name="place_holder_en_used_heat", units="J", value=0.0, description="Used energy to control the temperature")
        self.place_holder_en_needed_heat = Variable(name="place_holder_en_needed_heat", units="J", value=0.0, description="Needed energy to control the temperature")
        self.place_holder_en_used_pres = Variable(name="place_holder_en_used_pres", units="J", value=0.0, description="Used energy to control the pressure")
        self.place_holder_en_needed_pres = Variable(name="place_holder_en_needed_pres", units="J", value=0.0, description="Needed energy to control the pressure")
        self.place_holder_energy_cons = Variable(name="place_holder_energy_cons", units="J", value=0.0, description="Total energy consumption in ECLSS")
        self.place_holder_int_str_temp = Variable(name="place_holder_int_str_temp", units="K", value=300.0, description="Temparature of the inner side of the structure")
        self.place_holder_int_env_temp = Variable(name="place_holder_int_env_temp", units="K", value=280.0, description="Temparature of the interior environment")
        self.place_holder_int_env_pres = Variable(name="place_holder_int_env_pres", units="atm", value=1.0, description="Pressure of the interior environment")

        self.place_holder_struct_health = Variable(name="place_holder_struct_health", value=[1.0, 1.0, 1.0, 1.0, 1.0], units="", description="The array of how much healthy is each dome section")

        self.place_holder_agent_repair_struct = Variable(name="place_holder_agent_repair_struct", units="", value=[0.0, 0.0, 0.0, 0.0, 0.0], description="The array of how much repair is given to each dome section in unit of time step")
        self.place_holder_agent_clean_panel = Variable(name="place_holder_agent_clean_panel", units="", value=0.0, description="Cleaning the panel value in one time step")
        self.place_holder_agent_clean_plant = Variable(name="place_holder_agent_clean_plant", units="", value=0.0, description="Cleaning the nuclear plant radiator value in one time step")

        self.place_holder_HM_cover_panel = Variable(name="place_holder_HM_cover_panel", units="", value=False, description="1= Solar panel is functional, 0= solar panel is covered against dust")
        self.place_holder_HM_temperature_lower_setpoint = Variable(name="place_holder_HM_lower_temparature_setpoint", units="", value=270.0, description="The lower temperature set point from HM to ECLSS")
        self.place_holder_HM_temperature_upper_setpoint = Variable(name="place_holder_HM_upper_temparature_setpoint", units="", value=300.0, description="The upper temperature set point from HM to ECLSS")
        self.place_holder_HM_pressure_lower_setpoint = Variable(name="place_holder_HM_lower_pressure_setpoint", units="", value=0.80, description="The lower pressure set point from HM to ECLSS")
        self.place_holder_HM_pressure_upper_setpoint = Variable(name="place_holder_HM_upper_pressure_setpoint", units="", value=1.05, description="The upper pressure set point from HM to ECLSS")

        return

    def replace_place_holder(self, everything):
        """
            Replace Place holders
            Argument
                everything -- The habitat system which will get states replaced
        """

        replace(everything.place_holder_available_en, everything.energy.energy_store.available_en)
        replace(everything.place_holder_en_used_heat, everything.eclss.eclss_temperature.en_used_heat)
        replace(everything.place_holder_en_needed_heat, everything.eclss.eclss_temperature.en_needed_heat)
        replace(everything.place_holder_en_used_pres, everything.eclss.eclss_pressure.en_used_pres)
        replace(everything.place_holder_en_needed_pres, everything.eclss.eclss_pressure.en_needed_pres)
        replace(everything.place_holder_energy_cons, everything.eclss.eclss_energy_consumption.energy_cons)
        replace(everything.place_holder_int_str_temp, everything.struct.struct_temp.int_str_temp)
        replace(everything.place_holder_struct_health, everything.struct.struct_health.structure_secs)
        replace(everything.place_holder_int_env_temp, everything.int_env.int_env_temperature.int_env_temp)
        replace(everything.place_holder_int_env_pres, everything.int_env.int_env_pressure.int_env_pres)

        # print(everything.dome_specs)
        # input('dome_specs')
        # print('\n' * 80)
        # print(everything.moon)
        # input('moon')
        # print('\n' * 80)
        # print(everything.energy)
        # input('energy')
        # print('\n' * 80)
        # print(everything.eclss)
        # input('eclss')
        # print('\n' * 80)
        # print(everything.struct)
        # input('struct')
        # print('\n' * 80)
        # print(everything.int_env)
        # input('int_env')
        # print('\n' * 80)
        # dsas

        return everything