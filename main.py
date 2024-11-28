import os 
import sys
import inspect
import easygui
import threading
import shutil

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
otimization_algorithm_path = os.path.join(current_dir, "otimization_algorithm")
get_results_from_odb_path = os.path.join(current_dir, "get_results_from_odb_file")
sys.path.append(current_dir)
sys.path.append(otimization_algorithm_path)
sys.path.append(otimization_algorithm_path)
from generate_simulation.codes_to_create_geometry.mainGeometry import main_to_create_geometry
from otimization_algorithm.main_pso import main_pso_manager


class ScriptManager():
    def __init__(self):
        print("\nCLASS SCRIPT MANAGER ACTIVATE")
        self.clean_directory()
        self.inp_file_generator()
        # self.process_inp_file()
        self.inp_folder = r"S:\Junior\abaqus-with-python\otimization-scripts\otimization-algorithm-with-pso-and-dsa\results-json-excel\inp-and-simulation\defaut\INPFiles"
        self.call_pso_script()

    def clean_directory(self):
        results_dir = os.path.join(current_dir, 'results-json-excel')
        if os.path.exists(results_dir):
            shutil.rmtree(results_dir)

    def inp_file_generator(self):
        print("\n=====================\n")
        print("CREATING GEOMETRY:")
        main_to_create_geometry()
        self.inp_folder = os.path.join(current_dir, "auxiliary/INPFiles")

    def process_inp_file(self):
        print("\n=====================\n")
        print("WAITING FOR THE INP FILES...")
        self.inp_folder = easygui.diropenbox(title="Select the folder with the inp file")
        print("PATH:", self.inp_folder)
        print("\n=====================\n")
    
    def call_pso_script(self):
        
        main_pso_manager(self.inp_folder)


ScriptManager()
