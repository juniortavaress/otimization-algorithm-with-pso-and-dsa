import numpy as np
import matplotlib.pyplot as plt
from functions import *
from scipy.optimize import minimize

# Target values we want to reach
target_forces = [1010.0, 1160.0, 1010.0]  # Target forces in x, y, z directions
target_temperature = 1855.0  # Target temperature
parameter_bounds = [(300, 700), (350, 750), (0.005, 0.150), (0.1, 0.9), (0.1, 0.85)]

# PSO parameters
num_particles = 5
num_dimensions = 5  # Parameters: A, B, C, n, m
num_iterations = 100
w = 0.5
c1 = 1.5
c2 = 1.5
tolerance = 1.0  # Tolerance for stopping criterion in percentage

# Particle initialization
positions = np.random.uniform(low=[b[0] for b in parameter_bounds], high=[b[1] for b in parameter_bounds], size=(num_particles, num_dimensions))
velocities = np.random.uniform(low=-1, high=1, size=(num_particles, num_dimensions))
personal_best_positions = np.copy(positions)
personal_best_scores = np.array([objective_function(p, target_forces, target_temperature) for p in positions])
global_best_position = personal_best_positions[np.argmin(personal_best_scores)]
global_best_score = min(personal_best_scores)

global_best_scores_history = [global_best_score]

force_errors_list = []
temperature_error_list = []

# PSO optimization
for iteration in range(num_iterations):
    for i in range(num_particles):
        r1, r2 = np.random.rand(), np.random.rand()
        velocities[i] = (w * velocities[i] +
                         c1 * r1 * (personal_best_positions[i] - positions[i]) +
                         c2 * r2 * (global_best_position - positions[i]))
        
        positions[i] += velocities[i]
        positions[i] = np.clip(positions[i], [b[0] for b in parameter_bounds], [b[1] for b in parameter_bounds])

        # Evaluate the objective function
        score = objective_function(positions[i], target_forces, target_temperature)
        
        # Update personal and global best
        if score < personal_best_scores[i]:
            personal_best_scores[i] = score
            personal_best_positions[i] = positions[i]

        if score < global_best_score:
            global_best_score = score
            global_best_position = positions[i]
    
    global_best_scores_history.append(global_best_score)
    
    # Calculate current percentage errors with the best parameters
    best_forces, best_temperature, call_count = run_simulation(global_best_position)
    force_errors = [(abs(target - best) / target) * 100 for target, best in zip(target_forces, best_forces)]
    temperature_error = abs(target_temperature - best_temperature) / target_temperature * 100

    force_errors_list.append(force_errors)
    temperature_error_list.append(temperature_error)

    # Check if all errors are below tolerance
    if all(error < tolerance for error in force_errors) and temperature_error < tolerance:
        print(f"\nStopping criterion reached at iteration {iteration+1}")
        print(f"Error at iteration {iteration+1}: {global_best_score}")
        print("Percentage errors in forces (x, y, z):", force_errors)
        print("Percentage error in temperature:", temperature_error)
        break

print("\nBest position (parameters):", global_best_position)
print("Minimum obtained error:", global_best_score)
print("Forces calculated with the best parameters:", best_forces)
print("Temperature calculated with the best parameters:", best_temperature)
print("Final percentage errors in forces (x, y, z):", force_errors)
print("Final percentage error in temperature:", temperature_error)

print('Number of simulations:', call_count)

# Converting error lists to numpy format for easier plotting
force_errors_array = np.array(force_errors_list)
temperature_errors_array = np.array(temperature_error_list)

# Plotting the evolution of errors for each force and temperature
plt.figure(figsize=(12, 8))

plt.plot(force_errors_array[:, 0], label="Force Error in x (%)", marker='o', linestyle='-')
plt.plot(force_errors_array[:, 1], label="Force Error in y (%)", marker='o', linestyle='-')
plt.plot(force_errors_array[:, 2], label="Force Error in z (%)", marker='o', linestyle='-')
plt.plot(temperature_errors_array, label="Temperature Error (%)", marker='o', linestyle='-')

plt.xlabel("Iteration")
plt.ylabel("Percentage Error (%)")
plt.title("Evolution of Percentage Errors for Forces and Temperature in PSO")
plt.legend()
plt.grid(True)
plt.show()




# Refinement using the Downhill Simplex Algorithm (DSA) if PSO conditions are met
print("\n\n\nStarting DSA in the subdomain...")
subdomain_radius_min = 0.95  # Define a small search range around the global best found by PSO
subdomain_radius_max = 1.05
# Set bounds for DSA around the global best parameters
subdomain_bounds = [(global_best_position[k] - subdomain_radius_min, global_best_position[k] + subdomain_radius_max) for k in range(5)]

# Wrap objective_function with additional arguments
objective_function_dsa = lambda params: objective_function(params, target_forces, target_temperature)

# Run DSA using the Nelder-Mead method within defined bounds
result = minimize(objective_function_dsa, global_best_position, method='Nelder-Mead', bounds=subdomain_bounds, options={'xatol': 1e-6, 'maxiter': 150})
print("DSA - Optimized Parameters:", result.x)
print("DSA - Optimized Error:", result.fun)

# Get simulated results with the optimized parameters
best_forces_dsa, best_temperature_dsa, call_count = run_simulation(result.x)
print("Forces calculated with the optimized parameters:", best_forces_dsa)
print("Temperature calculated with the optimized parameters:", best_temperature_dsa)

# Calculate percentage errors after DSA
force_errors_dsa = [(abs(target - best) / target) * 100 for target, best in zip(target_forces, best_forces_dsa)]
temperature_error_dsa = abs(target_temperature - best_temperature_dsa) / target_temperature * 100

print("\nPercentage errors after DSA:")
print("Force errors (x, y, z):", force_errors_dsa)
print("Temperature error:", temperature_error_dsa)

print('Number of simulations:', call_count)