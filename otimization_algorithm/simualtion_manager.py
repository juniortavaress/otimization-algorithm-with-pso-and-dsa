import os
import re
import shutil
import traceback
import json
import numpy as np
import pandas as pd
from file_utils import FileUtils
from get_result_from_odb_file.main_results import getResults

class SimulationManager:
    def __init__(self):
        print("SimulationManager")

    def simulation_manager(self, parameters):
        """
        Manages the simulation workflow: editing input files, running simulations,
        transferring output files, and collecting results.
        """
        self.call_count += 1

        # Step 1: Edit the .inp file
        try:
            FileUtils.set_text(self, "message-3.1")
            for file in os.listdir(self.inp_dir):
                file_path = os.path.join(self.inp_dir, file)
                # print('Simulation_manager // file_path // analisar se precisa do for aqui: ', file_path)
                # print('Simulation_manager // file_path // analisar se precisa do for aqui: ', file)
            lis_dir_inp, index_names = SimulationManager.edit_inp_file(self, file_path, parameters)

            print("\n\n======================== ORDEM DOS PARÂMETROS ========================\n")
            for i, parameter in enumerate(parameters):
                print('Ordem Do Parametros', i, parameter)
            print('Lista de parametros com index', index_names)

        except Exception as e:
            stage = "Editing inp file"
            SimulationManager.except_function(self, stage, e, lis_dir_inp)
            
        # Step 2: Putting compiled files together 
        try:
            SimulationManager.copy_file(self, "CompiledFiles")
        except Exception as e:
            stage = "Transferring compiled files"
            SimulationManager.except_function(self, stage, e)

        # Step 3: Run the simulation
        # import time
        # print('simulando')
        # time.sleep(30)
        try:
            FileUtils.set_text(self, "message-3.2")
            SimulationManager.run_simulation(lis_dir_inp)
        except Exception as e:
            stage = "Rodando Simulação"
            SimulationManager.except_function(self, stage, e, lis_dir_inp)

        # Step 4: Transfer .odb files
        try:
            FileUtils.set_text(self, "message-3.3")
            SimulationManager.copy_file(self, "ODB")
        except Exception as e:
            stage = "Transferring odb files"
            SimulationManager.except_function(self, stage, e)

        # Step 5: Collect simulation results
        try:    
            FileUtils.set_text(self, "message-3.4")
            results = SimulationManager.get_results(self, index_names)
        except Exception as e:
            stage = "Collecting results"
            SimulationManager.except_function(self, stage, e)
        return results


    def edit_inp_file(self, file_path, parameters):
        # edit_inp_file(self, file_path, parameters)
        """
        Edits the .inp file by updating variables from material model.
        """
        lis_dir_inp = []
        index_names = {}
        filename = os.path.basename(file_path)[:-4]

        for j, new_values in enumerate(parameters):
            with open(file_path, 'r') as file:
                lines = file.readlines()

            # Changing D2
            pattern = r"^\*Damage Initiation.*JOHNSON COOK.*"  
            for i, line in enumerate(lines):
                if re.match(pattern, line):
                    values = lines[i + 1].split(',')
                    values[1] = f"{new_values[1]:>7}"   
                    lines[i + 1] = ','.join(values)  
                    break
                
            # Changing p
            pattern = r"^\*Damage Evolution.*"  
            for i, line in enumerate(lines):
                if re.match(pattern, line):
                    start_line = i + 1
                    break
            
            p = new_values[0]
            beta, u_pl = 3.00, 0.01649
            L = np.array([0, 0.0003298, 0.0006596, 0.0009894, 0.0013192, 0.001649, 0.0019788, 0.0023086, 0.0026384, 0.0029682, 0.003298, 0.0036278, 0.0039576, 0.0042874, 0.0046172, 0.004947, 0.0052768, 
                        0.0056066, 0.0059364, 0.0062662, 0.006596, 0.0069258, 0.0072556, 0.0075854, 0.0079152, 0.008245, 0.0085748, 0.0089046, 0.0092344, 0.0095642, 0.009894, 0.0102238, 0.0105536, 
                        0.0108834, 0.0112132, 0.011543, 0.0118728, 0.0122026, 0.0125324, 0.0128622, 0.013192, 0.0135218, 0.0138516, 0.0141814, 0.0145112, 0.014841, 0.0151708, 0.0155006, 0.0158304, 
                        0.0161602, 0.01649])
            D_de = (1 - np.exp(-beta * (L / u_pl))) / (1 - np.exp(-beta)) * p

            for i, value in enumerate(D_de):
                line_index = start_line + i
                values = lines[line_index].split(',')
                values[0] = f"{value:.9f}"
                lines[line_index] = ','.join(values)  
            
            # Changing Ts
            pattern = r"^\*Plastic, hardening=USER*"  
            Ts = new_values[2]
            for i, line in enumerate(lines):
                if re.match(pattern, line):
                    print(line)
                    lines[i] = "*Plastic, hardening=USER, properties=9\n"
                    lines[i+1] = f"1200., 800., 0.4, 0.0121, 0.0002, 0.005, 0.002, 0.0088, \n{Ts}\n"

                    break


            # params = f"{filename}_p_{foat(new_values[0].strip()):.2f}_D2_{float(new_values[1].strip()):.2f}_Ts_{float(new_values[2].strip()):.2f}.inp"
            params = f"{filename}_p_{float(new_values[0]):.2f}_D2_{float(new_values[1]):.2f}_Ts_{float(new_values[2]):.2f}.inp"
            dir_inp = os.path.join(self.inp_and_simulation_dir, params[:-4])
            os.makedirs(dir_inp)

            with open(os.path.join(dir_inp, params), 'w') as file:
                file.writelines(lines)
            lis_dir_inp.append(dir_inp)

            index_names[j] = params[:-4]

        return lis_dir_inp, index_names


    def run_simulation(path_list_to_inp_folders):
        """
        Starts the Abaqus simulation using a parallel processing framework.
        """
        from otimization_algorithm.pararel_simulation import PararelSimulation
        number_of_cores = 4
        number_pararell_sim = 3
        simulation = PararelSimulation
        simulation.startSimulation(simulation, path_list_to_inp_folders, number_of_cores, number_pararell_sim)
        # print('SIMULANDOOO')
        # import time
        # time.sleep(15)

    def copy_file(self, type):
        """
        Transfers .odb files from the simulation directory to the results directory.
        """
        if type == "ODB":
            destination_odb_folder = self.odb_dir
            for folder_name in os.listdir(self.inp_and_simulation_dir):
                folder_path = os.path.join(self.inp_and_simulation_dir, folder_name)
                if os.path.isdir(folder_path) and folder_name.lower() != "defaut":
                    for root, dirs, files in os.walk(folder_path):
                        for file in files:
                            if file.endswith(".odb"):
                                source_path = os.path.join(root, file) 
                                destination_path = os.path.join(destination_odb_folder, file)  
                                shutil.copy2(source_path, destination_path)
                                os.remove(source_path)
        
        elif type == "CompiledFiles":
            self.compiled_files_dir

            for folder_name in os.listdir(self.inp_and_simulation_dir):
                folder_path = os.path.join(self.inp_and_simulation_dir, folder_name)
                if folder_name.lower() != "defaut":
                    source_path_list = ["abaqus_v6.env", "explicitU-D.dll", "explicitU.dll"]
                    for file in source_path_list:
                        source_path = os.path.join(self.compiled_files_dir, file)
                        shutil.copy2(source_path, folder_path)


    def get_results(self, index_names):
        """
        Extracts results from the simulation output files and converts them into a structured format.
        """
        results_dict = {}
        
        results = getResults()
        results.send_odb_path(self.odb_dir)
        results.manage_abaqus_script()
        results.convert_json_to_excel()

        for file in os.listdir(self.odb_dir):
            if file.endswith('.odb'):
                odb_inp_path = os.path.join(self.odb_dir, file)
                odb_out_file = os.path.join(self.odb_processed_dir, file)

                if not os.path.exists(odb_out_file):
                    os.makedirs(odb_out_file)
                shutil.move(odb_inp_path, odb_out_file)

                """GERAR LISTAS DE FILENAME DAS SIMULAÇÕES RODADAS JUNTAS, E CRIAR O DF COM ESSES VALORES JUNTOS
                FORÇAS E TEMPERATURAS DEVEM SER RETORNADAS COMO LISTA DO TAMANHO DA QUANTIDADE DE SIMULAÇÕES RODADAS"""
            
                df = pd.read_excel(os.path.join(self.excel_dir, "Results.xlsx"), header=1)
                filtered_row = df[df["Filename"] == file[:-4]]
                simulated_forces = [filtered_row.iloc[0,3], filtered_row.iloc[0,7]]
                print("\n\n\n\n\n=============================================")
                print("NORMAL FORCE (MEAN OU MAX????)", filtered_row.iloc[0,3])
                print("=============================================\n\n\n\n\n")
                simulated_temperature = filtered_row.iloc[0,9]
                # FileUtils.set_text(self, "message-3.5")

                for index, filename in index_names.items():
                    if filename == file[:-4]:
                        results_dict[index] = {"Filename": filename, "Forces": simulated_forces, "Temperatures": simulated_temperature}
        return results_dict
    

    def except_function(self, stage, e, path='defaut'):
        """
        Handles exceptions by saving error data to a log file and re-raising the exception.
        """
        self.e = e
        json_file = os.path.join(self.current_dir, "error_log_otimization.json")

        error_data = {
            "id": stage,
            "error": str(e),  
            "error_type": str(type(e)),  
            "traceback": traceback.format_exc(),
            "path": path}
        
        with open(json_file, "w") as file:
            json.dump(error_data, file, indent=4)
        raise FileUtils.set_text(self, "message-3.6")
    

if __name__ == "__main__":
    inp_folder = r"S:\Junior\abaqus-with-python\otimization-scripts\otimization-algorithm-with-pso-and-dsa\results-json-excel\inp-and-simulation\defaut\INPFiles"
    for file in os.listdir(inp_folder):
        file_path = os.path.join(inp_folder, file)
    new_values = [0.05, 0.74, -1.45]
    SimulationManager.edit_inp_file(file_path, new_values)