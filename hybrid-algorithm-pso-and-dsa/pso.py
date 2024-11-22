from functions import *
from pyswarm import pso  
import numpy as np
from multiprocessing import Pool
import pandas as pd
import os

def objective_function(parameters, target_forces, target_temperature):
    simulated_forces, simulated_temperature, call_count = run_simulation(parameters)

    percentage_error_cutting_force = abs((target_forces[0] - simulated_forces[0])/target_forces[0])
    percentage_error_normal_force = abs((target_forces[1] - simulated_forces[1])/target_forces[1])
    percentage_error_temperature = abs((target_temperature - simulated_temperature)/target_temperature)
    percentage_errors = [percentage_error_cutting_force, percentage_error_normal_force, percentage_error_temperature]

    error_force = np.sum((np.array(simulated_forces) - np.array(target_forces))**2)
    error_temperature = (simulated_temperature - target_temperature)**2

    normalized_force_error = error_force / np.sum(np.array(target_forces)**2)
    normalized_temp_error = error_temperature / target_temperature**2
    save_iteration_datas(parameters, target_forces, target_temperature, simulated_forces, simulated_temperature, percentage_errors)
    return np.sqrt(0.7 * normalized_force_error + 0.3 * normalized_temp_error)


def run_pso(target_forces, target_temperature, parameter_bounds):
    objective_function_pso = lambda params: objective_function(params, target_forces, target_temperature)

    lb = [b[0] for b in parameter_bounds]
    ub = [b[1] for b in parameter_bounds]
    
    best_position, best_score = pso(objective_function_pso, lb, ub, swarmsize=6, omega=0.5, phip=2, phig=2, maxiter=2, minstep=1e-6, minfunc=1e-3)    
    return best_position, best_score


def save_iteration_datas(parameters, target_forces, target_temperature, simulated_forces, simulated_temperature, percentage_errors):
    data = {"Parameter A": [parameters[0]], "Parameter B": [parameters[1]], "Parameter C": [parameters[2]], "Parameter m": [parameters[3]], "Parameter n": [parameters[4]],
             "Experiment Cutting Force": target_forces[0], "Simulation Cutting Force": simulated_forces[0], "Error Fc": percentage_errors[0],
             "Experiment Normal Force": target_forces[1], "Simulation Normal Force": simulated_forces[1], "Error Fn": percentage_errors[1],
             "Experiment Temperature": target_temperature, "Simulation Temperature": simulated_temperature, "Error T": percentage_errors[2]}
    new_info = pd.DataFrame(data)
    
    if os.path.exists("datas.xlsx"):
        old_df = pd.read_excel("datas.xlsx", engine="openpyxl", index_col=0)
        new_df = pd.concat([old_df, new_info], ignore_index=True)
    else:
        new_df = new_info
    
    new_df.index.name = "Iteration"
    new_df.to_excel('datas.xlsx', index=True, engine="openpyxl")


