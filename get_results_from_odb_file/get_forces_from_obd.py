# -*- coding: utf-8 -*-
import os
import inspect
import json
from odbAccess import openOdb
import easygui

# Function to extract reaction force data from the history output
def extract_reaction_force_data(odb):
    # Access the step
    step = odb.steps['Cutting Step']
    history_outputs = {}

    # Initialize a list to store history outputs

    sets_and_nodes = odb.steps['Cutting Step'].historyRegions.keys()
    
    # Iterate through the available history regions
    for history_region in step.historyRegions.keys():
        region = step.historyRegions[history_region]

    # Specify the region of interest (e.g., a node or part)
    region_name = sets_and_nodes[-1]
    region = step.historyRegions[region_name]

    # Iterate through the available history outputs in the region
    for output_name in region.historyOutputs.keys():
        data = region.historyOutputs[output_name].data
        # print(output_name)
        history_outputs[output_name] = data
    return history_outputs

         
# Main function
def main():
    # Load the directory containing ODB files from the JSON file
    main_dir = (os.path.dirname(os.path.dirname(inspect.getfile(inspect.currentframe()))))
    result_dir = os.path.join(main_dir, "results-json-excel")
    json_dir = os.path.join(result_dir, "json-files")
    # odb_dir = os.path.join(main_dir, 'simulation-and-datas')

    # odb_dir = easygui.diropenbox(title="Select the folder with the odb files")
    odb_dir = os.path.join(result_dir, "odb-files")

    for file_name in os.listdir(odb_dir):
        if file_name.endswith('.odb'):  
            odb_path = str(os.path.join(odb_dir, file_name))  
            odb = openOdb(odb_path)

        # Cria o diretório de resultados, se necessário
        if not os.path.exists(json_dir):
            os.makedirs(json_dir)

        try:
            # Extract reaction force data
            history_outputs = extract_reaction_force_data(odb)
            odb.close()

            # Save data as JSON
            output_json_path = os.path.join(json_dir, "{}_forces.json".format(file_name[:-4]))
            with open(output_json_path, 'w') as json_file:
                json.dump(history_outputs, json_file, indent=4)

            # print(f"Data successfully saved to {output_json_path}")
        except Exception as e:
            # print(f"Error processing file {file_name}: {e}")
            pass
main()