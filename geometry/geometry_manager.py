# -*- coding: utf-8 -*-
import os
import sys
import json
from abaqus import *
from abaqusConstants import *
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
        """
        Initializes the class and runs the main processes: creating folders, simulation conditions,
        model setup, and geometry and assembly creation.
        If an error occurs, it is captured and logged to a file.
        """
        self.error_track = False
        try:
            sys.dont_write_bytecode = True
            self.create_setup_and_folders()
            self.createConditions()
            self.setupModel()
            self.createGeometryAndAssembly()

        except Exception as e:
            error_data = {  "id": "__init__",
                            "error": str(e),  
                            "error_type": str(type(e)),  
                            "traceback": traceback.format_exc()}

            json_file = os.path.join(self.error_dir, "error_log_geometry_manager_id01.json")
            with open(json_file, "w") as file:
                json.dump(error_data, file, indent=4)
            sys.exit(1)


    def create_setup_and_folders(self):
        """
        Creates the folders and sets up the environment for the model simulation.
        """
        from file_utils import FileUtils
        file = FileUtils() 
        file.create_folders(self)
    

    def createConditions(self):
        """
        Creates the simulation conditions by setting parameters like velocity,
        cutting depth, and simulation time.
        """
        defaut_data = os.path.join(self.geometry_datas_dir, "defaut\defautdatas.json")
        otimization_cond = os.path.join(self.geometry_datas_dir, "defaut\otimizationdatas.json")

        with open(defaut_data, "r") as info:
            defaut_datas = json.load(info)

        with open(otimization_cond, "r") as info:
            otimization_datas = json.load(info)

        conditions = otimization_datas.get("conditions", {})
        for key, _ in conditions.items():
            if key[0:4] == "cond":
                velocity = conditions[key]["velocity"]
                depth_of_cut = conditions[key]["depth_of_cut"]
                time_period = conditions[key]["timePeriod"]
                
                filename = "sim_v{}_h{}.json".format(velocity, int(depth_of_cut*1000))
                json_file = os.path.join(self.geometry_datas_dir, filename)

                defaut_datas["generalInformation"]["modelName"] = filename[:-5]
                defaut_datas["assemblyAndSimulationData"]["toolPosition"]["cuttingDepth"] = depth_of_cut
                defaut_datas["assemblyAndSimulationData"]["stepsAndHistoryInformation"]["timePeriod"] = time_period
                defaut_datas["assemblyAndSimulationData"]["stepsAndHistoryInformation"]["cuttingVelocity"] = velocity

                with open(json_file, "w") as file:
                    json.dump(defaut_datas, file, indent=4)
  

    def setupModel(self):
        """
        Sets up the model in Abaqus by creating a new model and removing old models.
        """
        mdb.Model(modelType=STANDARD_EXPLICIT, name='restartMode')
        for model_name in list(mdb.models.keys()):
            if model_name != 'restartMode':
                del mdb.models[model_name]

        for job_name in list(mdb.jobs.keys()):
            del mdb.jobs[job_name]

        
    def createGeometryAndAssembly(self):
        """
        Creates the geometry and assembly for the simulation from the JSON files.
        It's generated one .inp for each condition of velocity and cutting depth.
        """
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

                    file_base_name = os.path.splitext(files)[0]
                    ModelName = str(data['generalInformation']['modelName'])
                    mdb.Model(modelType=STANDARD_EXPLICIT, name=ModelName)
                    
                    Materials(data) 
                    ChipPlateModel(data)
                    EulerianModel(data)
                    ToolModel(data)
                    AssemblyModel(data, self.inp_dir, self.cae_dir, file_base_name)

            del mdb.models['restartMode']
            os.chdir(self.cae_dir)
            mdb.saveAs(pathName='simulation_cae')

        except Exception as e:  
            self.error_track = True
            error_data = {  "id": "createGeometryAndAssembly",
                            "error": str(e),  
                            "error_type": str(type(e)),  
                            "traceback": traceback.format_exc()}

            json_file = os.path.join(self.error_dir, "error_log_geometry_manager_id02.json")
            with open(json_file, "w") as file:
                json.dump(error_data, file, indent=4)
            sys.exit(1)


# Call the class
if __name__ == "__main__":
    try:
        model = Main()
    except SystemExit as e:
        sys.exit(e.code)






