from otimization_algorithm.pso_algorithm import *
from otimization_algorithm.dsa_algorithm import *
import time
from otimization_algorithm.simualtion_manager import *
import pandas as pd
from file_utils import FileUtils

def main_otimization_manager(self, inp_folder=None):
    print("main_pso_manager")
    FileUtils.set_text(self, "message-2.1")
    initial = time.time()

    # Target values we want to reach
    target_forces = [1044.30, 317.56]  # Target forces in x, y, z directions
    target_temperature = 97.66  # Target temperature
    parameter_bounds = [(0.00, 0.10), (0.50, 1.00), (-2.00, -1.00)]

    FileUtils.set_text(self, "message-2.2")

    start_pso(self, inp_folder, target_forces, target_temperature, parameter_bounds)
    # # start_dsa(target_forces, target_temperature, best_position, objective_function_pso)
    finish_otimization(self, initial)
    print("\n===========================================================================================\n")

def start_pso(self, inp_folder, target_forces, target_temperature, parameter_bounds):
    print("start_pso")

    FileUtils.set_text(self, "message-2.3")
    self.call_count, self.best_position, self.best_score = run_pso(self, inp_folder, target_forces, target_temperature, parameter_bounds)
    print("Optimized Parameters:", [f"{param}: {value:.3f}" for param, value in zip(['D1', 'D2', 'D3'], self.best_position)])
    print("Optimized Error:", self.best_score, '\n')

    target_values = self.best_position
    data_path = os.path.join(self.excel_dir, "datas.xlsx")
    datas = pd.read_excel(data_path)

    self.filtered_rows = datas[(datas['Parameter D1'].round(2) == target_values[0].round(2)) & 
                          (datas['Parameter D2'].round(2) == target_values[1].round(2)) & 
                          (datas['Parameter D3'].round(2) == target_values[2].round(2))]

    FileUtils.set_text(self, "message-2.4")
    

def start_dsa():
    # Runninf DSA Algorithm
    # run_dsa(target_forces, target_temperature, best_position, objective_function_pso)
    print("\n\n===========================================================================================\n\n")

def finish_otimization(self, initial):
    print("finish_otimization")

    self.duration = (time.time()) - initial
    days = self.duration // (24 * 3600)  # Número de dias
    hours = (self.duration % (24 * 3600)) // 3600  # Horas restantes
    minutes = (self.duration % 3600) // 60  # Minutos restantes
    seconds = self.duration % 60  # Segundos restantes

    self.formatted_duration = f"{int(days)} dias, {int(hours)}h, {int(minutes)}m e {int(seconds)}s"

    FileUtils.set_text(self, "message-2.5")

if __name__ == "__main__":
    inp_folder = r"S:\Junior\abaqus-with-python\otimization-scripts\otimization-algorithm-with-pso-and-dsa\auxiliary\INPFiles"
    main_otimization_manager(inp_folder)