import os
import sys
import json
import time

class Computer02():
    def __init__(self):
        print("======================================")
        print("\nINITIALIZING THE CODE AT COMPUTER 02\n")
        print("======================================\n")

    def run_simulations(self):           
        # Add Paths to sys
        sys.path.append(os.getcwd())

        # Getting Paths
        from file_utils import FileUtils
        file = FileUtils() 
        file.create_folders(self)

        while True:
            info_pc02 = os.path.join(self.status_dir, "status_file.json")

            with open(info_pc02, "r") as file:
                data = json.load(file)

            list_comp_02 = data["Simulation-list-pc2"]["list_comp_02"]
            # print(list_comp_02)

            try:
                if data["Simulation-list-pc2"]["status"] == True:
                    id = "cp2"
                    from otimization_algorithm.pararel_simulation import PararelSimulation
                    simulation = PararelSimulation
                    simulation.start_simulation(simulation, id, list_comp_02, number_of_cores = 4, number_pararell_sim = 3)

                print("status", data["Simulation-list-pc2"]["status"])
                data["Simulation-list-pc2"]["status"] = False
                with open(info_pc02, "w") as file:
                    json.dump(data, file, indent=4)
            except:
                pass

            time.sleep(600)  

if __name__ == "__main__":
    cp = Computer02()
    cp.run_simulations()