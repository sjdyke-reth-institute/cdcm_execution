"""Test a battery system

Author:
    Murali Krishnan R

Date:
    3/16/2022
"""

from rich import print as rprint

from cdcm import System, SystemOfSystems
from cdcm import PhysicalStateVariable, Parameter, HealthStateVariable


def clip(value, min_value=0., max_value=100.):
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
            "x_battery": PhysicalStateVariable(100., "ampere_hour", "x", track=True,
                                        description="battery capacity"),
            "h_battery": HealthStateVariable(1, None, "h", True,
                                        description="health state of battery"),
            "c_battery": PhysicalStateVariable(-1., "ampere", "current",
                                       description="Discharge or charge current")
        }
        parameters = {
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
        # Extract state values
        x = self.state["x_battery"].value
        h = self.state["h_battery"].value
        c = self.state["c_battery"].value
        
        # Extract parameter values
        x_good = self.parameters["x_good"].value
        x_min = self.parameters["x_min"].value
        x_max = self.parameters["x_max"].value
        nugget = self.parameters["nugget"].value
        
        # Dynamics
        x_new = clip(x + c * dt, x_min, x_max)

        if (x_new <= x_good):
            h_new = 0
        elif (h == 0) and (abs(x_new - x_max) < nugget):
            h_new = 1
        else:
            h_new = h

        # Update next time-step
        self._next_state["x_battery"].value = x_new
        self._next_state["h_battery"].value = h_new
        self._next_state["c_battery"].value = c
    

class BatterySystemController(System):
    """A switch to turn battery from discharging to charging"""
    
    def __init__(self, battery):
        name = "BatteryController"
        state = {
            "x_current" : PhysicalStateVariable(-1., "ampere", "current", True,
                                                description="Discharge/charge current to"),
            
        }
        parameters = {
            "d_current" : Parameter(-1., "ampere", "discharge_current"),
            "c_current" : Parameter(+2., "ampere", "charging_current"),
        }
        parents = {
            "h_battery" : battery
        }
        super().__init__(name=name, state=state, parameters=parameters, 
                         parents=parents)
        pass

    def _calculate_next_state(self, dt):
        # Get parents
        h_battery = self.get_parent_state('h_battery').value
        # Get parameters

        if h_battery == 1:
            x_current_next = self.parameters["d_current"].value
        elif h_battery == 0:
            x_current_next = self.parameters["c_current"].value
        else:
            raise RuntimeError(f"Invalid option for `h_battery`: {h_battery}")
        
        # Update for next time-step
        self._next_state["x_current"].value = x_current_next        

if __name__ == "__main__":
    # Test 1: A simple battery system
    # A battery system
    battery = BatterySystem()
    rprint(battery)
    # Run Battery alone
    dt = 0.1
    rprint(f"x1: {battery.state['x_battery'].value:.2f}, h: {battery.state['h_battery'].value:{1}}")
    for i in range(20):
        battery.step(dt)
        rprint(f"x_battery: {battery.state['x_battery'].value:.2f}, h_battery: {battery.state['h_battery'].value:{1}}")
    
    ## Test 2 : A simple battery system with controller (open)
    # A battery system
    battery = BatterySystem()
    # define a controller for the battery
    controller = BatterySystemController(battery)
    sys = SystemOfSystems("BatterySystemWithController", 
                          sub_systems=[battery, controller])
    for i in range(20):
        sys.unsafe_step(dt)
        rprint(f"x_battery: {sys.state['x_battery'].value:.2f}, h_battery: {sys.state['h_battery'].value}, x_current: {sys.state['x_current'].value}")