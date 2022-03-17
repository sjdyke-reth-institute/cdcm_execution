"""Test a battery system

Author:
    Murali Krishnan R

Date:
    3/16/2022
"""

from cdcm import BatterySystem
from cdcm import PhysicalStateVariable, Parameter

def battery_transition_func(dt, *, x, r, c):
    """A simple transition function for the battery
    """
    pass


if __name__ == "__main__":
    batt = BatterySystem(
        state={'x': PhysicalStateVariable(1000, "ampere_hour", "battery_capacity", True)},
        parameters={'c': Parameter(1e-6, "ampere", "average discharge current"),
                    'd': Parameter(2e-6, "ampere", "average charge current")},
        transition_func=battery_transition_func,
    )
    print(batt)
    pass