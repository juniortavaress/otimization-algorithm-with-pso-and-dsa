# -*- coding: utf-8 -*-
import os 
import json
import shutil
import inspect 
import numpy as np

class FileUtils():  
    def set_text(self, message):
        """
        Responsible for displaying messages in the interface.
        """
        # main.py - message
        if message == "message-id_01":
            messages = ["<br><br>", "==========================================", "<br><br>", "<b>CREATING GEOMETRY...</b>"]
        elif message == "message-id_02":
            messages = ["<br><br>", "==========================================", "<br><br>", "<b>WAITING FOR THE INP FILES...</b>"]
        elif message == "message-id_03":
            messages = ["<br>", "-> Geometry saved.", "<br><br>", "=========================================="]
        elif message == "message-id_04":
            messages = ["<br>", "-> Results Saved.", "<br><br>", "=========================================="]
        # main.py - error
        elif message == "message-ide_01":
            messages = ["<br><br>==========================================<br><br>", "-> There was a problem creating the geometry.", "<br><br>", self.e, "<br><br>", "=========================================="]
        elif message == "message-ide_02":
            messages = ["<br><br>==========================================<br><br>", "-> There was a problem running the PSO.", "<br><br>", self.e, "<br><br>", "=========================================="]
        elif message == "message-ide_03":
            messages = ["<br><br>==========================================<br><br>", "-> There was a problem cleaning the folder.", "<br><br>", self.e, "<br><br>", "=========================================="]
        elif message == "message-ide_04":
            messages = ["<br><br>==========================================<br><br>", "-> There was a problem creating the geometry (sys == 1).", "<br><br>", "=========================================="]

        # otimication_manager.py - message
        elif message == "message-id_05":
            messages = ["<br><br>", "<b>STARTING OPTIMIZATION</b>"]
        elif message == "message-id_06":
            messages = ["<br>Starting PSO optimization with pyswarm...<br>"]
        elif message == "message-id_07":
            messages = ["<br>==========================================<br><br>"]
            messages.extend(["<b>PSO RESULTS</b>"])
            messages.extend(["<br>Number of Simulations: {0}".format(self.call_count)])
            messages.extend("<br>Optimized Error: {0}".format(np.round(self.best_score, 2)))
            messages.extend(["<br>Optimized Parameters: "])
            messages.extend(["("])
            messages.extend(", ".join(["{0}: {1:.3f}".format(param, value) for param, value in zip(['p', 'D2', 'Ts'], self.best_position)]))
            messages.extend([")"])
        elif message == "message-id_08":
            messages = ["<br><br>==========================================<br><br>"]
            messages.extend(["Time running: {0}".format(self.formatted_duration)])
        # otimication_manager.py - error
        elif message == "message-ide_05":
            messages = ["<br><br>==========================================<br><br>", "-> There was a problem related with def start_pso.", "<br><br>", self.e, "<br><br>", "=========================================="]
        elif message == "message-ide_06":
            messages = ["<br><br>==========================================<br><br>", "-> There was a problem finishing the otimization.", "<br><br>", self.e, "<br><br>", "=========================================="]

        # simulation_manager.py - message
        elif message == "message-id_09":
            messages = ["<br>---"]
            messages.extend(["<br><b>ITERATION {0}</b>".format(self.call_count)])
            messages.extend(["<br>Editing .inp file"])
        elif message == "message-id_10":
            messages = ["<br>Running simulation"]
        elif message == "message-id_11":
            messages = ["<br>Transferring .odb files"]
        elif message == "message-id_12":
            messages = ["<br>Collecting results from .odb file<br><br>"]
        elif message == "message-id_13":
            messages = ["Simulation {0} -> Collected<br>".format(self.call_count)]
        # simulation_manager.py - error
        elif message == "message-ide_07":
            messages = ["<br>==========================================<br><br>"]
            messages.extend(["<b>AN ERROR IN THE CLASS SIMULATION MANAGER INTERRUPTED THE EXECUTION OF THE PROGRAM</b><br>"])
            messages.extend([self.e])

        # pso_algorithm.py - message
        elif message == "message-5":
            messages = ["<br><b> BEST RESULT </b><br>"]
            messages.extend(["Cutting Force from Simulation: {0}<br>".format(self.sim_cutting_force)])
            messages.extend(["Cutting Force from Experiment: {0}<br>".format(self.exp_cutting_force)])
            messages.extend(["Error: {0:.1f}%<br><br>".format(self.error_cutting_force * 100)])
            messages.extend(["Normal Force from Simulation: {0}<br>".format(self.sim_normal_force)])
            messages.extend(["Normal Force from Experiment: {0}<br>".format(self.exp_normal_force)])
            messages.extend(["Error: {0:.1f}%<br><br>".format(self.error_normal_force * 100)])
            messages.extend(["Temperature from Simulation: {0}<br>".format(self.sim_temp)])
            messages.extend(["Temperature from Experiment: {0}<br>".format(self.exp_temp)])
            messages.extend(["Error: {0:.1f}%<br>".format(self.error_temp * 100)])
            messages.extend(["---<br>"])

        else:
            print(message)
            print("MENSAGE NOT FINDED")

        if messages:
            [self.label.setText(self.label.text() + str(message)) for message in messages]


    def create_folders(self, mainclass, call=None):
        """
        Creates necessary folders for storing JSON, Excel, and ODB converted files.
        """
        mainclass.current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        mainclass.geometry_dir = os.path.join(mainclass.current_dir, "geometry")
        mainclass.datas_dir = os.path.join(mainclass.current_dir, "dafaut_datas_and_info")
        mainclass.results_dir = os.path.join(mainclass.current_dir, "results")
        mainclass.excel_dir = os.path.join(mainclass.current_dir, "results\excel_files")
        mainclass.inp_and_simulation_dir = os.path.join(mainclass.current_dir, "results\inp-and-simulation")
        mainclass.json_dir = os.path.join(mainclass.current_dir, "results\json_files")
        mainclass.odb_processed_dir = os.path.join(mainclass.current_dir, 'results\odb-file-processed')
        mainclass.odb_dir = os.path.join(mainclass.current_dir, "results\odb-files")
        mainclass.geometry_datas_dir = os.path.join(mainclass.datas_dir, "data")
        mainclass.compiled_files_dir = os.path.join(mainclass.datas_dir, "compiled")
        mainclass.error_dir = os.path.join(mainclass.datas_dir, "error")
        mainclass.inp_dir = os.path.join(mainclass.inp_and_simulation_dir, "defaut\INPFiles")
        mainclass.cae_dir = os.path.join(mainclass.inp_and_simulation_dir, "defaut\CAE")
        mainclass.info = os.path.join(mainclass.inp_and_simulation_dir, "info")

        if call == "main":
            folders = [mainclass.results_dir, mainclass.error_dir]
            for folder in folders:
                if os.path.exists(folder):
                    shutil.rmtree(folder)

            folders_to_create = [mainclass.excel_dir, mainclass.json_dir, mainclass.odb_processed_dir, mainclass.odb_dir, mainclass.inp_dir, mainclass.cae_dir, mainclass.error_dir, mainclass.info]
            for folder in folders_to_create:
                if not os.path.exists(folder):
                    os.makedirs(folder)
            
    @staticmethod
    def save_as_json(data, output_json):
        """Save extracted data to a JSON file."""
        with open(output_json, "w") as file:
            json.dump(data, file, indent=4)
        