from otimization_algorithm.simualtion_manager import SimulationManager
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
    
    best_position, best_score = pso(self, objective_function_pso, lb, ub, swarmsize=3, omega=0.5, phip=2, phig=2, maxiter=5, minstep=1e-6, minfunc=1e-3)    
    return self.call_count, best_position, best_score


def objective_function(self, inp_folder, parameters, target_forces, target_temperature):
    self.target_forces = target_forces
    self.target_temperature = target_temperature

    error_list = []
    print("\n\n\n\n\n\n======================== PSO ========================\n")
    print('Numero de particulas: ', len(parameters))
    results_dict = SimulationManager.simulation_manager(self, parameters)

    print("\n\n======================== RESULT ========================\n")
    print(results_dict)

    # Ordena os índices do dicionário results_dict em ordem crescente
    sorted_indices = sorted(results_dict.keys())
    # print(sorted_indices)

    # Itera sobre os índices ordenados
    print("\n\n======================== DATAS ========================\n")
    for index in sorted_indices:
        # Extrai os resultados simulados para cada simulação
        data = results_dict[index]
        simulated_forces = data["Forces"]
        simulated_temperature = data["Temperatures"]
        
        percentage_error_cutting_force = abs((target_forces[0] - simulated_forces[0])/target_forces[0])
        percentage_error_normal_force = abs((target_forces[1] - simulated_forces[1])/target_forces[1])
        percentage_error_temperature = abs((target_temperature - simulated_temperature)/target_temperature)
        percentage_errors = [percentage_error_cutting_force, percentage_error_normal_force, percentage_error_temperature]

        error_force = np.sum((np.array(simulated_forces) - np.array(target_forces))**2)
        error_temperature = (simulated_temperature - target_temperature)**2
        normalized_force_error = error_force / np.sum(np.array(target_forces)**2)
        normalized_temp_error = error_temperature / target_temperature**2

        # print("for for for")
        # print("error_force", error_force)
        # print("error_temperature", error_temperature)
        # print("normalized_force_error", normalized_force_error)
        # print("normalized_temp_error", normalized_temp_error)

        # save_iteration_datas(self, param, target_forces, target_temperature, simulated_forces, simulated_temperature, percentage_errors)
        error_list.append(np.sqrt(0.7 * normalized_force_error + 0.3 * normalized_temp_error))
        print('-T-', index, simulated_temperature)
        print('-F-', index, simulated_temperature)
        print('-E-', index, np.sqrt(0.7 * normalized_force_error + 0.3 * normalized_temp_error))

    print("\n\n======================== ERROS ========================\n")
    print("error_list", error_list)
    return error_list

def save_iteration_datas(self, parameters, target_forces, target_temperature, simulated_forces, simulated_temperature, percentage_errors):
    data = {"Parameter D1": [parameters[0]], "Parameter D2": [parameters[1]], "Parameter D3": [parameters[2]],
             "Experiment Cutting Force": target_forces[0], "Simulation Cutting Force": simulated_forces[0], "Error Fc": percentage_errors[1],
             "Experiment Normal Force": target_forces[1], "Simulation Normal Force": simulated_forces[1], "Error Fn": percentage_errors[0],
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




# Função PSO (Particle Swarm Optimization)
def pso(self, objective_function_pso, lb, ub, swarmsize, omega, phip, phig, maxiter, minstep=1e-6, minfunc=1e-3):
    
    # Inicialização das partículas
    num_particles = swarmsize
    num_dimensions = len(lb)
    positions = np.random.uniform(low=lb, high=ub, size=(num_particles, num_dimensions))
    velocities = np.random.uniform(low=-1, high=1, size=(num_particles, num_dimensions))

    # Inicialização das melhores posições e melhores scores
    personal_best_positions = np.copy(positions) # contem todas posições iniciais, mesmo numero de elementos que o particle swarm
    personal_best_scores = np.array(objective_function_pso(positions))  # contem o erro de cada particula

    print("\n\n======================== SCORE ========================\n")
    print('score', personal_best_scores)

    # Melhor global
    # Aqui pega o menor erro e a particula com menor erro 
    global_best_position = personal_best_positions[np.argmin(personal_best_scores)] # Pega a particula de menor erro
    global_best_score = min(personal_best_scores) # pega o menor erro
    global_best_scores_history = [global_best_score] # copia o menor erro

    # PSO Optimization
    for iteration in range(maxiter-1):
        for i in range(num_particles):
            r1, r2 = np.random.rand(), np.random.rand()
            velocities[i] = (omega * velocities[i] +
                            phip * r1 * (personal_best_positions[i] - positions[i]) +
                            phig * r2 * (global_best_position - positions[i]))
            
            positions[i] += velocities[i] # conjunto de novas particulas 
            positions[i] = np.clip(positions[i], lb, ub) # ajusta os valores fora do limite, tem que ver se isso faz sentido
            
        score = objective_function_pso(positions) # erro de cada iteração feita pelo for

        for i in range(num_particles):
            if score[i] < personal_best_scores[i]:
                personal_best_scores[i] = score[i]
                personal_best_positions[i] = positions[i]
        
            if score[i] < global_best_score:
                global_best_score = score[i]
                global_best_position = positions[i]
    
        global_best_scores_history.append(global_best_score) # melhor resultado de cada iteração
        
        # Verificar critério de parada
        if global_best_score < minfunc:
            print(f"Critério de parada atingido na iteração {iteration+1}")
            break
    # return [10,10,10], 10
    return global_best_position, global_best_score