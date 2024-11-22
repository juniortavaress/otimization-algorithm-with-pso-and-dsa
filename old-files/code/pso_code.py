from values_to_change import *
from run_abaqus import *
from functions import *

def pso_iterations(pso_data, experimental_data, velocities, p_best, g_best, best_error, positions):
    # Cache for evaluated parameters to avoid redundant computations
    evaluation_cache = {}

    # PSO main loop with a stopping condition (error < 1% or at least 10 iterations)
    iteration = 0
    n_particles = pso_data['n_particles']
    min_iterations_pso = pso_data['min_iterations_pso']
    w, c1, c2 = pso_data['w'], pso_data['c1'], pso_data['c2']

    print("PSO - Initial Global Parameters:", g_best)

    def evaluate_position(params):
        """Evaluate error for a set of parameters, using cache to avoid re-evaluation."""
        params_tuple = tuple(params)
        if params_tuple in evaluation_cache:
            return evaluation_cache[params_tuple]
        
        error = objective_function(experimental_data, params)
        evaluation_cache[params_tuple] = error
        return error

    while iteration < min_iterations_pso:
        print(f"\nPSO - Iteration {iteration + 1}, Best Error: {best_error}")
        for j in range(n_particles):
            r1, r2 = np.random.rand(), np.random.rand()
            velocities[j] = (w * velocities[j] + c1 * r1 * (p_best[j] - positions[j]) + c2 * r2 * (g_best - positions[j]))
            positions[j] += velocities[j]
            

            # Evaluate error only if the position could potentially improve p_best or g_best
            current_error = evaluate_position(positions[j])
            if current_error < evaluate_position(p_best[j]):
                p_best[j] = positions[j]
            if current_error < best_error:
                g_best = positions[j]
                best_error = current_error

        iteration += 1  # Increment iteration counter


    print("\nPSO - Global Best Parameters:", g_best)
    print("PSO - Global Best Error:", best_error)

    output = run_abaqus_simulation(g_best[0], g_best[1], g_best[2], g_best[3], g_best[4])
    print("\nbest_error", best_error)
    print(output)

    return g_best