import os
import re
import shutil
import traceback
import json
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
                print('Simulation_manager // file_path // analisar se precisa do for aqui: ', file_path)
                print('Simulation_manager // file_path // analisar se precisa do for aqui: ', file)
            dir_inp = SimulationManager.edit_inp_file(self, file_path, parameters)
        except Exception as e:
            stage = "Editing inp file"
            SimulationManager.except_function(self, stage, e, dir_inp)
            
        # Step 2: Run the simulation
        try:
            FileUtils.set_text(self, "message-3.2")
            SimulationManager.run_simulation(dir_inp)
        except Exception as e:
            stage = "Rodando Simulação"
            SimulationManager.except_function(self, stage, e, dir_inp)
        # print('simulando')
        # import time
        # time.sleep(15)
        
        # Step 3: Transfer .odb files
        try:
            FileUtils.set_text(self, "message-3.3")
            destination_path = SimulationManager.copy_odb_file(self)
        except Exception as e:
            stage = "Transferring odb files"
            SimulationManager.except_function(self, stage, e, destination_path)

        # Step 4: Collect simulation results
        try:    
            FileUtils.set_text(self, "message-3.4")
            print(destination_path)
            SimulationManager.get_results(self, destination_path, os.path.basename(dir_inp))
        except Exception as e:
            stage = "Collecting results"
            SimulationManager.except_function(self, stage, e, destination_path)

        return self.simulated_forces, self.simulated_temperature


    def edit_inp_file(self, file_path, new_values):
        """
        Edits the .inp file by updating variables from material model.
        """
        with open(file_path, 'r') as file:
            lines = file.readlines()
        pattern = r"^\*Damage Initiation.*JOHNSON COOK.*"  
        for i, line in enumerate(lines):
            if re.match(pattern, line):
                values = lines[i + 1].split(',')
                values[0] = f"{new_values[0]:>5}"  
                values[1] = f"{new_values[1]:>7}"   
                values[2] = f"{new_values[2]:>7}" 
                lines[i + 1] = ','.join(values)  
                break  

        # Saving info
        # dir_inp = S:\Junior\abaqus-with-python\otimization-scripts\otimization-algorithm-with-pso-and-dsa\results\inp-and-simulation\sim_D1_0.09_D2_0.95_D3_-1.56
        filename = os.path.basename(file_path)[:-4]
        params = f"{filename}_D1_{float(values[0].strip()):.2f}_D2_{float(values[1].strip()):.2f}_D3_{float(values[2].strip()):.2f}.inp"
        dir_inp = os.path.join(self.inp_and_simulation_dir, params[:-4])
        os.makedirs(dir_inp)
        with open(os.path.join(dir_inp, params), 'w') as file:
            file.writelines(lines)
        return dir_inp


    def run_simulation(path_to_inp_folder):
        """
        Starts the Abaqus simulation using a parallel processing framework.
        """
        from otimization_algorithm.pararel_simulation import PararelSimulation
        simulation = PararelSimulation
        number_of_cores = 4
        simulation.startSimulation(simulation, path_to_inp_folder, number_of_cores)
        # print('SIMULANDOOO')
        # import time
        # time.sleep(15)

    def copy_odb_file(self):
        """
        Transfers .odb files from the simulation directory to the results directory.
        """
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
        return destination_path


    def get_results(self, odb_path, filename_to_search):
        """
        Extracts results from the simulation output files and converts them into a structured format.
        """
        for file in os.listdir(os.path.dirname(odb_path)):
            if file.endswith('.odb'):
                results = getResults()
                results.send_odb_path(os.path.dirname(odb_path))
                results.manage_abaqus_script()
                results.convert_json_to_excel()

                filename = os.path.basename(odb_path)
                print("----------------\n", "file", file, "\nfilename", filename)
                odb_out_file = os.path.join(self.odb_processed_dir, filename)

                if not os.path.exists(odb_out_file):
                    os.makedirs(odb_out_file)
                shutil.move(odb_path, odb_out_file)

        """GERAR LISTAS DE FILENAME DAS SIMULAÇÕES RODADAS JUNTAS, E CRIAR O DF COM ESSES VALORES JUNTOS
        FORÇAS E TEMPERATURAS DEVEM SER RETORNADAS COMO LISTA DO TAMANHO DA QUANTIDADE DE SIMULAÇÕES RODADAS"""
        
        df = pd.read_excel(os.path.join(self.excel_dir, "Results.xlsx"), header=1)
        print('df', df)
        # print('filename_to_search', filename_to_search, filename_to_search[:-4])
        filtered_row = df[df["Filename"] == filename[:-4]]
        print(filename[:-4])
        print('filtered_row', filtered_row)
        self.simulated_forces = [filtered_row.iloc[0,3], filtered_row.iloc[0,7]]
        self.simulated_temperature = filtered_row.iloc[0,9]
        FileUtils.set_text(self, "message-3.5")


    def except_function(self, stage, e, path):
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