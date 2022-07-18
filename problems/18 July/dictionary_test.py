"""

Test by: Amir Behjat

Date:
    7/18/2022


Make the dictionary state test.

First step is ok. Second sep it gets the first key instead of dictionary.

"""
from cdcm import *
import time
import numpy as np
import copy

class dict_models():
    def __init__(self):

        with System(name="everything",
                    description="Everything that goes in the simulation") as everything:
            # dict_X = dict()
            # dict_X['name'] = 'name_XYZ'
            # dict_X['age'] = [0, 4, 5]
            # out = State(name="out", value=dict_X)
            out = State(name="out", value={'name': 'name_XYZ',
                                           'age': [0, 4, 5]},
                        description="nothing",
                        units="")

            @make_function(out)
            def f_dict(out=out):
                """Transition function for out"""
                print('input', type(out), out)
                out_new = copy.deepcopy(out)
                # out_new = dict()
                out_new['name'] = copy.deepcopy(out['name'])
                out_new['age'] = copy.deepcopy(out['age'])
                out_new['age'].pop()
                out_new['age'].append(np.random.randint(1,1111))
                print('output', type(out_new), out_new)
                return out_new
        self.hab_sys = everything

    def simulate(self):

        hab_sys = self.hab_sys
        max_steps = 10000
        dt = 10
        t_now = 0
        t_max = max_steps * dt
        tt = time.time()
        np.random.seed(0)
        while t_now < t_max:
            print(type(hab_sys.out.value), hab_sys.out.value)
            hab_sys.forward()
            hab_sys.transition()
            print(type(hab_sys.out.value), hab_sys.out.value)
            print('One step passed')
            t_now += dt
        return

np.random.seed(0)
hab_sys = dict_models()
hab_sys.simulate()
print('GG-NI')
