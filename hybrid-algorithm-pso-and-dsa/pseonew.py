import random as rd
import numpy as np
import matplotlib.pyplot as plt

# Configurações globais
rd.seed(12)
W = 0.5
c1 = 0.8
c2 = 0.9
n_iterations = 200
n_particles = 30
target = [537.26, 442.31, 72.39]  # Alvo para força de corte, força normal e temperatura
target_error = 1e-3

# Classe Particle
class Particle():
    def __init__(self):
        x = (-1) ** bool(rd.getrandbits(1)) * rd.random() * 1000
        y = (-1) ** bool(rd.getrandbits(1)) * rd.random() * 1000
        z = (-1) ** bool(rd.getrandbits(1)) * rd.random() * 1000  # Nova dimensão para temperatura
        self.position = np.array([x, y, z])  # Posição agora é 3D
        self.pBest_position = self.position
        self.pBest_value = float('inf')
        self.velocity = np.array([0, 0, 0])  # Velocidade agora é 3D

    def update(self):
        self.position = self.position + self.velocity


# Classe Space
class Space():
    def __init__(self, target, target_error, n_particles):
        self.target = np.array(target)  # Alvo é um vetor [Força_corte, Força_normal, Temperatura]
        self.target_error = target_error
        self.n_particles = n_particles
        self.particles = []
        self.gBest_value = float('inf')
        self.gBest_position = np.array([rd.random() * 50, rd.random() * 50, rd.random() * 50])  # Adaptação para 3D
            
    def fitness(self, particle):
        x = particle.position[0]
        y = particle.position[1]
        z = particle.position[2]
        
        # Simula valores para as três métricas
        f_cut = x**2 + 1  # Exemplo: força de corte
        f_norm = y**2 + 2  # Exemplo: força normal
        temp = z**2 + 3  # Exemplo: temperatura

        # Vetor de valores simulados
        simulated = np.array([f_cut, f_norm, temp])

        # Distância euclidiana entre valores simulados e alvo
        error = np.linalg.norm(simulated - self.target)
        return error
    
    def set_pBest(self):
        for particle in self.particles:
            fitness_candidate = self.fitness(particle)
            if particle.pBest_value > fitness_candidate:
                particle.pBest_value = fitness_candidate
                particle.pBest_position = particle.position
                
    def set_gBest(self):
        for particle in self.particles:
            best_fitness_candidate = self.fitness(particle)
            if self.gBest_value > best_fitness_candidate:
                self.gBest_value = best_fitness_candidate
                self.gBest_position = particle.position
                
    def update_particles(self):
        for particle in self.particles:
            global W
            inertial = W * particle.velocity
            self_confidence = c1 * rd.random() * (particle.pBest_position - particle.position)
            swarm_confidence = c2 * rd.random() * (self.gBest_position - particle.position)
            new_velocity = inertial + self_confidence + swarm_confidence
            particle.velocity = new_velocity
            particle.update()
            
    def show_particles(self, iteration):        
        print(f"Iteration {iteration}: BestPosition = {self.gBest_position}, BestValue = {self.gBest_value}")
        # Visualização em 2D (projeção do espaço 3D)
        for particle in self.particles:
            f_cut = particle.position[0]**2 + 1  # Exemplo: força de corte
            f_norm = particle.position[1]**2 + 2  # Exemplo: força normal
            # temp = z**2 + 3  # Exemplo: temperatura
            plt.plot(f_cut, f_norm, 'ro')  # x-y
            
        # plt.plot(self.gBest_position[0], self.gBest_position[1], 'bo')  # Melhor posição
        target = [100, 200, 300]
        plt.plot(target[0], target[1], 'gx', label="Target") 
        # plt.title(f"Iteration {iteration}")
        # plt.xlabel("X (Força de Corte)")
        # plt.ylabel("Y (Força Normal)")
        # plt.show()

# Inicialização
search_space = Space(target, target_error, n_particles)
particle_vector = [Particle() for _ in range(search_space.n_particles)]
search_space.particles = particle_vector

# Ciclo do PSO
iteration = 0
while iteration < n_iterations:
    # Atualiza os melhores locais
    search_space.set_pBest()
    search_space.set_gBest()

    # Visualização
    search_space.show_particles(iteration)
    
    # Condição de parada
    if search_space.gBest_value <= search_space.target_error:
        break

    search_space.update_particles()
    iteration += 1

# Resultado final
print("The best solution is: ", search_space.gBest_position, " in ", iteration, " iterations")