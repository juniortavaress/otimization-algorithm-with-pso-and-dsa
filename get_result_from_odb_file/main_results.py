# -*- coding: utf-8 -*-
import os
import json
import easygui
import subprocess
import multiprocessing
from get_result_from_odb_file.convert_json_to_excel import DataConverter

class getResults():
    """
    Class to handle results extraction and conversion processes.
    """
    def manage_abaqus_script(self):
        global error_track
        error_track = False
        """
        Executes Abaqus scripts to extract temperatures and forces from ODB files in parallel.
        """
        dir = os.path.join(self.current_dir, "get_result_from_odb_file")
        abaqus_command_temperatures = rf'C:\SIMULIA\Commands\abq2021.bat python {dir}\get_temps.py'
        abaqus_command_forces = rf'C:\SIMULIA\Commands\abq2021.bat python {dir}\get_forces.py'
        commands = [abaqus_command_forces, abaqus_command_temperatures]
    
        processes = []
        process_names = ["get_temps", "get_forces"]
        for name, command in zip(process_names, commands):
            process_name = f"Process_{name}"
            process = multiprocessing.Process(target=getResults.get_data_from_odb, args=(command, ))
            process.name = process_name
            processes.append(process)
            process.start()

        # Wait for all processes to finish
        for process in processes:
            process.join()

        self.error_track = error_track


    def get_data_from_odb(abaqus_command):
        """
        Executes a command to extract data from an ODB file.
        """
        result = subprocess.run(abaqus_command, shell=True, capture_output=True, check=True, text=True)

        if "Error" in result.stdout or "Error" in result.stderr:
            error_track = True


    def convert_json_to_excel(self):
        """
        Converts the generated JSON files into Excel format using the conversion script.
        """
        # input("coloca os json da temp ai")
        DataConverter.main_json_to_excel(self)



