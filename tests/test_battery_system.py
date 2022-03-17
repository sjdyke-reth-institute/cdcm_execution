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
    """A battery model with linear discharge and charging characteristics
    
    TODO
    - Move the control of battery out of this class
    """

    def __init__(self):
        name = "Battery"
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
            "x_good": Parameter(99., "ampere_hour", "x_good",
                                     description="Threshold for healthy behavior."),
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
        x_good = self.parameters['x_good'].value
        nugget = self.parameters['nugget'].value
        
        if h == 1:
            # Battery is healthy
            d = self.parameters['d'].value
            new_x = clip(x - d * dt, x_min, x_max)
            self._next_state['x'].value = new_x
            self._next_state['h'].value = 0 if new_x <= x_good else 1
        elif h == 0:
            # Battery is unhealthy
            c = self.parameters['c'].value
            new_x = clip(x + c * dt, x_min, x_max)
            self._next_state['x'].value = new_x
            self._next_state['h'].value = 1 if abs(new_x - x_max) < nugget else 0
        else:
            raise RuntimeError("Unrecognized health state...")
    

class BatterySystemSwitch(SystemFromFunction):
    """A switch to turn battery from discharging to charging"""
    def __init__(self):
        name = "BatterySwitch"
        state = {
            "x" : PhysicalStateVariable()
        }
        pass
        

if __name__ == "__main__":
    # A battery system
    battery = BatterySystem()
    charge_switch = BatterySystemSwitch()
    rprint(battery)
    # Run it for a while
    dt = 0.1
    rprint(f"x1: {battery.state['x'].value:.2f}, h: {battery.state['h'].value:{1}}")
    for i in range(30):
        battery.step(dt)
        rprint(f"x1: {battery.state['x'].value:.2f}, h: {battery.state['h'].value:{1}}")
