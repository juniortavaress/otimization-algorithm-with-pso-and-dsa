import os 
import re
import json
import subprocess
import concurrent.futures

class PararelSimulation():
    def __init__(self):
        super(PararelSimulation, self).__init__()

    def startSimulation(self, list_folder_path, number_of_cores, number_pararell_sim):
        # (simulation, path_list_to_inp_folders, number_of_cores, number_pararell_sim)
        
        self.path = list_folder_path
        self.number_of_cores = number_of_cores
        self.numberFiles = number_pararell_sim

        # PararelSimulation.setup(self)
        PararelSimulation.getINPFile(self)
        PararelSimulation.runSimulations(self)

    # Defining list and paths. Changing directory.
    def setup(self):
        
        pass
        # self.path = os.path.join(self.path_to_save_files ,  'INPFiles')
        
    # Getting all the inp files in the folder
    def getINPFile(self):
        self.inpFiles = []
        
        os.chdir(r"S:\Junior\abaqus-with-python\otimization-scripts\backup\results\inp-and-simulation") 

        for folder_path in self.path:
            if os.path.isdir(folder_path):
                for file in os.listdir(folder_path):
                    if file.endswith('.inp'):
                        # filepath = os.path.join(os.path.basename(folder_path), file)
                        filepath = os.path.join(folder_path, file)
                        self.inpFiles.append(filepath)
        print(self.inpFiles)


    def runSimulations(self):
        self.commands = []

        # Creating the run commands based on the inp files
        for inp in self.inpFiles:
            inp_dir = os.path.dirname(inp)
            command = rf'call C:\SIMULIA\Commands\abq2021.bat job={os.path.basename(inp)[:-4]} cpus={self.number_of_cores} interactive'
            self.commands.append((inp_dir, command))

        for i, command in enumerate(self.commands):
            print('\n', i, command)
        

        def runSimulationAux(inp_dir, command):
            try:
                os.chdir(inp_dir)
                process = subprocess.Popen(command, shell=True)
                process.wait()
            except Exception as e:
                return f"Failed: {command}. Error: {str(e)}"

        # Using ThreadPoolExecutor to manage the queue of simulations
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.numberFiles) as executor:
            # Submit all commands to the executor
            futures = {executor.submit(runSimulationAux, inp_dir, command): command for inp_dir, command in self.commands}


            # Process as they complete
            for future in concurrent.futures.as_completed(futures):
                command = futures[future]
                try:                 
                    result = future.result()
                except Exception as e:
                    print(f"Simulation {command} generated an exception: {e}")
