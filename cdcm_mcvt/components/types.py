#!ovn!
"""Types of components and systems required to model MCVT-NRH in `exlang`

Author:
    R Murali Krishnan

Date:
    03.30.2023

"""


from cdcm import *


# Components of the active pressure control system
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


# Components of the air-handling unit
class Fan(System):
    pass

## Components of the heat-pump loop
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

## Components of the radiator loop
class RadiatorPanels(HeatExchanger):
    """Radiator component"""
    pass

class HeatPump(System):
    """A heat-pump system"""
    pass

class TXValve(Valve):
    """Thermo-static expansion valve"""
    pass

class RadiatorLoop(System):
    """Radiator loop"""
    pass

class Pump(System):
    """Pump system"""
    pass

class Heater(System):
    """Heater system"""
    pass

# Components of the power system
class PowerConverter(System):
    """Step-up converter"""
    pass

class GenerationBus(System):
    """Generation bus of the Power System"""
    pass

class EnergyStorage(System):
    """Energy Storage Systems"""
    pass

class PowerGenerator(System):
    """Sources of energy"""
    pass

class PowerConsumer(System):
    """Consumer of energy"""
    pass


# Systems in MCVT-NRH
class PowerSystem(System):
    """System that handles power in MCVT"""
    # Dictionary
    converters = {"step_up": [], "step_down": []}