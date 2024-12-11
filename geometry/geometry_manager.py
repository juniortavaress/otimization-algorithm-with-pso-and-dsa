# -*- coding: utf-8 -*-
import os
import json
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
import traceback


class Main():
    def __init__(self):
        try:
            sys.dont_write_bytecode = True
            self.create_setup_and_folders()
            self.setupModel()
            self.createGeometryAndAssembly()
        except Exception as e:
            error_data = {
                "id": "__init__",
                "error": str(e),  
                "error_type": str(type(e)),  
                "traceback": traceback.format_exc() 
            }

            json_file = os.path.join(self.current_dir, "error_log.json")
            with open(json_file, "w") as file:
                json.dump(error_data, file, indent=4)


    def create_setup_and_folders(self):
        from file_utils import FileUtils
        file = FileUtils() 
        file.create_folders(self, "main")
    

    def setupModel(self):
        mdb.Model(modelType=STANDARD_EXPLICIT, name='restartMode')
        for model_name in list(mdb.models.keys()):
            if model_name != 'restartMode':
                del mdb.models[model_name]

        for job_name in list(mdb.jobs.keys()):
            del mdb.jobs[job_name]

            
    def createGeometryAndAssembly(self):
        os.chdir(self.geometry_dir)

        from materials import Materials
        from create_chip_plate import ChipPlateModel
        from create_eulerian import EulerianModel
        from create_tool import ToolModel
        from assembly_and_simulation import AssemblyModel

        try: 
            for files in os.listdir(self.geometry_datas_dir):
                if files.endswith(".json"):
                    with open(os.path.join(self.geometry_datas_dir, files), 'r') as file:
                        data = json.load(file)

                ModelName = str(data['generalInformation']['modelName'])
                mdb.Model(modelType=STANDARD_EXPLICIT, name=ModelName)

                Materials(data) 
                ChipPlateModel(data)
                EulerianModel(data)
                ToolModel(data)
                AssemblyModel(data, self.inp_dir, self.cae_dir, "sim")

            del mdb.models['restartMode']
            os.chdir(self.cae_dir)
            mdb.saveAs(pathName='simulation_cae')

        except Exception as e:  
            error_data = {
                "id": "createGeometryAndAssembly",
                "error": str(e),  
                "error_type": str(type(e)),  
                "traceback": traceback.format_exc() 
            }

            json_file = os.path.join(self.current_dir, "error_log.json")
            with open(json_file, "w") as file:
                json.dump(error_data, file, indent=4)



model = Main()







