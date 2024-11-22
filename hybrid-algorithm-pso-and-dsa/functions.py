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
    ]
    
    # Simulando temperatura como outra combinação dos parâmetros
    simulated_temperature = A * 2.0 + B * 1.5 + C * 1.8 + n * 1.1 + m * 1.3
    
    return simulated_forces, simulated_temperature, call_count


