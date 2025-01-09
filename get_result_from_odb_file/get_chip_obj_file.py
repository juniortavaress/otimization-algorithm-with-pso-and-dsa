import os
from abaqus import *
from abaqusConstants import *
from odbAccess import *
from step import *
import displayGroupOdbToolset as dgo
import sys
import inspect
from odbAccess import openOdb

class GetChipMeasure():
    """
    Class to manage the extraction of chip data from ODB files and generate OBJ files.
    """
    def __init__(self):
        """
        Initialize the GetChipMeasure instance, process ODB files, and extract data.
        """
        # Get and verify result directories.
        sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))))
        from file_utils import FileUtils
        self.file = FileUtils()
        self.file.create_folders(self)
        
        # Process ODB files
        step_name, file_directory, obj_directory = self.get_parameters_and_dir()
        self.process_odb(file_directory, step_name, obj_directory)

        
    def get_parameters_and_dir(self):
        """
        Set up the required directories and step name.

        Returns:
            tuple: Step name, directory for ODB files, and directory for OBJ files.
        """
        step_name = 'Cutting Step'
        # file_directory = self.odb_dir
        file_directory = self.odb_dir
        obj_directory = self.obj_dir
        return step_name, file_directory, obj_directory


    def process_odb(self, file_directory, step_name, obj_directory):
        """
        Process each ODB file to extract chip data and generate OBJ files.

        Args:
            file_directory (str): Path to the directory containing ODB files.
            step_name (str): Name of the step to process.
            obj_directory (str): Path to the directory for saving OBJ files.
        """
        
        odb_files = [f for f in os.listdir(file_directory) if f.endswith('.odb')]

        for odb_file in odb_files:
            odb_file_path = os.path.join(file_directory, odb_file)

            # odb = openOdb(odb_file_path, readOnly=True)
            # step_names = odb.steps.keys()
            # step_name = odb.steps[step_names[-1]]

            # Open ODB
            try:
                view = session.Viewport(name='Viewport: 1', origin=(0.0, 0.0), width=200, height=100)
                view.makeCurrent()
                view.maximize()
                view.setValues(displayedObject=session.openOdb(name=odb_file_path))
            except Exception as e:
                continue

            try:
                # Get the step and the total number of frames
                odb = session.odbs[odb_file_path]
                step = odb.steps[step_name]
                total_frames = len(step.frames)

                # Select the last 5 frames or fewer if total_frames < 5
                frame_indices = range(max(0, total_frames - 5), total_frames)

                for frame_index in frame_indices:
                    # frame = step.frames[frame_index]
                    obj_file_name = os.path.splitext(odb_file)[0] + '_Frame' + str(frame_index) + '.obj'
                    obj_file_path = os.path.join(obj_directory, obj_file_name)

                    # Activate section view
                    view.odbDisplay.setFrame(step=step_name, frame=frame_index)
                    view.odbDisplay.setValues(viewCutNames=('EVF_VOID',), viewCut=ON)
                    print("Section view set for frame {0}.".format(frame_index))

                    # Remove CHIPPLATE-1, TOOL-1 and EULERIAN-1
                    try:
                        leaf_chipplate = dgo.LeafFromPartInstance(partInstanceName=('CHIPPLATE-1',))
                        view.odbDisplay.displayGroup.remove(leaf=leaf_chipplate)

                        leaf_tool = dgo.LeafFromPartInstance(partInstanceName=('TOOL-1',))
                        view.odbDisplay.displayGroup.remove(leaf=leaf_tool)

                        leaf_eulerian = dgo.LeafFromPartInstance(partInstanceName=('EULERIANPART-1', ))
                        view.odbDisplay.displayGroup.remove(leaf=leaf_eulerian)
                    except Exception as e:
                        continue

                    # Add Chip Set, set Front View, and create OBJ
                    try:
                        leaf_chipset = dgo.LeafFromElementSets(elementSets=('EULERIANPART-1.CHIPSET', ))
                        view.odbDisplay.displayGroup.add(leaf=leaf_chipset)
                        view.view.setValues(session.views['Front'])
                        session.writeOBJFile(fileName=obj_file_path, canvasObjects=(view, ))
                    except Exception as e:
                        print("Error creating OBJ file for frame {0}: {1}".format(frame_index, str(e)))

            except Exception as e:
                print("Error processing ODB: {0}".format(str(e)))
            finally:
                session.odbs[odb_file_path].close()


if __name__ == "__main__":
    GetChipMeasure()
    sys.exit()

