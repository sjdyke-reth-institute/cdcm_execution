"""Test a nested system of systems.

Author:
	Ilias Bilionis

Date:
	3/15/2022

"""


from cdcm import *


def trans_func_1(dt, *, x1, r1):
    """A simple transition function for an isolated system."""
    new_x1 = x1 + r1 * dt
    new_state = {'x1': new_x1}
    return new_state

def trans_func_2(dt, *, x2, x1, r2, c):
    """Another simple transition function."""
    new_x2 = x2 + r2 * dt + c * x1 * dt
    return {'x2': new_x2}


def trans_func_3(dt, *, x3, r3):
    """A simple transition function for an isolated system."""
    new_x3 = x3 + r3 * dt
    new_state = {'x3': new_x3}
    return new_state

def trans_func_4(dt, *, x4, x2, r4, c24):
    """Another simple transition function."""
    new_x4 = x4 + r4 * dt + c24 * x2 * dt
    return {'x4': new_x4}


if __name__ == "__main__":
    sys1 = SystemFromFunction(
    	name="system_1",
        state={"x1": PhysicalStateVariable(0.1, "meters", "x1")},
        parameters={"r1": Parameter(1.2, "meters / second", "rate of change")},
        transition_func=trans_func_1)
    sys2 = SystemFromFunction(
    	name="system_2",
        state={"x2": PhysicalStateVariable(0.1, "meters", "x2")},
        parameters={"r2": Parameter(0.2, "meters / second", "rate of change"),
                    "c": Parameter(0.1, "1 / second", "coupling coeff")},
        parents={'x1': sys1},
        transition_func=trans_func_2)
    sos1 = SystemOfSystems(name="combined_system_1", 
        sub_systems={"system_1": sys1, "systm_2": sys2})
    sys3 = SystemFromFunction(
    	name="system_3",
        state={"x3": PhysicalStateVariable(0.1, "meters", "x3")},
        parameters={"r3": Parameter(1.2, "meters / second", "rate of change")},
        transition_func=trans_func_3)
    sys4 = SystemFromFunction(
    	name="system_4",
        state={"x4": PhysicalStateVariable(0.1, "meters", "x4")},
        parameters={"r4": Parameter(0.2, "meters / second", "rate of change"),
                    "c24": Parameter(0.1, "1 / second", "coupling coeff")},
        parents={'x2': sos1},
        transition_func=trans_func_4)
    sos2 = SystemOfSystems(name="combined_system_2", 
        sub_systems={"system_3": sys3, "system_4": sys4})
    sys = SystemOfSystems(sub_systems={"combined_system_1": sos1,
                                       "combined_system_2": sos2})
    print(sys)
    dt = 0.1
    for i in range(10):
        sys.unsafe_step(dt)
        print(f"x1: {sys.state['x1'].value:{1}.{3}}, x2: {sys.state['x2'].value:{1}.{3}}")