from pso import *
from dsa import *
import time
from functions import *
import pandas as pd

def main_pso_manager(inp_folder=None):
    print("INICIO DA OTIMIZAÇÃO\n")

    initial = time.time()
    if os.path.exists("datas.xlsx"):
        os.remove("datas.xlsx")

    main_dir_inp_defaut = os.path.dirname(os.path.dirname(inp_folder))
    
    print('----')
    print('Excluindo arquivos .inp antigos...')
    for folder_name in os.listdir(main_dir_inp_defaut):
        folder_path = os.path.join(main_dir_inp_defaut, folder_name)
        if os.path.isdir(folder_path) and folder_name != "defaut":
            # print(f"Removing folder: {folder_path}")
            shutil.rmtree(folder_path)  # Remove a pasta

    # Target values we want to reach
    target_forces = [1044.30, 317.56]  # Target forces in x, y, z directions
    target_temperature = 97.66  # Target temperature
    parameter_bounds = [(0.00, 0.10), (0.50, 1.00), (-2.00, -1.00)]

    print('Chamando gerenciador do pso...')
    print('----')
    start_pso(inp_folder, target_forces, target_temperature, parameter_bounds)
    # # start_dsa(target_forces, target_temperature, best_position, objective_function_pso)
    finish_otimization(initial)
    print("\n===========================================================================================\n")

def start_pso(inp_folder, target_forces, target_temperature, parameter_bounds):
    # Running PSO Algorithm
    print("\nStarting PSO optimization with pyswarm...\n")
    call_count, best_position, best_score = run_pso(inp_folder, target_forces, target_temperature, parameter_bounds)
    print("Optimized Parameters:", [f"{param}: {value:.3f}" for param, value in zip(['D1', 'D2', 'D3'], best_position)])
    print("Optimized Error:", best_score, '\n')

    # simulated_forces, simulated_temperature, call_count = run_simulation(best_position)

    target_values = best_position
    main_dir = (os.path.dirname(inspect.getfile(inspect.currentframe()))) 
    data_path = os.path.join(main_dir, "datas.xlsx")
    datas = pd.read_excel(data_path)

    filtered_rows = datas[(datas['Parameter D1'].round(2) == target_values[0].round(2)) & 
                          (datas['Parameter D2'].round(2) == target_values[1].round(2)) & 
                          (datas['Parameter D3'].round(2) == target_values[2].round(2))]

    print('Number of Simulations:', call_count)
    print('Cutting Force from Simulation:', filtered_rows["Simulation Cutting Force"].round(2).values[0])
    print('Cutting Normal from Simulation:', filtered_rows["Simulation Normal Force"].round(2).values[0])
    print('Temperature from Simulation:',  filtered_rows["Simulation Temperature"].round(2).values[0])

    print("\n===========================================================================================\n")

def start_dsa():
    # Runninf DSA Algorithm
    # run_dsa(target_forces, target_temperature, best_position, objective_function_pso)
    print("\n\n===========================================================================================\n\n")

def finish_otimization(initial):
    end = time.time()
    print('time running:', end - initial)

if __name__ == "__main__":
    inp_folder = r"S:\Junior\abaqus-with-python\otimization-scripts\otimization-algorithm-with-pso-and-dsa\auxiliary\INPFiles"
    main_pso_manager(inp_folder)