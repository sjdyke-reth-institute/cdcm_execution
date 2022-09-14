"""
Minimal bug report.

What happens:

    The order of the input variables may get mixed.

"""

from cdcm import *


out = Parameter(name="out", value=0.0)

HM_pressure_lower_setpoint = Variable(name="lower_pressure_setpo", value=1.0)
HM_pressure_upper_setpoint = Variable(name="upper_pressure_setpo", value=2.0)
struct_health = Variable(name="struct_health=struct_health", value=3.0)
efficiency_of_PM = Variable(name="efficiency_of_PM", value=4.0)
pres_capac_per_vol = Variable(name="pres_capac_per_vol", value=5.0)
air_leak_coeficent = Variable(name="air_leak_coeficent", value=6.0)
en_needed_pres = Variable(name="en_needed_pres", value=7.0)
available_en = Variable(name="available_en", value=8.0)
int_env_pres = Variable(name="int_env_pres", value=9.0)


@make_function(out)
def f_eclss_pres_1(
    lower_pressure_setpo=HM_pressure_lower_setpoint,
    upper_pressure_setpo=HM_pressure_upper_setpoint,
    efficiency_of_PM=efficiency_of_PM,
    pres_capac_per_vol=pres_capac_per_vol,
    air_leak_coeficent=air_leak_coeficent,
    en_needed_pres=en_needed_pres,
    available_en=available_en,
    struct_health=struct_health,
    int_env_pres=int_env_pres,
):
    """Transition function for ECLSS pressure"""
    print(
        "en_needed_pres",
        en_needed_pres,
        "available_en",
        available_en,
        "struct_health",
        struct_health,
        "int_env_pres",
        int_env_pres,
        "lower_pressure_setpo",
        lower_pressure_setpo,
        "upper_pressure_setpo",
        upper_pressure_setpo,
        "pres_capac_per_vol",
        pres_capac_per_vol,
        "air_leak_coeficent",
        air_leak_coeficent,
        "efficiency_of_PM",
        efficiency_of_PM,
    )


@make_function(out)
def f_eclss_pres_2(
    lower_pressure_setpo=HM_pressure_lower_setpoint,
    upper_pressure_setpo=HM_pressure_upper_setpoint,
    struct_health=struct_health,
    efficiency_of_PM=efficiency_of_PM,
    pres_capac_per_vol=pres_capac_per_vol,
    air_leak_coeficent=air_leak_coeficent,
    en_needed_pres=en_needed_pres,
    available_en=available_en,
    int_env_pres=int_env_pres,
):
    """Transition function for ECLSS pressure"""
    print(
        "en_needed_pres",
        en_needed_pres,
        "available_en",
        available_en,
        "struct_health",
        struct_health,
        "int_env_pres",
        int_env_pres,
        "lower_pressure_setpo",
        lower_pressure_setpo,
        "upper_pressure_setpo",
        upper_pressure_setpo,
        "pres_capac_per_vol",
        pres_capac_per_vol,
        "air_leak_coeficent",
        air_leak_coeficent,
        "efficiency_of_PM",
        efficiency_of_PM,
    )


print()
f_eclss_pres_1.forward()
print()
f_eclss_pres_2.forward()
