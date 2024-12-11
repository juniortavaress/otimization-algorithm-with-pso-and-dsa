# -*- coding: utf-8 -*-
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


class ChipPlateModel():
    def __init__(self, data):
        # Create the chip plate model 
        # if not data:
        #     with open(r"S:\Junior\abaqus-with-python\otimization-scripts\separeted-scripts\generate_cae\geometry\data\defautdatas.json", "r") as file:
        #         data = json.load(file)

        self.dataInput(data)
        self.createPart()
        self.createSetsandSections()
        self.createMesh()

    def dataInput(self, data):
        # Calling Model
        self.ModelName = str(data['generalInformation']['modelName'])
        self.m = mdb.models[self.ModelName]

        # Defining Variables
        self.ElementType = "C3D8R"
        self.ElementLibrary = "EXPLICIT"
        self.ReferenceSetName = "PlateRP"
        self.DomainSetName = "PlateDomain"
        self.SectionName = "ChipPlateSection"

        self.Width = data['chipPlateData']['createPartInformation']['Width']
        self.Height = data['chipPlateData']['createPartInformation']['Height']
        self.PartName = str(data['chipPlateData']['createPartInformation']['Name'])
        self.Trickness = data['chipPlateData']['createPartInformation']['Trickness']
        self.Material = str(data['chipPlateData']['createPartInformation']['Material'])
        self.GlobalSize = data['chipPlateData']['createMeshInformation']['globalSize']
        self.MinSizeFactor = data['chipPlateData']['createMeshInformation']['minSizeFactor']       
        self.DeviationFactor = data['chipPlateData']['createMeshInformation']['deviationFactor']
        
    def createPart(self):
        # Creating the Chip Plate
        self.s = self.m.ConstrainedSketch(name='sketchChipPlate', sheetSize=200.0)
        self.s.rectangle(point1=(0.0, 0.0), point2=(self.Width, self.Height))
        self.p = self.m.Part(dimensionality=THREE_D, name=self.PartName, type=DEFORMABLE_BODY)
        self.p.BaseSolidExtrude(depth=self.Trickness, sketch=self.s)   

    def createSetsandSections(self):
        # Defining the Reference Point
        ref_point_coords = (0.0, self.Height, self.Trickness / 2.0)
        ref_point_id = self.p.ReferencePoint(point=ref_point_coords).id
        
        # Creating RP Set
        self.p.Set(name=self.ReferenceSetName, referencePoints=(self.p.referencePoints[ref_point_id], ))

        # Creating RP Set
        self.p.Set(name=self.ReferenceSetName, referencePoints=(self.p.referencePoints[2], ))
        # Creating Domain Set - Without RF
        self.p.Set(cells=self.p.cells.getSequenceFromMask(('[#1 ]', ), ), name=self.DomainSetName)
        # Creating Sections
        self.m.HomogeneousSolidSection(material=self.Material, name=self.SectionName, thickness=None)
        self.p.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE, region=self.p.sets[self.DomainSetName], sectionName=self.SectionName, thicknessAssignment=FROM_SECTION)
        # Creating Surfaces
        self.p.Surface(name='ChipPlateSurface', side1Faces=self.p.faces.getSequenceFromMask(('[#3f ]', ), ))

    def createMesh(self):
        # Creating Mesh
        self.p.setElementType(elemTypes=(ElemType(
            elemCode=self.ElementType, elemLibrary=self.ElementLibrary, secondOrderAccuracy=OFF, kinematicSplit=AVERAGE_STRAIN, hourglassControl=DEFAULT, 
            distortionControl=DEFAULT), ElemType(elemCode=C3D6, elemLibrary=EXPLICIT), 
            ElemType(elemCode=C3D4, elemLibrary=EXPLICIT)), regions=(self.p.cells.getSequenceFromMask(('[#1 ]', ), ), ))
        self.p.seedPart(deviationFactor=self.DeviationFactor, minSizeFactor=self.MinSizeFactor, size=self.GlobalSize)   # size is the same then global size
        self.p.generateMesh()

# Instantiate the class
# if __name__ == "__main__":
#     ChipPlateModel()

