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

class Heater(System):
    """Heater system"""
    pass

# MCVT :: Power System
class PowerConverter(System):
    """Step-up converter"""
    pass

class GenerationBus(System):
    """Generation bus of the Power System"""
    pass

class EnergyStorage(System):
    """Energy Storage Systems"""
    pass

# Source of energy
class PowerGenerator(System):
    """Sources of energy"""
    pass

class PowerConsumer(System):
    """Consumer of energy"""
    pass
