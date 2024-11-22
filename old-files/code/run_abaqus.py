call_count = 0
# Simulated Abaqus function for example purposes
def run_abaqus_simulation(A, B, C, m, n):
    global call_count
    call_count += 1  # Increment the counter on each call
    print(f"Simulation #{call_count}")

    """This function represents the model to be optimized. It takes five parameters (A, B, C, m, and n) and returns simulated values 
    for the same output variables present in the experimental data. In the code, this function was simplified, but in practice, 
    it would perform a simulation using Abaqus software and return the results."""

    simulated_data = {
        'cutting_force': (2*A) - 1,
        'normal_cutting_force': (B * 50) / 50,
        'surface_temperature': (C * 0.5)
    }
    return simulated_data