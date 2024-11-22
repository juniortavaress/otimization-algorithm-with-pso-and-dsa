import numpy as np
from scipy.optimize import minimize

# Dados experimentais e simulados para várias condições de corte
experimental_data = {
    "cutting_force": np.array([1.8, 2.1, 2.5]),  # Exemplos para três velocidades de corte
    "normal_cutting_force": np.array([1.6, 1.9, 2.2]),
    "chip_thickness": np.array([0.1, 0.15, 0.2]),
    "chip_radius": np.array([0.5, 0.55, 0.6]),
    "chip_temperature": np.array([200, 210, 220]),
    "workpiece_surface_temperature": np.array([180, 185, 190])
}

# Dados simulados iniciais (para serem ajustados pelo processo de otimização)
simulated_data_initial = {
    "cutting_force": np.array([1.7, 2.0, 2.4]),
    "normal_cutting_force": np.array([1.5, 1.8, 2.1]),
    "chip_thickness": np.array([0.09, 0.14, 0.19]),
    "chip_radius": np.array([0.48, 0.53, 0.58]),
    "chip_temperature": np.array([198, 208, 218]),
    "workpiece_surface_temperature": np.array([178, 183, 188])
}

# Função para calcular o erro relativo médio para um conjunto de parâmetros simulados
def calculate_error(params, experimental_data, simulated_data):
    # Atualize os dados simulados com os novos parâmetros ajustados
    # Aqui você pode aplicar os parâmetros ajustáveis, por exemplo, multiplicadores para cada observável
    adjusted_simulated_data = {
        "cutting_force": simulated_data["cutting_force"] * params[0],
        "normal_cutting_force": simulated_data["normal_cutting_force"] * params[1],
        "chip_thickness": simulated_data["chip_thickness"] * params[2],
        "chip_radius": simulated_data["chip_radius"] * params[3],
        "chip_temperature": simulated_data["chip_temperature"] * params[4],
        "workpiece_surface_temperature": simulated_data["workpiece_surface_temperature"] * params[5]
    }
    
    # Calcule o erro relativo médio para cada parâmetro e condição de corte
    total_error = 0
    for key in experimental_data.keys():
        experimental_values = experimental_data[key]
        simulated_values = adjusted_simulated_data[key]
        # Erro absoluto médio relativo
        error = np.mean(np.abs((experimental_values - simulated_values) / experimental_values))
        total_error += error
    
    return total_error

# Inicialização dos parâmetros de ajuste
initial_params = np.ones(len(simulated_data_initial))  # Comece com multiplicadores de 1 para todos os parâmetros

# Otimização usando a função de minimização do SciPy (exemplo com Nelder-Mead, que é similar ao Downhill Simplex)
result = minimize(calculate_error, initial_params, args=(experimental_data, simulated_data_initial), method='Nelder-Mead')

# Parâmetros otimizados
optimized_params = result.x
print("Parâmetros Otimizados:", optimized_params)

# Dados simulados ajustados usando os parâmetros otimizados
adjusted_simulated_data = {
    key: simulated_data_initial[key] * optimized_params[i] 
    for i, key in enumerate(simulated_data_initial.keys())
}

# Exibir o erro final
final_error = calculate_error(optimized_params, experimental_data, simulated_data_initial)
print("Erro Final:", final_error)

# Exibir os dados ajustados para cada condição de corte
print("\nDados Simulados Ajustados para cada Condição de Corte:")
for key, values in adjusted_simulated_data.items():
    print(f"{key}: {values}")
