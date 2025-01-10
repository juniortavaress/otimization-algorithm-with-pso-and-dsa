import os 
import re
import json
import subprocess
import concurrent.futures
import psutil
import time

class PararelSimulation():
    def __init__(self):
        super(PararelSimulation, self).__init__()

    def start_simulation(self, id, list_folder_path, number_of_cores, number_pararell_sim):  
        """
        Start the simulation process by retrieving input files 
        and running simulations in parallel.

        Args:
            list_folder_path (list): List of folder paths containing .inp files.
            number_of_cores (int): Number of CPU cores to use for each simulation.
            number_parallel_sim (int): Number of parallel simulations to run.
        """   

        for i, file in enumerate(list_folder_path):
            print(id, file)  
        
        self.path = list_folder_path
        self.number_of_cores = number_of_cores
        self.numberFiles = number_pararell_sim

        PararelSimulation.getINPFile(self)
        PararelSimulation.runSimulations(self)
        

    def getINPFile(self):
        """
        Retrieve all .inp files from the provided directories.

        This method scans each folder in the provided list of paths and 
        collects the full paths of files with the `.inp` extension.
        """
        self.inpFiles = []

        for folder_path in self.path:
            if os.path.isdir(folder_path):
                for file in os.listdir(folder_path):
                    if file.endswith('.inp'):
                        filepath = os.path.join(folder_path, file)
                        self.inpFiles.append(filepath)
        # print(self.inpFiles)


    def runSimulations(self):
        """
        Run the Abaqus simulations in parallel.

        Each simulation command is constructed based on the input files, 
        and simulations are executed concurrently using a thread pool executor.
        """

        self.commands = []

        # Creating the run commands based on the inp files
        for inp in self.inpFiles:
            inp_dir = os.path.dirname(inp)
            command = rf'call C:\SIMULIA\Commands\abq2021.bat job={os.path.basename(inp)[:-4]} cpus={self.number_of_cores} interactive'
            self.commands.append((inp_dir, command))

        # for i, command in enumerate(self.commands):
        #     print('\n', i, command)
        

        def runSimulationAux(inp_dir, command):
            retries = 3
            job_name = command.split('job=')[1].split()[0]
            output_file = os.path.join(inp_dir, f"{job_name}.odb")

            for attempt in range(1, retries + 1):
                try:
                    os.chdir(inp_dir)
                    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

                    stdout, stderr = process.communicate()
                    print(f"stdout: {stdout.decode()}\n", f"stderr: {stderr.decode()}\n")
                    process.wait()                    

                    if os.path.exists(output_file):
                        print("Simulation completed successfully: {}".format(output_file))
                        return "Success"
                    else:
                        print("Output file not found for {}. Retrying...".format(job_name))

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
