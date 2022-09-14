import json
import pickle

import numpy as np
import matplotlib.pyplot as plt

#use one of LS_mission files name without .pkl part
f_name = "Battery_sample"

file = open(f_name + ".pkl",'rb')
object_file = pickle.load(file)


var_to_check = dict()
var_to_check_unit = dict()

var_to_check[0] = 'high_current'
var_to_check_unit[0] = 'A'
var_to_check[1] = 'battery_degeradation_state'
var_to_check_unit[1] = '% Life'
var_to_check[2] = 'battery_shock_current_state'
var_to_check_unit[2] = '% Life'
var_to_check[3] = 'battery_overal_state'
var_to_check_unit[3] = '% Life'

var_to_check_old = dict() # just for lables
var_to_check_old[0] = 'Extra Current'
var_to_check_old[1] = 'Degradation State'
var_to_check_old[2] = 'Shocked State'
var_to_check_old[3] = 'overall State'
N_times = len(object_file)
N_vars = len(var_to_check)

times = np.zeros(shape = [N_times, ])
var = np.zeros(shape = [N_times, N_vars])
for i in range(N_times):
    times[i] = object_file[i]['time']
    for j in range(N_vars):
        var[i, j] = object_file[i][var_to_check[j]]


N_columns = int(min(2, N_vars))
N_rows = int(np.ceil(N_vars / N_columns))
fig, axs = plt.subplots(N_rows, N_columns)
fig.set_size_inches(18.5, 10.5 * np.ceil(N_rows/2))
for j in range(N_vars):
    if (j % 2) == 1:
        axs[int(np.floor(j / 2)), 1].grid(True)
        axs[int(np.floor(j / 2)), 1].plot(times, var[:, j])
        axs[int(np.floor(j / 2)), 1].set(xlabel='Time (hr)', ylabel=var_to_check[j] + "(" + var_to_check_unit[j] + ")")
        axs[int(np.floor(j / 2)), 1].set_title(var_to_check_old[j] + " Vs. Time")
    else:
        axs[int(np.floor(j / 2)), 0].grid(True)
        axs[int(np.floor(j / 2)), 0].plot(times, var[:, j])
        axs[int(np.floor(j / 2)), 0].set(xlabel='Time (hr)', ylabel=var_to_check[j] + "(" + var_to_check_unit[j] + ")")
        axs[int(np.floor(j / 2)), 0].set_title(var_to_check_old[j] + " Vs. Time")

plt.subplots_adjust(left=0.1,
                    bottom=0.1,
                    right=0.9,
                    top=0.9,
                    wspace=0.4,
                    hspace=0.4)

plt.savefig(f_name + '.png', dpi=200)
# plt.show()

