import os 
import subprocess 

def generate_inp_files():
    try:
        abaqus_command = rf'C:\SIMULIA\Commands\abq2021.bat cae noGUI=codes-to-create-geometry\simulationManager.py'
        result = subprocess.run(abaqus_command, shell=True, check=True)
        return 'INP files were successful generated (managerThread.py)'
    except Exception as e:
        return f'Error to generate INP: {str(e)} (managerThread.py)'
    
generate_inp_files()


files_to_delete = ['abaqus.rpy', 'abaqus.rpy.1', 'abaqus.rpy.2', 'abaqus.rpy.3', 'abaqus.rpy.4', 'abaqus.rec', 'abaqus_acis.log']
try:
    for file in files_to_delete:
        print(file)
        if os.path.exists(file):
            os.remove(file)
except:
    pass    