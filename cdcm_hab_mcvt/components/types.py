#!ovn!
"""Types of components required to model MCVT-NRH in CDCM

Author:
    R Murali Krishnan

Date:
    03.27.2023

"""


from cdcm import *


# Sub-systems in ECLSS - Pressure Control
class AirTank(System):
    pass

class Valve(System):
    pass

class InletValve(Valve):
    pass

class ReliefValve(Valve):
    pass

# Sub-systems in ECLSS - Thermal Control
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

class Radiator(HeatExchanger):
    """Radiator component"""
    pass

class HeatPump(System):
    """A heat-pump system"""
    pass

class TXValve(Valve):
    """Thermo-static expansion valve"""
    pass