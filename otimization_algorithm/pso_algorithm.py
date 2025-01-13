# -*- coding: utf-8 -*-
import os
import json
import numpy as np
import pandas as pd
from file_utils import FileUtils
from otimization_algorithm.simualtion_manager import SimulationManager

class PsoManager():
    def run_pso(self):
        """
        Runs the Particle Swarm Optimization (PSO) algorithm to minimize the objective function.
        """
        self.call_count = 0
        self.call_count_interation = 0
        lb, ub = PsoManager.get_boundry(self)
        objective_function_pso = lambda params: PsoManager.objective_function(self, params)
        best_position, best_score = PsoManager.pso(self, objective_function_pso, lb, ub, swarmsize=1, omega=0.5, phip=2, phig=2, maxiter=1, minstep=1e-6, minfunc=1e-3)
        return self.call_count, best_position, best_score
        

    def get_boundry(self):
        """
        Retrieves the lower and upper boundaries for optimization parameters.
        """
        otimization_cond = os.path.join(self.geometry_datas_dir, "defaut\otimizationdatas.json")
        with open(otimization_cond, "r") as info:
            otimization_datas = json.load(info)

        lb, ub = [], []
        parameters = otimization_datas.get("parameters_limits", {})
        for key, _ in parameters.items():
            min_value = parameters[key]["min"]
            max_value = parameters[key]["max"]
            lb.append(min_value)
            ub.append(max_value)
        return lb, ub


    def objective_function(self, parameters):
        """
        Objective function calculates errors based on simulated forces and temperatures
        compared to experimental data.

        Returns:
            list: Errors for each parameter set.
        """
            
        # Dicionário para armazenar os erros calculados
        error_dict = {}
        error_list = []

        params_map = {}
        for index, param in enumerate(parameters):
            formatted_coords = '[' + ', '.join(map(lambda x: str(np.round(x, 2)), param)) + ']'
            params_map[index] = formatted_coords

        datas_exp = PsoManager.get_experimental_datas(self)
        results_dict = SimulationManager.simulation_manager(self, parameters)
        
        if not self.error_track:
            sorted_indices = sorted(results_dict.keys())
            for index in sorted_indices:
                data = results_dict[index]
                filename = data["Filename"]
                simulated_forces = data["Forces"]
                simulated_temperature = data["Temperatures"]
                simulated_chip_compression_ratio = data["CCR"]
                simulated_chip_segmentation_ratio = data["CSR"]

                # print("++++++++++",  chip_compression_ratio, chip_segmentation_ratio)

                info = filename.split("_p")
                param_info = info[1].split("_")
                params_set = [float(param_info[1]), float(param_info[3]), float(param_info[5])]

                if info[0] in datas_exp:
                    target_cutting_force = datas_exp[filename.split("_p")[0]].get("cutting_force")
                    target_normal_force = datas_exp[filename.split("_p")[0]].get("normal_force")
                    target_temperature = datas_exp[filename.split("_p")[0]].get("temperature")
                    target_chip_compression_ratio = datas_exp[filename.split("_p")[0]].get("CCR")
                    target_chip_segentatio_ratio = datas_exp[filename.split("_p")[0]].get("CSR")
                    targets = [target_cutting_force, target_normal_force, target_temperature, target_chip_compression_ratio, target_chip_segentatio_ratio]

                percentage_error_cutting_force = abs((target_cutting_force - simulated_forces[0])/target_cutting_force)
                percentage_error_normal_force = abs((target_normal_force - simulated_forces[1])/target_normal_force)
                percentage_error_temperature = abs((target_temperature - simulated_temperature)/target_temperature)
                percentage_error_CCR = abs((target_chip_compression_ratio - simulated_chip_compression_ratio)/target_chip_compression_ratio)
                percentage_error_CSR = abs((target_chip_segentatio_ratio - simulated_chip_segmentation_ratio)/target_chip_segentatio_ratio)
                percentage_errors = [percentage_error_cutting_force, percentage_error_normal_force, percentage_error_temperature, percentage_error_CCR, percentage_error_CSR]

                normalized_cutting_force_error = ((simulated_forces[0] - target_cutting_force)**2) / target_cutting_force**2
                normalized_normal_force_error = ((simulated_forces[1] - target_normal_force)**2) / target_normal_force**2
                normalized_temp_error = ((simulated_temperature - target_temperature)**2) / target_temperature**2
                normalized_CCR_error = ((simulated_chip_compression_ratio - target_chip_compression_ratio)**2) / target_chip_compression_ratio**2
                normalized_CSR_error = ((simulated_chip_segmentation_ratio - target_chip_segentatio_ratio)**2) / target_chip_segentatio_ratio**2

                if str(params_set) not in error_dict:
                    error_dict[str(params_set)] = {}
                normalized_total_error = (np.sqrt(0.5 * normalized_cutting_force_error + 0.1 * normalized_normal_force_error + 0.2 * normalized_CCR_error + 0.2 * normalized_CSR_error))
                error_dict[str(params_set)][index] = normalized_total_error

                PsoManager.save_iteration_datas(self, info[0], params_set, simulated_forces, simulated_temperature, simulated_chip_compression_ratio, simulated_chip_segmentation_ratio, percentage_errors, targets, normalized_total_error)

            for key, set in params_map.items():
                if set in error_dict:
                    error = sum(error_dict[set].values())/len(error_dict[set].values())
                    error_list.append(error)

        return error_list


    def get_experimental_datas(self):
        """
        Reads and organizes experimental data from JSON files.
        """
        datas_exp = {}
        otimization_cond = os.path.join(self.geometry_datas_dir, "defaut\otimizationdatas.json")
        with open(otimization_cond, "r") as info:
            otimization_datas = json.load(info)

        conditions = otimization_datas.get("conditions", {})
        for key, _ in conditions.items():
            if key[0:4] == "cond":
                velocity = conditions[key]["velocity"]
                depth_of_cut = conditions[key]["depth_of_cut"]
                cutting_force = conditions[key]["cutting_force"]
                normal_force = conditions[key]["normal_force"]
                temperature = conditions[key]["temperature"]
                CCR = conditions[key]["CCR"]
                CSR = conditions[key]["CSR"]
                filename = "sim_v{}_h{}".format(velocity, int(depth_of_cut*1000))
                
                datas_exp[filename] = {"cutting_force": cutting_force, "normal_force": normal_force, "temperature": temperature, "CCR": CCR, "CSR": CSR}
        return datas_exp


    def save_iteration_datas(self, condition, parameters, simulated_forces, simulated_temperature, chip_compression_ratio, chip_segmentation_ratio, percentage_errors, targets, normalized_total_error):
        """
        Saves simulation iteration data to an Excel file.
        """
        data = {"Condition": condition,
                "Parameter p": [parameters[0]], "Parameter D2": [parameters[1]], "Parameter Ts": [parameters[2]],
                "Normalized Error": normalized_total_error,
                "Experiment Cutting Force": targets[0], "Simulation Cutting Force": simulated_forces[0], "Error Fc": percentage_errors[0],
                "Experiment Normal Force": targets[1], "Simulation Normal Force": simulated_forces[1], "Error Fn": percentage_errors[1],
                "Experiment Temperature": targets[2], "Simulation Temperature": simulated_temperature, "Error T": percentage_errors[2],
                "Experiment CCR": targets[3], "Simulation CCR": chip_compression_ratio, "Error CCR": percentage_errors[3],
                "Experiment CSR": targets[4], "Simulation CSR": chip_segmentation_ratio, "Error CSR": percentage_errors[4]}
        new_info = pd.DataFrame(data)
        
        data_path = os.path.join(self.excel_dir, "datas.xlsx")

        if os.path.exists(data_path):
            old_df = pd.read_excel(data_path, engine="openpyxl", index_col=0)
            new_df = pd.concat([old_df, new_info], ignore_index=True)
        else:
            new_df = new_info
        
        new_df.index.name = "Simulation"
        new_df.to_excel(data_path, index=True, engine="openpyxl")


    def pso(self, objective_function_pso, lb, ub, swarmsize, omega, phip, phig, maxiter, minstep=1e-6, minfunc=1e-3):
        """
        Particle Swarm Optimization algorithm.
        """
        # Inicialização das partículas
        num_particles = swarmsize
        num_dimensions = len(lb)
        positions = np.random.uniform(low=lb, high=ub, size=(num_particles, num_dimensions))
        velocities = np.random.uniform(low=-1, high=1, size=(num_particles, num_dimensions))

        # Inicialização das melhores posições e melhores scores
        personal_best_positions = np.copy(positions) # contem todas posições iniciais, mesmo numero de elementos que o particle swarm
        personal_best_scores = np.array(objective_function_pso(positions))  # contem o erro de cada particula
        self.call_count_interation += 1

        # Melhor global
        # Aqui pega o menor erro e a particula com menor erro 
        global_best_position = personal_best_positions[np.argmin(personal_best_scores)] # Pega a particula de menor erro
        global_best_score = min(personal_best_scores) # pega o menor erro
        global_best_scores_history = [global_best_score] # copia o menor erro

        PsoManager.show_results(self, global_best_position, global_best_score)

        # PSO Optimization
        for iteration in range(maxiter-1):
            for i in range(num_particles):
                r1, r2 = np.random.rand(), np.random.rand()
                velocities[i] = (omega * velocities[i] + phip * r1 * (personal_best_positions[i] - positions[i]) + phig * r2 * (global_best_position - positions[i]))
                positions[i] += velocities[i] # conjunto de novas particulas 
                positions[i] = np.clip(positions[i], lb, ub) # ajusta os valores fora do limite, tem que ver se isso faz sentido
                
            score = objective_function_pso(positions) # erro de cada iteração feita pelo for
            self.call_count_interation += 1

            for i in range(num_particles):
                if score[i] < personal_best_scores[i]:
                    personal_best_scores[i] = score[i]
                    personal_best_positions[i] = positions[i]
            
                if score[i] < global_best_score:
                    global_best_score = score[i]
                    global_best_position = positions[i]
        
            PsoManager.show_results(self, global_best_position, global_best_score)
            self.call_count_interation += 1
            global_best_scores_history.append(global_best_score) # melhor resultado de cada iteração
            
            print("global_best_score", global_best_score)
            print("global_best_scores_history", global_best_scores_history)

            # Verificar critério de parada
            if global_best_score < minfunc:
                print(f"Critério de parada atingido na iteração {iteration+1}")
                break
        return global_best_position, global_best_score


    def show_results(self, global_best_position, global_best_score):
        """
        Displays the results of the best particle from PSO.
        """
        self.global_best_position = global_best_position
        self.global_best_score = global_best_score

        df = pd.read_excel(os.path.join(self.excel_dir, 'datas.xlsx'))
        mat_row = df[(df['Parameter p'] == np.round(global_best_position[0], 2)) & (df['Parameter D2'] == np.round(global_best_position[1], 2)) & (df['Parameter Ts'] == np.round(global_best_position[2], 2))]
        if not mat_row.empty:
            self.exp_cutting_force = mat_row['Experiment Cutting Force'].values[0]
            self.sim_cutting_force = mat_row['Simulation Cutting Force'].values[0]
            self.error_cutting_force = mat_row['Error Fc'].values[0]
            
            self.exp_normal_force = mat_row['Experiment Normal Force'].values[0]
            self.sim_normal_force = mat_row['Simulation Normal Force'].values[0]
            self.error_normal_force = mat_row['Error Fn'].values[0]
            
            self.exp_temp = mat_row['Experiment Temperature'].values[0]
            self.sim_temp = mat_row['Simulation Temperature'].values[0]
            self.error_temp = mat_row['Error T'].values[0]

            self.exp_CCR = mat_row['Experiment CCR'].values[0]
            self.sim_CCR = mat_row['Simulation CCR'].values[0]
            self.error_CCR = mat_row['Error CCR'].values[0]

            self.exp_CSR = mat_row['Experiment CSR'].values[0]
            self.sim_CSR = mat_row['Simulation CSR'].values[0]
            self.error_CSR = mat_row['Error CSR'].values[0]

            FileUtils.set_text(self, "message-5")
            FileUtils.code_status(self, "iteration")
        else:
            print("Linha não encontrada.")

                