import os 
import json
import subprocess
import concurrent.futures

class PararelSimulation():
    def __init__(self):
        super(PararelSimulation, self).__init__()

    def startSimulation(self, folder_path, cores):
        self.numberFiles = 1
        self.path = folder_path
        self.number_of_cores = cores
        PararelSimulation.setup(self)
        PararelSimulation.getINPFile(self)
        PararelSimulation.runSimulations(self)

    # Defining list and paths. Changing directory.
    def setup(self):
        self.inpFiles = []
        self.commands = []
        # self.path = os.path.join(self.path_to_save_files ,  'INPFiles')
        os.chdir(self.path) 

    # Getting all the inp files in the folder
    def getINPFile(self):
        for file in os.listdir(self.path):
            if file.endswith('.inp'):
                self.inpFiles.append(file)

    def runSimulations(self):
        # Creating the run commands based on the inp files
        for inp in self.inpFiles:
            command = rf'call C:\SIMULIA\Commands\abq2021.bat job={inp[:-4]} cpus={self.number_of_cores} interactive'
            print('->',command, '\n')
            print('============= ABAQUS OUTPUT =============')
            self.commands.append(command)

        def runSimulationAux(command):
            try:
                process = subprocess.Popen(command, shell=True)
                process.wait()
            except Exception as e:
                return f"Failed: {command}. Error: {str(e)}"

        # Using ThreadPoolExecutor to manage the queue of simulations
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.numberFiles) as executor:
            # Submit all commands to the executor
            futures = {executor.submit(runSimulationAux, command): command for command in self.commands}

            # Process as they complete
            for future in concurrent.futures.as_completed(futures):
                command = futures[future]
                try:
                    result = future.result()
                except Exception as e:
                    print(f"Simulation {command} generated an exception: {e}")
