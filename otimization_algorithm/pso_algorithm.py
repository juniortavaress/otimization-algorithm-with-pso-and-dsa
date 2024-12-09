from otimization_algorithm.simualtion_manager import SimulationManager
from pyswarm import pso  
import numpy as np
from multiprocessing import Pool
import pandas as pd
import inspect
import os


def run_pso(self, inp_folder, target_forces, target_temperature, parameter_bounds):
    self.call_count = 0
    objective_function_pso = lambda params: objective_function(self, inp_folder, params, target_forces, target_temperature)

    lb = [b[0] for b in parameter_bounds]
    ub = [b[1] for b in parameter_bounds]
    
    best_position, best_score = pso(objective_function_pso, lb, ub, swarmsize=1, omega=0.5, phip=2, phig=2, maxiter=1, minstep=1e-6, minfunc=1e-3)    
    return self.call_count, best_position, best_score


def objective_function(self, inp_folder, parameters, target_forces, target_temperature):
    self.target_forces = target_forces
    self.target_temperature = target_temperature
    simulated_forces, simulated_temperature = SimulationManager.simulation_manager(self, parameters)

    percentage_error_cutting_force = abs((target_forces[0] - simulated_forces[0])/target_forces[0])
    percentage_error_normal_force = abs((target_forces[1] - simulated_forces[1])/target_forces[1])
    percentage_error_temperature = abs((target_temperature - simulated_temperature)/target_temperature)
    percentage_errors = [percentage_error_cutting_force, percentage_error_normal_force, percentage_error_temperature]

    error_force = np.sum((np.array(simulated_forces) - np.array(target_forces))**2)
    error_temperature = (simulated_temperature - target_temperature)**2
    normalized_force_error = error_force / np.sum(np.array(target_forces)**2)
    normalized_temp_error = error_temperature / target_temperature**2

    print("error_force", error_force)
    print("error_temperature", error_temperature)
    print("normalized_force_error", normalized_force_error)
    print("normalized_temp_error", normalized_temp_error)

    save_iteration_datas(self, parameters, target_forces, target_temperature, simulated_forces, simulated_temperature, percentage_errors)
    return np.sqrt(0.7 * normalized_force_error + 0.3 * normalized_temp_error)


def save_iteration_datas(self, parameters, target_forces, target_temperature, simulated_forces, simulated_temperature, percentage_errors):
    data = {"Parameter D1": [parameters[0]], "Parameter D2": [parameters[1]], "Parameter D3": [parameters[2]],
             "Experiment Cutting Force": target_forces[0], "Simulation Cutting Force": simulated_forces[1], "Error Fc": percentage_errors[1],
             "Experiment Normal Force": target_forces[1], "Simulation Normal Force": simulated_forces[0], "Error Fn": percentage_errors[0],
             "Experiment Temperature": target_temperature, "Simulation Temperature": simulated_temperature, "Error T": percentage_errors[2]}
    new_info = pd.DataFrame(data)
    
    data_path = os.path.join(self.excel_dir, "datas.xlsx")

    if os.path.exists(data_path):
        old_df = pd.read_excel(data_path, engine="openpyxl", index_col=0)
        new_df = pd.concat([old_df, new_info], ignore_index=True)
    else:
        new_df = new_info
    
    new_df.index.name = "Iteration"
    new_df.to_excel(data_path, index=True, engine="openpyxl")


