from pso import *
from dsa import *
import time
from functions import *

initial = time.time()
if os.path.exists("datas.xlsx"):
    os.remove("datas.xlsx")

# Target values we want to reach
target_forces = [1010.0, 1160.0]  # Target forces in x, y, z directions
target_temperature = 1855.0  # Target temperature
parameter_bounds = [(300, 700), (350, 750), (0.005, 0.150), (0.1, 0.9), (0.1, 0.85)]


print("\n===========================================================================================\n")

# Running PSO Algorithm
print("Starting PSO optimization with pyswarm...")
best_position, best_score = run_pso(target_forces, target_temperature, parameter_bounds)
print("Optimized Parameters:", [f"{param}: {value:.3f}" for param, value in zip(['A', 'B', 'C', 'n', 'm'], best_position)])
print("Optimized Error:", best_score, '\n')

simulated_forces, simulated_temperature, call_count = run_simulation(best_position)
print('Number of Simulations:', call_count)
print('Cutting Force from Simulation:', simulated_forces[0].round(2))
print('Cutting Normal from Simulation:', simulated_forces[1].round(2))
print('Temperature from Simulation:',  simulated_temperature.round(2))

print("\n===========================================================================================\n")

# Runninf DSA Algorithm
# run_dsa(target_forces, target_temperature, best_position, objective_function_pso)

# print("\n\n===========================================================================================\n\n")

end = time.time()
print('time running:', end - initial)