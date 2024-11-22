from run_abaqus import *
from values_to_change import *

def objective_function(experimental_data, params):
    A, B, C, m, n = params
    simulated_data = run_abaqus_simulation(A, B, C, m, n)
    error = sum((experimental_data[key] - simulated_data[key]) ** 2 for key in experimental_data)
    return error

def get_initial_parameters(experimental_data, pso_data, positions):
    n_particles = pso_data['n_particles']
    velocities = np.random.rand(n_particles, 5) * 10         # Initialize velocities with moderate range
    p_best = positions.copy()                                # Track the best-known position of each particle
    # g_best = positions[np.argmin([objective_function(experimental_data, pos) for pos in positions])] # Find the global best initial position
    g_best = [293.46747126, 11.6871621, -71.50550618, 73.38129193, -105.96674671]
    best_error = objective_function(experimental_data, g_best)     
    return velocities, p_best, g_best, best_error