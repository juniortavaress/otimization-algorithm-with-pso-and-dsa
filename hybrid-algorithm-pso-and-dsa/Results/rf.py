# -*- coding: utf-8 -*-
import os
import inspect
import json
import pickle
from odbAccess import openOdb
import matplotlib.pyplot as plt

# Function to load and open the ODB file
def load_odb_file():
    # Determine the main directory
    # main_directory = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))))
    # # Define the path to the JSON file with input data
    # data_directory = os.path.join(r'S:\Junior\abaqus-with-python\gui-interface-abaqus-with-python\data\dataInput.json')
    # with open(data_directory, 'r') as json_file:
    #     data = json.load(json_file)
    #     path_to_odb_files = data['paths']['path_to_odb_file']
    
    main_path = (os.path.dirname(inspect.getfile(inspect.currentframe())))
    path_to_odb_files = os.path.join(main_path, 'simulation-and-datas')
    # path_to_odb_files = "S:\Junior\Severin_Datas_Abaqus\Scripts_Orthogonal_cutting"
    return path_to_odb_files

# Function to extract reaction force data from the history output
def extract_reaction_force_data(odb):
    # Access the step
    step = odb.steps['CuttingStep']

    # Initialize a list to store history outputs
    history_outputs = [] 
    sets_and_nodes = odb.steps['CuttingStep'].historyRegions.keys()
    
    # Iterate through the available history regions
    for history_region in step.historyRegions.keys():
        region = step.historyRegions[history_region]

    # Specify the region of interest (e.g., a node or part)
    region_name = sets_and_nodes[-1]
    region = step.historyRegions[region_name]

    # Iterate through the available history outputs in the region
    for output_name in region.historyOutputs.keys():
        data = region.historyOutputs[output_name].data
        history_outputs.append((output_name, data))
    return history_outputs

# Function to process and extract specific reaction force data (RF1, RF2, RF3)
def process_reaction_forces(history_outputs):
    # Dictionaries to store the data for each reaction force
    data_rf1, data_rf2, data_rf3 = None, None, None
    # Extracting specific reaction force data
    for output_name, data in history_outputs:
        times = [point[0] for point in data]
        values = [point[1] for point in data]
        # Assign data based on the output name (RF1, RF2, RF3)
        if output_name == 'RF1':
            data_rf1 = (times, values)
        elif output_name == 'RF2':
            data_rf2 = (times, values)
        elif output_name == 'RF3':
            data_rf3 = (times, values)
    return data_rf1, data_rf2, data_rf3

# Function to save data to a pickle file
def save_data(path_to_odb_files, file_name, data_rf1, data_rf2, data_rf3):
    # Get the current directory of the script
    current_directory = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    main = os.path.dirname(os.path.dirname(current_directory))
    data_directory = os.path.join(current_directory) 
    # Save the reaction force data to a pickle file
    datas = [data_rf1, data_rf2, data_rf3]
    # print(datas)
    with open(r'{}\datasRF{}.pkl'.format(path_to_odb_files, file_name), 'wb') as f:
        pickle.dump(datas, f)

def create_graph_image(data_rf1, data_rf2):
    plt.plot(data_rf1[0], data_rf1[1], '-', label="Target")  
    plt.title("Cutting Force (RF1)")
    plt.xlabel("Time Step")
    plt.ylabel("Force")
    plt.savefig('Results\graph-images\cutting-force', dpi=300, bbox_inches='tight')
    plt.close()

    plt.plot(data_rf2[0], data_rf2[1], 'r-', label="Target")  
    plt.title("Normal Force (RF2)")
    plt.xlabel("Time Step")
    plt.ylabel("Force")
    plt.savefig(r'Results\graph-images\normal-force', dpi=600, bbox_inches='tight')
    plt.close()

# Main function
def main():
    # Load the directory containing ODB files from the JSON file
    path_to_odb_files = load_odb_file()
    # Loop through each file in the directory to process ODB files
    for file_name in os.listdir(path_to_odb_files):
        if file_name.endswith('.odb'):  
            odb_path = str(os.path.join(path_to_odb_files, file_name))  
            odb = openOdb(odb_path)
            if odb is None:
                raise ValueError("Failed to open the ODB file.") 
        
            try:
                history_outputs = extract_reaction_force_data(odb)
                # Process the extracted data
                data_rf1, data_rf2, data_rf3 = process_reaction_forces(history_outputs)
                # Save the reaction force data to a pickle file
                save_data(path_to_odb_files, file_name[:-4], data_rf1, data_rf2, data_rf3)
                create_graph_image(data_rf1, data_rf2)
                odb.close()
            except:
                print('Error to open odb file')

# Execute the script
main()
