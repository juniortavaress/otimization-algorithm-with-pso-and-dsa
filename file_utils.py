# -*- coding: utf-8 -*-
import os 
import json
import shutil
import inspect 
import easygui

class FileUtils():  
    def set_text(self, message):
        if message == "message-1.0":
            messages = ["<br><br>", "==========================================", "<br><br>", "<b>CREATING GEOMETRY...</b>"]
        elif message == "message-1.1":
            messages = ["<br>", "-> Geometry saved.", "<br><br>", "=========================================="]
        elif message == "message-1.1-2":
            messages = ["<br>", "-> There was a problem creating the geometry.", "<br><br>", "=========================================="]
        elif message == "message-1.0.2":
            messages = ["<br><br>", "==========================================", "<br><br>", "<b>WAITING FOR THE INP FILES...</b>"]
        elif message == "message-1.1.2":
            messages = ["<br>", "-> PATH:", "{0}".format(self.inp_dir), "<br><br>", "=========================================="]
        elif message == "message-2.1":
            messages = ["<br><br>", "<b>STARTING OPTIMIZATION</b>"]
        elif message == "message-2.2":
            messages = ["<br>", "Calling PSO manager..."]
        elif message == "message-2.3":
            messages = ["<br>Starting PSO optimization with pyswarm...<br>"]
        elif message == "message-3.1":
            messages = ["<br>---"]
            messages.extend(["<br><b>ITERATION {0}</b>".format(self.call_count)])
            messages.extend(["<br>Editing .inp file"])
        elif message == "message-3.2":
            messages = ["<br>Running simulation"]
        elif message == "message-3.3":
            messages = ["<br>Transferring .odb files"]
        elif message == "message-3.4":
            messages = ["<br>Collecting results from .odb file<br>"]
        elif message == "message-3.5":
            messages = ["<br><b> Current iteration result </b><br>"]
            messages.extend(["Cutting Force from Simulation: {0}<br>".format(self.simulated_forces[1])])
            messages.extend(["Cutting Force from Experiment: {0}<br>".format(self.target_forces[0])])
            error = (self.target_forces[0] - self.simulated_forces[1]) / self.target_forces[0]
            messages.extend(["Error: {0:.1f}%<br><br>".format(error * 100)])
            messages.extend(["Normal Force from Simulation: {0}<br>".format(self.simulated_forces[0])])
            messages.extend(["Normal Force from Experiment: {0}<br>".format(self.target_forces[1])])
            error = (self.target_forces[1] - self.simulated_forces[0]) / self.target_forces[1]
            messages.extend(["Error: {0:.1f}%<br><br>".format(error * 100)])
            messages.extend(["Temperature from Simulation: {0}<br>".format(self.simulated_temperature)])
            messages.extend(["Temperature from Experiment: {0}<br>".format(self.target_temperature)])
            error = (self.target_temperature - self.simulated_temperature) / self.target_temperature
            messages.extend(["Error: {0:.1f}%<br>".format(error * 100)])
            messages.extend(["---<br>"])
        elif message == "message-3.6":
            messages = ["<br>==========================================<br><br>"]
            messages.extend(["<b>AN ERROR INTERRYPTED THE EXECUTION OF THE PROGRAM</b><br>"])
            messages.extend([self.e])
        elif message == "message-2.4":
            messages = ["<br>==========================================<br><br>"]
            messages.extend(["<b>PSO RESULTS</b>"])
            messages.extend(["<br>Number of Simulations: {0}".format(self.call_count)])
            messages.extend("<br>Optimized Error: {0}".format(self.best_score))
            messages.extend(["<br>Optimized Parameters: "])
            messages.extend(["("])
            messages.extend(", ".join(["{0}: {1:.3f}".format(param, value) for param, value in zip(['D1', 'D2', 'D3'], self.best_position)]))
            messages.extend([")"])
            messages.extend("<br><br>Cutting Force from Simulation: {0}".format(self.filtered_rows['Simulation Cutting Force'].round(2).values[0]))
            messages.extend("<br>Normal Force from Simulation: {0}".format(self.filtered_rows['Simulation Normal Force'].round(2).values[0]))
            messages.extend("<br>Temperature from Simulation: {0}".format(self.filtered_rows['Simulation Temperature'].round(2).values[0]))
        elif message == "message-2.5":
            messages = ["<br><br>==========================================<br><br>"]
            messages.extend(["Time running: {0}".format(self.formatted_duration)])
        elif message == "message-4.1":
            messages = ["<br>", "-> Results Saved.", "<br><br>", "=========================================="]
        elif message == "message-4.1-2":
            messages = ["<br>", "-> There was a problem to get the results.", "<br><br>", "=========================================="]
        else:
            messages = None

        if messages:
            [self.label.setText(self.label.text() + str(message)) for message in messages]

    def create_folders(self, mainclass, call=None):
        """
        Creates necessary folders for storing JSON, Excel, and ODB converted files.
        """
        mainclass.current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        mainclass.geometry_dir = os.path.join(mainclass.current_dir, "geometry")
        mainclass.geometry_datas_dir = os.path.join(mainclass.geometry_dir, "data")
        mainclass.results_dir = os.path.join(mainclass.current_dir, "results")
        mainclass.json_dir = os.path.join(mainclass.results_dir, "json_files")
        mainclass.excel_dir = os.path.join(mainclass.results_dir, "excel_files")
        mainclass.info_dir = os.path.join(mainclass.results_dir, "info_dir")
        mainclass.inp_and_simulation_dir = os.path.join(mainclass.results_dir, "inp-and-simulation")
        mainclass.dafaut_datas_dir = os.path.join(mainclass.results_dir, "defaut")
        mainclass.inp_dir = os.path.join(mainclass.inp_and_simulation_dir, "defaut\INPFiles")
        mainclass.cae_dir = os.path.join(mainclass.inp_and_simulation_dir, "defaut\CAE")
        mainclass.odb_processed_dir = os.path.join(mainclass.results_dir, 'odb-file-processed')
        mainclass.odb_dir = os.path.join(mainclass.results_dir, "odb-files")

        # if call == "temp-force":
        #     with open(os.path.join(mainclass.info_dir, "info.json"), "r") as file:
        #         data = json.load(file)
        #     mainclass.odb_dir = os.path.join(mainclass.current_dir, str(data["path_to_odb"]))
        
        if call == "main":
            print('s5d5d5sd45')
            if os.path.exists(mainclass.results_dir):
                shutil.rmtree(mainclass.results_dir)

            for folder in [mainclass.json_dir, mainclass.excel_dir, mainclass.info_dir, mainclass.inp_dir, mainclass.cae_dir, mainclass.odb_processed_dir, mainclass.odb_dir]:
                if not os.path.exists(folder):
                    os.makedirs(folder)
            
    @staticmethod
    def save_as_json(data, output_json):
        """Save extracted data to a JSON file."""
        with open(output_json, "w") as file:
            json.dump(data, file, indent=4)
        