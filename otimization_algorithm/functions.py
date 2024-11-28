import re
import os
import shutil
import numpy as np 
import pandas as pd
import subprocess

call_count = 0

def edit_inp_file(file_path, new_values):
    # Abrir o arquivo para leitura
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Encontrar e editar os parâmetros D1, D2, D3 na seção *Damage Initiation
    pattern = r"^\*Damage Initiation.*JOHNSON COOK.*"  # Encontra a linha de início da seção *Damage Initiation
    for i, line in enumerate(lines):
        if re.match(pattern, line):
            # A linha seguinte contém os valores de D1, D2, D3
            damage_initiation_values_line = lines[i + 1]
            
            # Dividir os valores da linha e substituí-los
            values = damage_initiation_values_line.split(',')

            # Suponha que os 3 primeiros valores correspondem a D1, D2, D3
            values[0] = f"{new_values[0]:>5}"  # Atualiza o valor de D1
            values[1] = f"{new_values[1]:>7}"   # Atualiza o valor de D2
            values[2] = f"{new_values[2]:>7}"  # Atualiza o valor de D3

            # Recriar a linha com os novos valores
            new_damage_initiation_values_line = ','.join(values)
            lines[i + 1] = new_damage_initiation_values_line  # Substitui a linha original pela nova
            break  # Assumindo que há apenas uma ocorrência de *Damage Initiation

    # Salvar as alterações no arquivo
    main_dir_inp_defaut = os.path.dirname(os.path.dirname(os.path.dirname(file_path)))
    filename = os.path.basename(file_path)[:-4]
    params = f"{filename}_D1_{float(values[0].strip()):.2f}_D2_{float(values[1].strip()):.2f}_D3_{float(values[2].strip()):.2f}.inp"
    dir_inp = os.path.join(main_dir_inp_defaut, params[:-4])
    output_file_path = os.path.join(dir_inp, params)
    os.makedirs(dir_inp)
    
    with open(output_file_path, 'w') as file:
        file.writelines(lines)
    
    return dir_inp

##########################################################
# MOVER ODB DE LUGAR
##########################################################
def copy_odb_file(file_path):
    main_dir_inp_defaut = os.path.dirname(os.path.dirname(os.path.dirname(file_path)))
    main_dir_results = os.path.dirname(main_dir_inp_defaut)
    # print("-", main_dir_results)
    destination_odb_folder = os.path.join(main_dir_results, "odb-files")
    
    if not os.path.exists(destination_odb_folder):
        os.makedirs(destination_odb_folder)

    for folder_name in os.listdir(main_dir_inp_defaut):
        folder_path = os.path.join(main_dir_inp_defaut, folder_name)
        if os.path.isdir(folder_path) and folder_name.lower() != "defaut":
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    if file.endswith(".odb"):  # Verifica se é um arquivo .odb
                        source_path = os.path.join(root, file)  # Caminho completo do arquivo
                        destination_path = os.path.join(destination_odb_folder, file)  # Caminho para o destino

                        shutil.copy2(source_path, destination_path)
                        os.remove(source_path)


def get_results(filename_to_search):
    from get_results_from_odb_file.main_results import getResults
    results = getResults()
    results.startResults()
    file_path = r"S:\Junior\abaqus-with-python\otimization-scripts\otimization-algorithm-with-pso-and-dsa\results-json-excel\excel-file"
    for file in os.listdir(file_path):
        path_df = os.path.join(file_path, file)

    df = pd.read_excel(path_df, header=1)

    # print(filename_to_search)
    # Filtrar o DataFrame com base no Filename
    filtered_row = df[df["Filename"] == filename_to_search]
    simulated_forces = [filtered_row.iloc[0,3], filtered_row.iloc[0,7]]
    simulated_temperature = filtered_row.iloc[0,9]
    
    print("--- Resultado da iteração atual ---")
    print('Cutting Force from Simulation:', simulated_forces[0])
    print('Cutting Normal from Simulation:', simulated_forces[1])
    print('Temperature from Simulation:',  simulated_temperature)
    print("")

    return simulated_forces, simulated_temperature

def run_simulation(path_to_inp_folder):
    number_of_cores = 4
    # for files in os.listdir(path_to_inp_folder):
    #     if files.endswith('.inp'):
    #         path = os.path.join(path_to_inp_folder, files)
    #         command = rf'call C:\SIMULIA\Commands\abq2021.bat job={path} cpus={number_of_cores} interactive'
    # os.chdir(path_to_inp_folder) 
    # result = subprocess.run(command, shell=True, check=True)
    # print("|-> Comando executado com sucesso!\n") if result.returncode == 0 else print("|-> Ocorreu um erro ao executar o comando.\n")
    from otimization_algorithm.pararelSimulation import PararelSimulation
    simulation = PararelSimulation
    simulation.startSimulation(simulation, path_to_inp_folder, number_of_cores)
    print('=========================================\n')

    # A, B, C= parameters # 160, 120, 100, 2, 3
    # # Simulando forças como uma combinação linear dos parâmetros
    # simulated_forces = [
    #     A * 1.1 + B * 0.8 + C * 0.5,  # Força em x
    #     A * 0.9 + B * 1.3 + C * 0.4  # Força em y
    # ]
    
    # # Simulando temperatura como outra combinação dos parâmetros
    # simulated_temperature = A * 2.0 + B * 1.5 + C * 1.8
    
    # source_dir = r"S:\Junior\abaqus-with-python\otimization-scripts\otimization-algorithm-with-pso-and-dsa\inp-and-simulation22\test-scrip-with-python_D1_0.03_D2_0.53_D3_-1.9"
    # destination_dir = output_file_path
    # # print(destination_dir)

    # # Listar arquivos no diretório de origem
    # files = [f for f in os.listdir(source_dir) if os.path.isfile(os.path.join(source_dir, f))]
    
    # if files:
    #     first_file = files[0]  # Primeiro arquivo encontrado
    #     source_path = os.path.join(source_dir, first_file)
    #     destination_path = os.path.join(destination_dir, os.path.basename(output_file_path)+".odb")

    #     # Copiar o arquivo
    #     shutil.copy2(source_path, destination_path)
    #     # print(f"Arquivo '{first_file}' copiado para '{destination_path}'")

    #     # Remover o arquivo da origem
    #     os.remove(source_path)

# Função para simular o caso, retornando forças e temperatura com base nos parâmetros
def simulation_manager(inp_folder, parameters):
    global call_count
    call_count += 1
    
    print(f'ITERAÇÃO {call_count}')
    print(f'Editando arquivo .inp')
    for file in os.listdir(inp_folder):
        file_path = os.path.join(inp_folder, file)
    output_file_path = edit_inp_file(file_path, parameters)

    print(f'Rodando Simulação')
    run_simulation(output_file_path)
    
    print(f'Transferindo arquivos .odb')
    copy_odb_file(file_path)

    print(f'Coletando resultados do arquivo .odb')
    simulated_forces, simulated_temperature = get_results(os.path.basename(output_file_path))

    print('----\n')
    # simulated_forces = [0,1]
    # simulated_temperature = 1
    return simulated_forces, simulated_temperature, call_count






    


if __name__ == "__main__":
    inp_folder = r"S:\Junior\abaqus-with-python\otimization-scripts\otimization-algorithm-with-pso-and-dsa\results-json-excel\inp-and-simulation\defaut\INPFiles"
    for file in os.listdir(inp_folder):
        file_path = os.path.join(inp_folder, file)
    new_values = [0.05, 0.74, -1.45]
    edit_inp_file(file_path, new_values)