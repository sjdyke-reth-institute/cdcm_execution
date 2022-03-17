"""Test a battery system

Author:
    Murali Krishnan R

Date:
    3/16/2022
"""

from rich import print as rprint

from cdcm import System, SystemFromFunction
from cdcm import PhysicalStateVariable, Parameter, HealthStateVariable

def clip(value, min_value, max_value):
    """Clip the value between the bounds"""
    return min(max(value, min_value), max_value)

class BatterySystem(System):

    def __init__(self):
        name = "battery"
        state = {
            "x": PhysicalStateVariable(100., "ampere_hour", "x", track=True,
                                        description="battery capacity"),
            "h": HealthStateVariable(1, None, "h", True,
                                        description="health state of battery")
        }
        parameters = {
            "c" : Parameter(2., "ampere", "charge_current",
                            description="Average charge current."),
            "d" : Parameter(1., "ampere", "discharge_current",
                            description="Average discharge current."),
            "x_min": Parameter(0., "ampere_hour", "x_min", 
                               description="Minimum battery capacity."),
            "x_max": Parameter(100., "ampere_hour", "x_max",
                               description="Minimum battery capacity."),
            "x_unhealthy": Parameter(99., "ampere_hour", "x_unhealthy",
                                     description="Threshold for unhealthy behavior."),
            "nugget": Parameter(1e-3, [], "nugget", 
                                description="Floating point error tolerance")
        }
        super().__init__(name=name, state=state, parameters=parameters,
                         description="Simple Battery System")
    
    def _calculate_next_state(self, dt):
        h = self.state["h"].value
        x = self.state["x"].value
        x_min = self.parameters['x_min'].value
        x_max = self.parameters['x_max'].value
        x_unhealthy = self.parameters['x_unhealthy'].value
        nugget = self.parameters['nugget'].value
        
        if h == 1:
            d = self.parameters['d'].value
            self._next_state['x'].value = clip(x - d * dt, x_min, x_max)
            rprint(self._next_state['x'].value)
            self._next_state['h'].value = 0 if x <= x_unhealthy else 1
        elif h == 0:
            c = self.parameters['c'].value
            self._next_state['x'].value = clip(x + c * dt, x_min, x_max)
            self._next_state['h'].value = 1 if abs(x-x_max) < nugget else 0
        else:
            raise RuntimeError("Unrecognized health state...")
    

        

if __name__ == "__main__":
    # A battery system
    sys = BatterySystem()
    
    # Run it for a while
    dt = 0.1
    for i in range(20):
        sys.step(dt)
        rprint(f"x1: {sys.state['x'].value:{0}.{3}}, h: {sys.state['h'].value:{1}}")
    pass