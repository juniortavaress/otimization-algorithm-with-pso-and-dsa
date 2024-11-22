# -*- coding: utf-8 -*-
# """ Define o terminal cd C:\ temp e usa o comando abaqus cae noGUI=S:/Junior/Abaqus+Python/PythonScriptforAbaqus/backend/main.py """
import os
import json
import inspect
from abaqus import *
from abaqusConstants import *
import numpy as np
from part import *
from step import *
from material import *
from section import *
from assembly import *
from interaction import *
from mesh import *
from visualization import *
from connectorBehavior import *

class Main():
    def __init__(self):
        Main.changeDirectory(self)
        Main.setupModel(self)
        Main.createGeometryAndAssembly(self)
    
    def changeDirectory(self):
        self.current_directory = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) # Path to the folder geometryAndAssembly
        self.main_directory = os.path.dirname(os.path.dirname(self.current_directory)) # Path to the folder backend
        work_directory = os.chdir(self.current_directory) # Define the main directory as geometryAndAssembly

    def setupModel(self):
        mdb.Model(modelType=STANDARD_EXPLICIT, name='restartMode')
        for model_name in list(mdb.models.keys()):
            if model_name != 'restartMode':
                del mdb.models[model_name]

        for job_name in list(mdb.jobs.keys()):
            del mdb.jobs[job_name]
        

        self.path_simulation_datas = os.path.join(os.path.dirname(self.current_directory), 'data/simulationDatas')
        for files in os.listdir(self.path_simulation_datas):
            with open(os.path.join(self.path_simulation_datas, files), 'r') as file:
                data = json.load(file)
            
        pathOutputFiles = data['paths']['pathOutputFiles']
        self.path_INP = os.path.join(pathOutputFiles, 'INPFiles')
        self.path_CAE = os.path.join(pathOutputFiles, 'CAEFiless')
        folders = [self.path_INP, self.path_CAE]

        for folder in folders:
            try:   
                for file in os.listdir(folder):
                    pathFile = os.path.join(self.path_INP, file)
                    os.remove(pathFile)
            except:
                if not os.path.exists(folder):
                    os.makedirs(folder)

    def createGeometryAndAssembly(self):
        import imports 
        from materials import Materials
        from createChipPlate import ChipPlateModel
        from createEulerian import EulerianModel
        from createTool import ToolModel
        from assemblyAndSimulation import AssemblyModel

        for files in os.listdir(self.path_simulation_datas):
            with open(os.path.join(self.path_simulation_datas, files), 'r') as file:
                data = json.load(file)

            ModelName = str(data['generalInformation']['modelName'])
            mdb.Model(modelType=STANDARD_EXPLICIT, name=ModelName)

            for model_name in mdb.models.keys():
                print(model_name, '\n')    
            Materials(data) 
            ChipPlateModel(data)
            EulerianModel(data)
            ToolModel(data)
            fileName = files[10: -5] if files != 'SingleSimulation.json' else files[:-5]
            AssemblyModel(data, self.path_INP, self.path_CAE, fileName)

            print(fileName)
        del mdb.models['restartMode']

        os.chdir(self.path_CAE)
        mdb.saveAs(pathName='simulation_CAE')
    
model = Main()







