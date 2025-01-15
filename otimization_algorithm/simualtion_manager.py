import os
import re
import shutil
import traceback
import json
import time
import numpy as np
import pandas as pd
from file_utils import FileUtils
from get_result_from_odb_file.main_results import getResults
import uuid

class SimulationManager:
    def __init__(self):
        print("SimulationManager")

    def simulation_manager(self, parameters):
        """
        Manages the simulation workflow: editing input files, running simulations,
        transferring output files, and collecting results.
        """
        results = []

        # Step 1: Edit the .inp file
        try:
            FileUtils.set_text(self, "message-id_09")
            lis_dir_inp, index_names = SimulationManager.edit_inp_file(self, parameters)
        except Exception as e:
            self.error_track = True
            stage = "Editing inp file"
            SimulationManager.except_function(self, stage, e)
            
        # Step 2: Putting compiled files together 
        if not self.error_track:
            try:
                SimulationManager.copy_file(self, "CompiledFiles")
            except Exception as e:
                stage = "Transferring compiled files"
                SimulationManager.except_function(self, stage, e)

        # Step 3: Creating list for computer 2
        if not self.error_track:
            division = len(lis_dir_inp)//2
            lis_dir_inp_comp01 = lis_dir_inp[:division]
            lis_dir_inp_comp02 = lis_dir_inp[division:]

            status_file = os.path.join(self.status_dir, "status_file.json")
            with open(status_file, 'r') as json_file:
                existing_data = json.load(json_file)

            existing_data["Simulation-list-pc2"] = {"status": True, "list_comp_02": lis_dir_inp_comp02}

            with open(status_file, "w") as file:
                json.dump(existing_data, file, indent=4)

        # Step 4: Run the simulation
        if not self.error_track:
            try:
                id = "cp1"
                FileUtils.set_text(self, "message-id_10")
                SimulationManager.run_simulation(id, lis_dir_inp_comp01)
            except Exception as e:
                self.error_track = True
                stage = "Rodando Simulação"
                SimulationManager.except_function(self, stage, e)


        while True:
            with open(status_file, "r") as file:
                data = json.load(file)

            if data["Simulation-list-pc2"]["status"] == False:    
                break
            else:
                time.sleep(10)


        # Step 5: Transfer .odb files
        if not self.error_track:
            try:
                FileUtils.set_text(self, "message-id_11")
                SimulationManager.copy_file(self, "ODB")
            except Exception as e:
                self.error_track = True
                stage = "Transferring odb files"
                SimulationManager.except_function(self, stage, e)

        # Step 6: Collect simulation results
        if not self.error_track:
            try:    
                FileUtils.set_text(self, "message-id_12")
                results = SimulationManager.get_results(self, index_names)
            except Exception as e:
                self.error_track = True
                stage = "Collecting results"
                SimulationManager.except_function(self, stage, e)
        return results


    def edit_inp_file(self, parameters):
        """
        Edits the .inp file by updating variables from material model.
        """
        lis_dir_inp = []
        index_names = {}
        global_index = 0
        
        print("\n\n=======================================\n\nPARAMETROS", parameters, "\n\n=======================================\n\n")
        for file in os.listdir(self.inp_dir):
            file_path = os.path.join(self.inp_dir, file)
            filename = os.path.basename(file_path)[:-4]

            for new_values in parameters:
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
                        lines[i] = "*Plastic, hardening=USER, properties=9\n"
                        # A, B, n,  C1, C2, C3, EQPLAS_Zero, k, Ts
                        lines[i+1] = f"1200., 1284., 0.54, 0.0121, 0.0002, 0.005, 0.002, 0.0088, \n{Ts}\n"
                        break

                # Saving
                params = f"{filename}_p_{float(new_values[0]):.2f}_D2_{float(new_values[1]):.2f}_Ts_{float(new_values[2]):.2f}.inp"
                dir_inp = os.path.join(self.inp_and_simulation_dir, params[:-4])

                if not os.path.exists(dir_inp):
                    os.makedirs(dir_inp)
                    with open(os.path.join(dir_inp, params), 'w') as file:
                        file.writelines(lines)
                    lis_dir_inp.append(dir_inp)

                else:
                    dir_inp = os.path.join(self.inp_and_simulation_dir, params[:-4] + '_' + str(uuid.uuid4()))
                    os.makedirs(dir_inp)
                    with open(os.path.join(dir_inp, params), 'w') as file:
                        file.writelines(lines)
                    lis_dir_inp.append(dir_inp)
                    print("\n\n\n\n============================= O CODIGO MANDOU PARAMETROS REPETIDOS =============================\n\n\n\n")

                index_names[global_index] = params[:-4]
                global_index += 1

        return lis_dir_inp, index_names


    def run_simulation(id, path_list_to_inp_folders):
        """
        Starts the Abaqus simulation using a parallel processing framework.
        """
        # from otimization_algorithm.pararel_simulation import PararelSimulation
        # number_of_cores = 4
        # number_pararell_sim = 3
        # simulation = PararelSimulation
        # simulation.start_simulation(simulation, id, path_list_to_inp_folders, number_of_cores, number_pararell_sim)
        x = input("coloca as simulações ai meu bom!")


    def copy_file(self, type):
        """
        Transfers .odb files from the simulation directory to the results directory.
        """
        if type == "ODB":
            # PARA OS FOLDERS COMP01_DATA E COMP02_DATA
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
            for folder_name in os.listdir(self.inp_and_simulation_dir):
                folder_path = os.path.join(self.inp_and_simulation_dir, folder_name)
                if folder_name.lower() != "defaut" and folder_name.lower() != "info":
                    source_path_list = ["abaqus_v6.env", "explicitU-D.dll", "explicitU.dll"]
                    for file in source_path_list:
                        source_path = os.path.join(self.compiled_files_dir, file)
                        shutil.copy2(source_path, folder_path)


    def get_results(self, index_names):
        """
        Extracts results from the simulation output files and converts them into a structured format.
        """
        results_dict = {}
        getResults.manage_abaqus_script(self)
        # x = input("coloca a temp ai")
        getResults.convert_json_to_excel(self)

        for file in os.listdir(self.odb_dir):
            if file.endswith('.odb'):
                self.call_count += 1
                odb_inp_path = os.path.join(self.odb_dir, file)
                odb_out_file = os.path.join(self.odb_processed_dir, file)

                if not os.path.exists(odb_out_file):
                    os.makedirs(odb_out_file)
                shutil.move(odb_inp_path, odb_out_file)
            
                df_temp_force = pd.read_excel(os.path.join(self.excel_dir, "Results.xlsx"), header=1)
                filtered_row = df_temp_force[df_temp_force["Filename"] == file[:31]]
                self.simulated_forces = [filtered_row.iloc[0,7], filtered_row.iloc[0,3]]
                self.simulated_temperature = filtered_row.iloc[0,9]

                df_chip = pd.read_excel(os.path.join(self.excel_dir, "Results_chip_analysis.xlsx"), header=0)
                filtered_row = df_chip[df_chip["Filename"] == file[:-4]]
                self.chip_compression_ratio = filtered_row.iloc[0,5]
                self.chip_segmentation_ratio = filtered_row.iloc[0,6]

                # self.chip_compression_ratio, self.chip_segmentation_ratio = 1, 1

                FileUtils.set_text(self, "message-id_13")

                for index, filename in index_names.items():
                    if filename == file[:-4]:
                        results_dict[index] = {"Filename": filename, "Forces": self.simulated_forces, "Temperatures": self.simulated_temperature, "CCR": self.chip_compression_ratio, "CSR": self.chip_segmentation_ratio}
        return results_dict
    

    def except_function(self, stage, e):
        """
        Handles exceptions by saving error data to a log file and re-raising the exception.
        """
        self.e = e
        self.stage = stage
        FileUtils.code_status(self, "iteration-error")
        FileUtils.set_text(self, "message-ide_07")
    

