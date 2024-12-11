# -*- coding: utf-8 -*-
import os
import json
import easygui
import subprocess
import multiprocessing
from get_result_from_odb_file.convert_json_to_excel import DataConverter
from file_utils import FileUtils

class getResults():
    """
    Class to handle results extraction and conversion processes.
    """
    def __init__(self):
        """
        Initializes the GetResults class, creating necessary folders.
        """
        file = FileUtils() 
        file.create_folders(self, None)


    def get_odb_path(self):
        """
        Prompts the user to select a directory containing ODB files and saves the path to a JSON file.
        """
        self.odb_dir = str(easygui.diropenbox("Select ODB folder"))
        path_to_save_info = os.path.join(self.info_dir, "info.json")
        FileUtils.save_as_json({"path_to_odb": self.odb_dir}, path_to_save_info)


    def send_odb_path(self, odb_path):
        """
        Sets the ODB directory path and saves it to a JSON file.
        """
        self.odb_dir = str(odb_path)
        path_to_save_info = os.path.join(self.info_dir, "info.json")
        FileUtils.save_as_json({"path_to_odb": self.odb_dir}, path_to_save_info)


    def manage_abaqus_script(self):
        """
        Executes Abaqus scripts to extract temperatures and forces from ODB files in parallel.
        """
        dir = os.path.join(self.current_dir, "get_result_from_odb_file")
        abaqus_command_temperatures = rf'C:\SIMULIA\Commands\abq2021.bat python {dir}\get_temps.py'
        abaqus_command_forces = rf'C:\SIMULIA\Commands\abq2021.bat python {dir}\get_forces.py'
        commands = [abaqus_command_forces, abaqus_command_temperatures]
    
        # Create processes to run commands in parallel
        processes = []
        for command in commands:
            process = multiprocessing.Process(target=self.get_data_from_odb, args=(command,))
            processes.append(process)
            process.start()

        # Wait for all processes to finish
        for process in processes:
            process.join()


    def get_data_from_odb(self, abaqus_command):
        print('comando')
        """
        Executes a command to extract data from an ODB file.
        """
        result = subprocess.run(abaqus_command, shell=True, capture_output=True, check=True, text=True)
        print(result)
        print(result.stderr)
        print(result.stdout)
        # if "Error" in result.stdout or "Error" in result.stderr:
        #     FileUtils.set_text(parent, "message-4.1")
        # else:
        #     FileUtils.set_text(parent, "message-4.1-2")


    def convert_json_to_excel(self):
        print('excel')
        """
        Converts the generated JSON files into Excel format using the conversion script.
        """
        DataConverter.main_json_to_excel(self)


if __name__ == "__main__":
    runner = getResults()
    runner.get_odb_path()
    runner.manage_abaqus_script()
    runner.convert_json_to_excel()

