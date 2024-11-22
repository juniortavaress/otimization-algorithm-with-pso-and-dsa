import numpy as np 
call_count = 0

# Função para simular o caso, retornando forças e temperatura com base nos parâmetros
def run_simulation(parameters):
    global call_count
    call_count += 1
    A, B, C, n, m = parameters # 160, 120, 100, 2, 3
    # Simulando forças como uma combinação linear dos parâmetros
    simulated_forces = [
        A * 1.1 + B * 0.8 + C * 0.5 + n * 1.2 + m * 0.9,  # Força em x
        A * 0.9 + B * 1.3 + C * 0.4 + n * 1.0 + m * 1.1,  # Força em y
        A * 1.2 + B * 0.7 + C * 0.6 + n * 0.9 + m * 1.3   # Força em z
    ]
    
    # Simulando temperatura como outra combinação dos parâmetros
    simulated_temperature = A * 2.0 + B * 1.5 + C * 1.8 + n * 1.1 + m * 1.3
    
    return simulated_forces, simulated_temperature, call_count

# Função objetivo que calcula o erro entre os valores simulados e os valores-alvo
def objective_function(parameters, target_forces, target_temperature):
    simulated_forces, simulated_temperature, call_count = run_simulation(parameters)
    error_force = np.sum((np.array(simulated_forces) - np.array(target_forces))**2)
    error_temperature = (simulated_temperature - target_temperature)**2
    return np.sqrt(error_force + error_temperature)
