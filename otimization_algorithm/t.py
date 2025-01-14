import json

# Carregar o arquivo JSON
file_path = r"S:\Junior\abaqus-with-python\otimization-scripts\otimization-algorithm-with-pso-and-dsa\dafaut_datas_and_info\status\status_file.json"
with open(file_path, "r") as file:
    data = json.load(file)

# Acessar os dados de otimização
optimization_data = data.get("Otimization", {})
iterations = {key: value for key, value in optimization_data.items() if key.startswith("iteration")}
print(len(iterations))
last_iteration_key = max(iterations.keys(), key=lambda k: int(k.split()[-1]))
last_iteration = iterations[last_iteration_key]


# Verificar se há erro na última iteração e extrair valores
if last_iteration.get("error") != "null":
    previous_iteration_key = f"iteration {int(last_iteration_key.split()[-1]) - 1}"

    best_position = iterations[previous_iteration_key].get("best position")
    personal_best_positions = iterations[previous_iteration_key].get("personal_best_positions")
    positions = iterations[previous_iteration_key].get("positions")
    otimized_error = iterations[previous_iteration_key].get("otimized-error")
    velocities = iterations[previous_iteration_key].get("velocities")

    print("Última Iteração com Erro:")
    print(f"Best Position: {best_position}")
    print(f"Personal Best Positions: {personal_best_positions}")
    print(f"Positions: {positions}")
    print(f"otimized-error: {otimized_error}")
    print(f"velocities: {velocities}")
else:
    print("A última iteração não contém erro.")
