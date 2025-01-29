import sys
import time
import pandas as pd
from otimization_algorithm.pso_algorithm import PsoManager
from otimization_algorithm.simualtion_manager import *
from file_utils import FileUtils
sys.dont_write_bytecode = True

class OtimizationManager():
    def main_otimization_manager(self):
        """
        Main method to manage the optimization process, including
        folder setup, PSO algorithm execution, and finalizing the optimization.
        """
        initial_time = time.time()
        # Create necessary folders for the optimization process
        file = FileUtils() 
        file.create_folders(self)
        # Set messages and start the PSO algorithm
        FileUtils.set_text(self, "message-id_05")
        OtimizationManager.start_pso(self)
        # Finalize the optimization process
        OtimizationManager.finish_otimization(self, initial_time)
        time.sleep(2)


    def start_pso(self):
        """
        Start the Particle Swarm Optimization (PSO) algorithm.
        Updates the optimization manager with the best position and score.
        """
        try:
            FileUtils.set_text(self, "message-id_06")
            self.call_count, self.best_position, self.best_score = PsoManager.run_pso(self)
            FileUtils.set_text(self, "message-id_07")
        except Exception as e:
            self.e = e
            self.error_track = True
            FileUtils.code_status(self, "start_pso")
            FileUtils.set_text(self, "message-ide_05")


    def finish_otimization(self, initial_time):
        """
        Finalizes the optimization process by calculating and formatting the 
        duration of the optimization.
        """
        if not self.error_track:
            try:
                self.duration = (time.time()) - initial_time
                days, hours, minutes, seconds = self.duration // (24 * 3600), (self.duration % (24 * 3600)) // 3600, (self.duration % 3600) // 60, self.duration % 60       
                self.formatted_duration = f"{int(days)} dias, {int(hours)}h, {int(minutes)}m e {int(seconds)}s"
                FileUtils.set_text(self, "message-id_08")
                FileUtils.code_status(self, "otimization-fisished")
            except Exception as e:
                self.e = e
                self.error_track = True
                FileUtils.set_text(self, "message-ide_06")
                
        # else:
        #     FileUtils.code_status(self, "otimization-error")