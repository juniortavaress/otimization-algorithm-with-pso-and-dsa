#file.py
# -*- coding: utf-8 -*-
import os
import easygui
import subprocess
import inspect

class getResults():
    def startResults(self):
        current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        main_dir = os.path.dirname(os.path.dirname(current_dir))
        self.result_dir = os.path.join(main_dir, 'results-json-excel')

        abaqus_command_to_nt11 = rf'C:\SIMULIA\Commands\abq2021.bat python {current_dir}\nt11.py'
        abaqus_command_to_rf = rf'C:\SIMULIA\Commands\abq2021.bat python {current_dir}\get_forces_from_obd.py'

        # commands = [abaqus_command_to_nt11, abaqus_command_to_rf]
        commands = [abaqus_command_to_rf]
        # getResults.cleanDirectory(self)
        [getResults.getDatasfromODB(self, command) for command in commands]
        getResults.convert_json()

    def cleanDirectory(self):
        try:
            for file in os.listdir(self.result_dir):
                pathFile = os.path.join(self.result_dir, file)
                os.remove(pathFile)
        except:
            os.makedirs(self.result_dir)

    def getDatasfromODB(self, abaqus_command):
        result = subprocess.run(abaqus_command, shell=True, check=True)
        print("|-> Comando executado com sucesso!\n") if result.returncode == 0 else print("|-> Ocorreu um erro ao executar o comando.\n")

    def convert_json():
        from get_results_from_odb_file.convert_json_to_excel import main

        # print(sys.path)
        # path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        # print(path)
        main()

if __name__ == "__main__":
    run = getResults()
    run.startResults()

