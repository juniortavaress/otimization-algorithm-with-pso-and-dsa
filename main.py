import os
import sys
import inspect
import subprocess
from PySide6.QtCore import Qt, QThread
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from file_utils import FileUtils
from otimization_algorithm.otimization_manager import OtimizationManager
from ui_form import Ui_Widget

# Get the current directory and set paths for other modules
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
optimization_algorithm_path = os.path.join(current_dir, "otimization_algorithm")
get_results_from_odb_path = os.path.join(current_dir, "get_result_from_odb_file")

# Add paths to the system path
sys.path.append(current_dir)
sys.path.append(optimization_algorithm_path)
sys.path.append(get_results_from_odb_path)


class ScriptManager(QWidget):
    """
    Manages the GUI and the overall script workflow, including geometry generation,
    simulation management, and optimization tasks.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Widget()
        self.ui.setupUi(self)

        self.create_setup_and_folders()
        self.create_message_area()
        self.generate_geometry_from_script()    
        # self.generate_geometry_from_input()  


    def create_setup_and_folders(self):
        """
        Creates required directories for the script's workflow.
        """
        self.error_track = False
        file = FileUtils() 
        file.create_folders(self, "main")


    def create_message_area(self):
        """
        Sets up the message display area with a scrollable QLabel.
        """
        central_widget = QWidget(self)
        self.ui.scrollArea.setWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        self.ui.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.label = QLabel("<b>SCRIPT STARTED</b>", self)
        layout.addWidget(self.label)
        self.label.setAlignment(Qt.AlignTop)


    def generate_geometry_from_input(self):
        """
        Prompts the user to select a directory containing input files
        and starts the geometry generation process.
        """
        try:
            FileUtils.set_text(self, "message-id_02")
            self.thread = QThread()
            self.thread.setObjectName("GeometryGenerationThread")
            self.thread.run = lambda: self.get_path()
            self.thread.finished.connect(lambda: FileUtils.set_text(self, "message-id_03"))
            self.thread.finished.connect(lambda: self.call_pso_script())
            self.thread.start()
        except Exception as e:
            self.e = e
            FileUtils.set_text(self, "message-ide_01")


    def get_path(self):
        """
        Opens a dialog box for the user to select the directory with .inp files.
        """
        # self.inp_dir = easygui.diropenbox(title="Select the folder with the inp file")
        self.inp_dir = r"S:\Junior\abaqus-with-python\otimization-scripts\otimization-algorithm-with-pso-and-dsa"


    def generate_geometry_from_script(self):
        """
        Starts the geometry generation process using an Abaqus script.
        """
        try:
            FileUtils.set_text(self, "message-id_01")
            self.thread = QThread()
            self.thread.setObjectName("GeometryGenerationThread")
            self.thread.run = lambda: ScriptManager.generate_inp_files(self)  
            self.thread.finished.connect(lambda: self.call_pso_script())
            self.thread.start()
        except Exception as e:
            self.e = e
            self.error_track = True
            FileUtils.set_text(self, "message-ide_01")


    def generate_inp_files(self):
        """
        Runs an Abaqus script to generate input files for simulations.
        """
        path_to_manager_geometry = os.path.join(self.geometry_dir, "geometry_manager.py")
        abaqus_command = rf'C:\SIMULIA\Commands\abq2021.bat cae noGUI={path_to_manager_geometry}'
        result = subprocess.run(abaqus_command, shell=True, capture_output=True, check=True, text=True)

        if "Error" in result.stdout or "Error" in result.stderr:
            self.error_track = True
            print(result.stdout)
            print(result.stderr)
            FileUtils.set_text(self, "message-ide_04")
        else:
            FileUtils.set_text(self, "message-id_03")


    def call_pso_script(self):
        """
        Calls the optimization script after geometry generation is complete.
        """
        if not self.error_track:
            try:
                self.thread = QThread()
                self.thread.run = lambda: ScriptManager.thread_to_pso(self)  
                self.thread.finished.connect(lambda: self.clean_folder())
                self.thread.start()
                # self.thread.wait()
            except Exception as e:
                self.e = e
                self.error_track = True
                FileUtils.set_text(self, "message-ide_02")
           

    def thread_to_pso(self):
        """
        Manages the optimization process by calling the main optimization manager.
        """
        OtimizationManager.main_otimization_manager(self)
        FileUtils.set_text(self, "message-id_04")
        

    def clean_folder(self):
        """
        Cleans up temporary Abaqus-related files from the current directory.
        """
        if not self.error_track:
            try:
                for file in os.listdir(self.current_dir):
                    if file.startswith("abaqus"):
                        file_path = os.path.join(self.current_dir, file)
                        if os.path.isfile(file_path):  
                            os.remove(file_path)
            except Exception as e:
                self.e = e
                raise FileUtils.set_text(self, "message-ide_01")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = ScriptManager()
    widget.show()
    sys.exit(app.exec())
