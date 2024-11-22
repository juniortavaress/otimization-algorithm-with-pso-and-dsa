import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Definir valores alvo (target values)
target_force_cut = 50  # Força de corte
target_normal_force = 100  # Força normal
target_temperature = 300  # Temperatura

# Gerar 5 pontos aleatórios (partículas PSO)
np.random.seed(42)  # Para reprodutibilidade
particles = np.array([
    [
        np.random.uniform(40, 60),  # Força de corte
        np.random.uniform(90, 110),  # Força normal
        np.random.uniform(290, 310)  # Temperatura
    ] for _ in range(5)
])

# Simular a segunda iteração com partículas mais próximas ao ponto alvo
particles_second_iteration = np.array([
    (target_force_cut + 3, target_normal_force + 3, target_temperature + -1),
    (target_force_cut + 2, target_normal_force + 2, target_temperature + 2),
    (target_force_cut + 1, target_normal_force + 1, target_temperature + 1),
    (target_force_cut + 2, target_normal_force + -3, target_temperature + 3),
    (target_force_cut + -3, target_normal_force + 2, target_temperature + 2)
])

# Configurar o gráfico 3D para as duas iterações
fig = plt.figure(figsize=(18, 8))

# Gráfico da primeira iteração
ax1 = fig.add_subplot(121, projection='3d')
ax1.scatter(target_force_cut, target_normal_force, target_temperature, color='blue', s=100, label='Target Value (Results from experiment)', marker='x')
ax1.scatter(particles[:, 0], particles[:, 1], particles[:, 2], color='red', s=50, label='PSO Particles (D1, D2...)', marker='o')
# Configurar rótulos e título
ax1.set_xlabel('Cutting Force')
ax1.set_ylabel('Normal Force')
ax1.set_zlabel('Temperature')
ax1.set_title('PSO Behavior - First Iteration')
ax1.set_xlim(40,60)
ax1.set_ylim(90,110)
ax1.set_zlim(290,310)
ax1.legend()

# Gráfico da segunda iteração
ax2 = fig.add_subplot(122, projection='3d')
ax2.scatter(target_force_cut, target_normal_force, target_temperature, color='blue', s=100, label='Target Value (Results from experiment)', marker='x')
ax2.scatter(particles_second_iteration[:, 0], particles_second_iteration[:, 1], particles_second_iteration[:, 2], color='orange', s=50, label='PSO Particles (D1, D2...)', marker='o')
# Configurar rótulos e título
ax2.set_xlabel('Cutting Force')
ax2.set_ylabel('Normal Force')
ax2.set_zlabel('Temperature')
ax2.set_title('PSO Behavior - n Iteration')
ax2.set_xlim(40,60)
ax2.set_ylim(90,110)
ax2.set_zlim(290,310)
ax2.legend()

# Exibir o gráfico
plt.show()
