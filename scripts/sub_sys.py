

import argparse
import random
import math
import copy
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import time

##################################################

class solar:

    dynamic_system_name: str = 'solar'

    # coefficients
    capacity: int= 10
    energy_cons: int= 2
    initial_cost: int = 50
    rate: int = 10

    #subsystems
    sub1: str= 'solar_cover'
    sub2: str= 'solar_energy'
    sub3: str = 'energy_sensing_solar'


class solar_cover:

    dynamic_system_name: str = 'solar_cover'

    # coefficients
    capacity: int= 10
    energy_cons: int= 2
    initial_cost: int = 50

    #states
    state1: str= 'covered_or_not'
    state2: str= 'fault1'

    #state types
    s_type1: str= 'sensor'
    s_type1: str = 'health'



class solar_energy:

    dynamic_system_name: str = 'solar_energy'

    # coefficients
    capacity: int= 10
    energy_cons: int= 2
    initial_cost: int = 50
    rate_radiation: int = 100

    #states
    state1: str= 'energy_value'
    state2: str= 'fault1'

    #state types
    s_type1: str= 'physics'
    s_type1: str = 'health'


class energy_sensing_solar:

    dynamic_system_name: str = 'energy_sensing_solar'

    # coefficients
    capacity: int = 10
    energy_cons: int = 2
    initial_cost: int = 50
    rate_radiation: int = 100
    mean_error = 0.05
    std_error = 0.2
    rate = 10

    # states
    state1: str = 'solar_energy_output'
    state2: str = 'fault1'

    # state types
    s_type1: str = 'sensor'
    s_type1: str = 'health'


class nuclear:

    dynamic_system_name: str= 'nuclear'

    #coefficients
    capacity: int= 100
    energy_cons: int= 1
    initial_cost: int = 1000

    #subsystems
    sub1: str= 'nuclear_energy'
    sub2: str= 'energy_sensing_nuclear'

class nuclear_energy:

    dynamic_system_name: str = 'nuclear_energy'

    #coefficients
    capacity: int = 10000
    energy_cons: int = 2
    initial_cost: int = 5000
    rate = 2

    # states
    state1: str = 'energy_value'
    state2: str = 'fault1'

    # state types
    s_type1: str = 'physics'
    s_type1: str = 'health'


class energy_sensing_nuclear:

    dynamic_system_name: str = 'energy_sensing_nuclear'

    #coefficients
    capacity: int = 10000
    energy_cons: int = 2
    initial_cost: int = 5000
    rate = 2

    # states
    state1: str = 'nuclear_energy_output'
    state2: str = 'fault1'

    # state types
    s_type1: str = 'sensor'
    s_type1: str = 'health'






