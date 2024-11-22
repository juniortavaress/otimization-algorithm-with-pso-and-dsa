import numpy as np
from scipy.optimize import minimize

# --------- Initial Configurations ---------
error_threshold = 0.01  # Desired error limit: 1% (0.01 in fractional terms)
min_iterations_pso = 10 # Minimum number of PSO iterations before switching to DSA
n_particles = 20        # Number of particles in the PSO
w = 0.5                 # Inertia coefficient for PSO
c1 = 1.5                # Cognitive coefficient (attraction to particle's best-known position)
c2 = 1.5                # Social coefficient (attraction to global best position)


# Experimental data (replace with actual values)
experimental_data = {
    'cutting_force': 3,
    'normal_cutting_force': 1,
    'chip_thickness': 0.5,
    'chip_radius': 0.3,
    'surface_temperature': 1.5,
}


# Simulated Abaqus function for example purposes
def run_abaqus_simulation(A, B, C, m, n):

    """This function represents the model to be optimized. It takes five parameters (A, B, C, m, and n) and returns simulated values 
    for the same output variables present in the experimental data. In the code, this function was simplified, but in practice, 
    it would perform a simulation using Abaqus software and return the results."""

    simulated_data = {
        'cutting_force': (A * 1.1 + B * 0.5 - C * 0.3) / 200,
        'normal_cutting_force': (B * 0.7 + A * 0.2 + n * 0.3) / 50,
        'chip_thickness': (m * 0.05 + n * 0.03) / 0.5,
        'chip_radius': (A * 0.01 + C * 0.04) / 0.3,
        'surface_temperature': (A * 1.5 - m * 0.8 + n * 0.5) / 150
    }
    return simulated_data


# Objective function to calculate the error between simulated and experimental data
def objective_function(params):
    A, B, C, m, n = params
    simulated_data = run_abaqus_simulation(A, B, C, m, n)
    # Calculating the sum of squared differences between experimental and simulated data
    error = sum((experimental_data[key] - simulated_data[key]) ** 2 for key in experimental_data)
    # print(error)
    return error


# Initialize particles and velocities for PSO
positions = np.random.uniform(-50, 50, (n_particles, 5)) # Randomly initialize particle positions within a wide range
velocities = np.random.rand(n_particles, 5) * 10         # Initialize velocities with moderate range
p_best = positions.copy()                                # Track the best-known position of each particle
g_best = positions[np.argmin([objective_function(pos) for pos in positions])] # Find the global best initial position
best_error = objective_function(g_best)                  # Calculate error for the global best position
print(best_error)


# PSO main loop with a stopping condition (error < 1% or at least 10 iterations)
iteration = 0
while iteration < min_iterations_pso:
    print(f"PSO - Iteration {iteration + 1}, Best Error: {best_error}")
    for j in range(n_particles):
        r1, r2 = np.random.rand(), np.random.rand()  # Generate random values for PSO update
        # Update particle velocity based on inertia, cognitive, and social factors
        velocities[j] = (w * velocities[j] + c1 * r1 * (p_best[j] - positions[j]) + c2 * r2 * (g_best - positions[j]))
        # Update particle position based on new velocity
        positions[j] += velocities[j]
        
        # Update best-known position of the particle if the new position gives a lower error
        current_error = objective_function(positions[j])
        if current_error < objective_function(p_best[j]):
            p_best[j] = positions[j]
        # Update global best position if the current particle's error is the lowest found so far
        if current_error < best_error:
            g_best = positions[j]
            best_error = current_error
    
    iteration += 1  # Increment iteration counter

print("PSO - Global Best Parameters:", g_best)
print("PSO - Global Best Error:", best_error)

# Refinement using the Downhill Simplex Algorithm (DSA) if PSO conditions are met
print("Starting DSA in the subdomain...")
subdomain_radius = 0.05  # Define a small search range around the global best found by PSO
# Set bounds for DSA around the global best parameters
subdomain_bounds = [(g_best[k] - subdomain_radius, g_best[k] + subdomain_radius) for k in range(5)]
# Run DSA using the Nelder-Mead method within defined bounds
result = minimize(objective_function, g_best, method='Nelder-Mead', bounds=subdomain_bounds)
print("DSA - Optimized Parameters:", result.x)
print("DSA - Optimized Error:", result.fun)

A, B, C, m, n = result.x
simulated_data = run_abaqus_simulation(A, B, C, m, n)
print(simulated_data)