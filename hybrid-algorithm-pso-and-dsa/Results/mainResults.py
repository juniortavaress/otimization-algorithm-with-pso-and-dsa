#file.py
# -*- coding: utf-8 -*-
import os
import subprocess
import matplotlib.pyplot as plt
import inspect

class getResults():
    def startResults(self):
        current_directory = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        self.main = os.path.dirname(os.path.dirname(current_directory))
        abaqus_command_to_nt11 = rf'abaqus python {current_directory}\nt11.py'
        abaqus_command_to_rf = rf'abaqus python {current_directory}\rf.py'
        # commands = [abaqus_command_to_nt11, abaqus_command_to_rf]
        commands = [abaqus_command_to_rf]
        getResults.cleanDirectory(self)
        [getResults.getDatasfromODB(self, command) for command in commands]

    def cleanDirectory(self):
        data_directory = os.path.join(self.main, 'data/resultsDatas')
        try:
            for file in os.listdir(data_directory):
                pathFile = os.path.join(data_directory, file)
                os.remove(pathFile)
        except:
            os.makedirs(data_directory)

    def getDatasfromODB(self, abaqus_command):
        result = subprocess.run(abaqus_command, shell=True, check=True)
        print("Comando executado com sucesso!") if result.returncode == 0 else print("Ocorreu um erro ao executar o comando.")

if __name__ == "__main__":
    run = getResults()
    run.startResults()

