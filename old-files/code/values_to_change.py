import numpy as np

def initial_config():
    error_threshold = 2  # Desired error limit: 1% (0.01 in fractional terms)
    pso_data = {'min_iterations_pso': 12, # Minimum number of PSO iterations before switching to DSA
                'n_particles': 12,        # Number of particles in the PSO
                'w': 0.5,                 # Inertia coefficient for PSO
                'c1': 1.5,                # Cognitive coefficient (attraction to particle's best-known position)
                'c2': 1.5,                # Social coefficient (attraction to global best position)
                'n_variables': 5}
    return error_threshold, pso_data


def get_experimental_data(): 
    # Experimental data (replace with actual values)
    experimental_data = {
        'cutting_force': 3,
        'normal_cutting_force': 1,
        'surface_temperature': 1.5}
    return experimental_data


def initial_particles_position(pso_data):
    n_particles, n_variables = pso_data['n_particles'], pso_data['n_variables']
    # Definir intervalos para cada variável (A, B, C, m, n)
    lower_bounds = [-5, -1, -2, -2, -0]
    upper_bounds = [5, 3, 2, 2, 5]

    # Inicializar as posições das partículas respeitando os limites individuais
    positions = np.array([
        np.random.uniform(lower_bounds[i], upper_bounds[i], n_particles)
        for i in range(n_variables)
    ]).T


    return positions