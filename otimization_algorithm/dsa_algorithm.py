from otimization_algorithm.simualtion_manager import *
from scipy.optimize import minimize

def run_dsa(target_forces, target_temperature, best_position, objective_function_pso):
    # Refinement using the Downhill Simplex Algorithm (DSA) if PSO conditions are met
    print("Starting DSA refinement in the subdomain...")
    subdomain_radius_min = 0.95
    subdomain_radius_max = 1.05
    # Set bounds for DSA around the global best parameters
    subdomain_bounds = [(best_position[k] * subdomain_radius_min, best_position[k] * subdomain_radius_max) for k in range(5)]

    # Run DSA using the Nelder-Mead method within defined bounds
    result = minimize(objective_function_pso, best_position, method='Nelder-Mead', bounds=subdomain_bounds, options={'xatol': 1e-1, 'maxiter': 150})
    print("DSA - Optimized Parameters:", [f"{param:.3f}" for param in result.x])
    print("DSA - Optimized Error:", result.fun)

    # Get simulated results with the optimized parameters
    best_forces_dsa, best_temperature_dsa, call_count = run_simulation(result.x)
    print("\nForces calculated with the optimized parameters:", best_forces_dsa)
    print("Temperature calculated with the optimized parameters:", best_temperature_dsa)

    # Calculate percentage errors after DSA
    force_errors_dsa = [(abs(target - best) / target) * 100 for target, best in zip(target_forces, best_forces_dsa)]
    temperature_error_dsa = abs(target_temperature - best_temperature_dsa) / target_temperature * 100

    print("\nPercentage errors after DSA:")
    print("Force errors (x, y, z):", force_errors_dsa)
    print("Temperature error:", temperature_error_dsa)
    print("\nNumero de simulações PSO + DSA:", call_count)