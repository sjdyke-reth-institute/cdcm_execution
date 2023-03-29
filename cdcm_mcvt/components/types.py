#!ovn!
"""Types of components required to model MCVT-NRH in `exlang`

Author:
    R Murali Krishnan

Date:
    03.27.2023

"""


from cdcm import *

# Sub-systems in MCVT/Structure


# Sub-systems in MCVT/ECLSS/Pressure Control
class Tank(System):
    """A tank system"""
    pass

class AirTank(Tank):
    """Tank for storing air"""
    pass

class Valve(System):
    pass

class InletValve(Valve):
    pass

class ReliefValve(Valve):
    pass

# Sub-systems in MCVT/ECLSS/Thermal Control
## Air-Handling Unit
class Fan(System):
    pass

## Heat-pump loop
class Compressor(System):
    pass

class HeatExchanger(System):
    pass

class Condenser(HeatExchanger):
    """Condense vapor-to-liquid"""
    pass

class Evaporator(HeatExchanger):
    """Turn liquid-to-vapor"""
    pass

class HeatPump(System):
    """A heat-pump system"""
    pass

class TXValve(Valve):
    """Thermo-static expansion valve"""
    pass

## Radiator Loop
class Radiator(HeatExchanger):
    """Radiator component"""
    pass

class Pump(System):
    """Pump system"""
    pass

# MCVT :: Power System
# SPD
class StepUpConverter(System):
    """Step-up converter"""
    pass

class StepDownConverter(System):
    """Step-down generator"""
    pass

POWER_CONVERTER_SET = {'U': StepUpConverter, 'D': StepDownConverter}

class GenerationBus(System):
    """Generation bus of the Power System"""
    pass

class Batteries(System):
    """Energy Storage Systems"""
    pass

# Source of energy
class EnergySource(System):
    """Sources of energy"""
    pass

class Solar(EnergySource):
    """Solar power source"""
    pass

class Nuclear(EnergySource):
    """Nuclear energy source"""
    pass

class EnergyConsumer(System):
    """Consumer of energy"""
    pass
