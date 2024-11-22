# -*- coding: utf-8 -*-
import os
import inspect
import json
import pickle
from odbAccess import openOdb

# Function to load and open the ODB file
def load_odb_file():
    # Determine the main directory
    main_directory = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))))
    # # Define the path to the JSON file with input data
    # data_directory = os.path.join(main_directory, 'data\dataInput.json')
    # with open(data_directory, 'r') as json_file:
    #     data = json.load(json_file)
    #     path_to_odb_files = data['paths']['path_to_odb_file']
    path_to_odb_files = (os.path.dirname(inspect.getfile(inspect.currentframe())))
    return path_to_odb_files


# Function to access the node set and extract temperature data
def extract_temperature_data(odb):
    node_set_name = 'TOOLTEMPERATUREOUTPUTSET'
    step = odb.steps['CuttingStep']  # Adjust as needed
    # Initialize lists to store times and temperatures
    times, temperatures = [], []
    # Iterate over frames to extract temperatures
    for frame in step.frames:
        time = frame.frameValue
        temperature = frame.fieldOutputs['NT11'].getSubset(region=odb.rootAssembly.instances['TOOL-1'].nodeSets[node_set_name])
        # Extract temperature values
        temp = [values.data for values in temperature.values][0]
        # Store the time and temperature
        times.append(time)
        temperatures.append(temp)
    return times, temperatures

# Function to save data to a pickle file
def save_data(file_name, times, temperatures):
    # Get the current directory of the script
    data_directory = os.path.join('data') 
    # Save the data to a pickle file
    data = [times, temperatures]
    with open(r'{}\datasNT11{}.pkl'.format(data_directory, file_name), 'wb') as f:
        pickle.dump(data, f)


# Main function to coordinate the loading, processing, and saving of data
def main():
    # Load the directory containing ODB files from the JSON file
    path_to_odb_files = load_odb_file()
    print(path_to_odb_files)
    # Loop through each file in the directory to process ODB files
    for file_name in os.listdir(path_to_odb_files):
        if file_name.endswith('.odb'):  
            odb_path = str(os.path.join(path_to_odb_files, file_name))  
            print(odb_path)
            odb = openOdb(odb_path)
            if odb is None:
                raise ValueError("Failed to open the ODB file.") 
        try:
            times, temperatures = extract_temperature_data(odb)
            save_data(file_name[:-4], times, temperatures)  
            odb.close()
        except:
            pass         


# Entry point to start the program
if __name__ == "__main__":
    main()


  # # Listar todos os conjuntos de nós disponíveis nas partes e instâncias
# print("Conjuntos de Nós Disponíveis em Partes e Instâncias:")
# for instance in odb.rootAssembly.instances.values():
#     print("Instância: " + instance.name)
#     for node_set_name in instance.nodeSets.keys():
#         print("  " + node_set_name)
