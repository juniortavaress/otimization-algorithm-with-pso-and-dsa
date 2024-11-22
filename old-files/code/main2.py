from values_to_change import *
from run_abaqus import *
from functions import *
from pso_code import *
import numpy as np
from scipy.optimize import minimize

error_threshold, pso_data = initial_config()
experimental_data = get_experimental_data()
positions = initial_particles_position(pso_data)
velocities, p_best, g_best, best_error = get_initial_parameters(experimental_data, pso_data, positions) 
g_best = pso_iterations(pso_data, experimental_data, velocities, p_best, g_best, best_error, positions)


# from functools import partial
# # Inicia o refinamento com o DSA, continuando até que o erro seja menor que o limiar definido
# print("Starting DSA in the subdomain...")
# subdomain_radius = 0.1  # Define a pequena faixa de busca em torno do g_best encontrado pelo PSO
# objective_with_data = partial(objective_function, experimental_data)  # Fixar experimental_data como argumento

# # Loop para continuar o DSA até atingir o erro desejado
# while best_error > error_threshold:
#     # Define os limites do subdomínio para a otimização DSA
#     subdomain_bounds = [(g_best[k] - subdomain_radius, g_best[k] + subdomain_radius) for k in range(5)]
#     # Executa o DSA usando o método Nelder-Mead nos limites definidos
#     result = minimize(objective_with_data, g_best, method='Nelder-Mead', bounds=subdomain_bounds)
    
#     # Atualiza o g_best e o best_error com o resultado do DSA
#     g_best = result.x
#     best_error = result.fun

#     print("DSA - Optimized Parameters:", g_best)
#     print("DSA - Optimized Error:", best_error)

# # Resultado final com os parâmetros otimizados e a simulação
# output = run_abaqus_simulation(g_best[0], g_best[1], g_best[2], g_best[3], g_best[4])
# print("\nFinal Optimized Error:", best_error)
# print("Simulation Output:", output)