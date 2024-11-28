import os 
import inspect 
import subprocess 

def generate_inp_files():
    current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    path_to_manager = os.path.join(current_dir, "simulationManager.py")

    try:
        print("---")
        abaqus_command = rf'C:\SIMULIA\Commands\abq2021.bat cae noGUI={path_to_manager}'
        result = subprocess.run(abaqus_command, shell=True, check=True)
        print("---")
        return current_dir, 'INP files were successful generated'
    except Exception as e:
        return f'Error to generate INP: {str(e)} (managerThread.py)'
    
def clean_directory():
    files_to_delete = ['abaqus.rpy', 'abaqus.rpy.1', 'abaqus.rpy.2', 'abaqus.rpy.3', 'abaqus.rpy.4', 'abaqus.rec', 'abaqus_acis.log']
    try:
        for file in files_to_delete:
            print(file)
            if os.path.exists(file):
                os.remove(file)
    except:
        pass    

def main_to_create_geometry():
    dir, message = generate_inp_files()
    print(message)
    print("Directory:", dir)
    print("\n=====================\n")
    clean_directory