import numpy as np
import matplotlib.pyplot as plt
from functions import *

# Valores-alvo que desejamos encontrar (target)
target_forces = [1010.0, 1160.0, 1010.0]  # Valores de força nas direções x, y, z
target_temperature = 1855.0  # Temperatura alvo
parameter_bounds = [(300, 700), (350, 750), (0.005, 0.150), (0.1, 0.9), (0.1, 85)]

# Parâmetros PSO
num_particles = 5
num_dimensions = 5  # Parâmetros: A, B, C, n, m
num_iterations = 100
w = 0.5
c1 = 1.5
c2 = 1.5
tolerance = 5.0  # Tolerância para o critério de parada em porcentagem

# Inicialização das partículas
positions = np.random.uniform(low=[b[0] for b in parameter_bounds], high=[b[1] for b in parameter_bounds], size=(num_particles, num_dimensions))
velocities = np.random.uniform(low=-1, high=1, size=(num_particles, num_dimensions))
personal_best_positions = np.copy(positions)
personal_best_scores = np.array([objective_function(p, target_forces, target_temperature) for p in positions])
global_best_position = personal_best_positions[np.argmin(personal_best_scores)]
global_best_score = min(personal_best_scores)

global_best_scores_history = [global_best_score]

# Histórico dos erros
force_errors_list = []
temperature_error_list = []

# Otimização PSO
for iteration in range(num_iterations):
    for i in range(num_particles):
        r1, r2 = np.random.rand(), np.random.rand()
        velocities[i] = (w * velocities[i] +
                         c1 * r1 * (personal_best_positions[i] - positions[i]) +
                         c2 * r2 * (global_best_position - positions[i]))
        
        # Atualizar posição e garantir que esteja dentro dos limites
        positions[i] += velocities[i]
        positions[i] = np.clip(positions[i], [b[0] for b in parameter_bounds], [b[1] for b in parameter_bounds])

        # Avalie a função objetivo
        score = objective_function(positions[i], target_forces, target_temperature)
        
        # Atualize o melhor pessoal e global
        if score < personal_best_scores[i]:
            personal_best_scores[i] = score
            personal_best_positions[i] = positions[i]

        if score < global_best_score:
            global_best_score = score
            global_best_position = positions[i]
    
    global_best_scores_history.append(global_best_score)
    
    # Calcula os erros percentuais atuais com os melhores parâmetros
    best_forces, best_temperature, call_count = run_simulation(global_best_position)
    force_errors = [(abs(target - best) / target) * 100 for target, best in zip(target_forces, best_forces)]
    temperature_error = abs(target_temperature - best_temperature) / target_temperature * 100

    force_errors_list.append(force_errors)
    temperature_error_list.append(temperature_error)

    # Verifica se todos os erros estão abaixo da tolerância
    if all(error < tolerance for error in force_errors) and temperature_error < tolerance:
        print(f"\nCriterio de parada alcançado na iteração {iteration+1}")
        break

print("\nMelhor posição (parâmetros):", global_best_position)
print("Erro mínimo obtido:", global_best_score)
print("Forças calculadas com os melhores parâmetros:", best_forces)
print("Temperatura calculada com os melhores parâmetros:", best_temperature)
print("Erros percentuais finais nas forças (x, y, z):", force_errors)
print("Erro percentual final na temperatura:", temperature_error)
print('Número de simulações:', call_count)

# Convertendo listas de erros para formato numpy para plotagem mais fácil
force_errors_array = np.array(force_errors_list)
temperature_errors_array = np.array(temperature_error_list)

# Gráfico da evolução dos erros de cada força
plt.figure(figsize=(12, 8))

plt.plot(force_errors_array[:, 0], label="Erro Força em x (%)", marker='o', linestyle='-')
plt.plot(force_errors_array[:, 1], label="Erro Força em y (%)", marker='o', linestyle='-')
plt.plot(force_errors_array[:, 2], label="Erro Força em z (%)", marker='o', linestyle='-')
plt.plot(temperature_errors_array, label="Erro Temperatura (%)", marker='o', linestyle='-')

plt.xlabel("Iteração")
plt.ylabel("Erro Percentual (%)")
plt.title("Evolução dos Erros Percentuais para Forças e Temperatura no PSO")
plt.legend()
plt.grid(True)
plt.show()
