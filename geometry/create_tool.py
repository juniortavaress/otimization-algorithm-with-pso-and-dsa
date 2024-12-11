# -*- coding: utf-8 -*-
import inspect
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

class ToolModel():
    def __init__(self, data):



        self.dataInput(data)
        self.createPart()
        self.createPartition()
        self.createSetsandSections()
        self.createMesh()


    def dataInput(self, data):
        # Calling Model
        self.ModelName = str(data['generalInformation']['modelName'])
        self.m = mdb.models[self.ModelName]

        # Defining Variables
        self.SectionName = "ToolSection"
        self.Name = str(data['toolData']['createPartInformation']['Name'])
        self.ReliefAngle = data['toolData']['createPartInformation']['clearanceAngle']
        self.RakeAngle = data['toolData']['createPartInformation']['rakeAngle']
        self.clearanceFaceDimension = data['toolData']['createPartInformation']['clearanceFaceDimension']
        self.rakeFaceDimension = data['toolData']['createPartInformation']['rakeFaceDimension']
        self.Radius = data['toolData']['createPartInformation']['Radius']
        self.Trickness = data['toolData']['createPartInformation']['Trickness']
        self.GlobalSize = data['toolData']['createMeshInformation']['globalSize']
        self.DeviationFactor = data['toolData']['createMeshInformation']['deviationFactor']
        self.MinSizeFactor = data['toolData']['createMeshInformation']['minSizeFactor']
        self.BiasMinSize = data['toolData']['createMeshInformation']['biasMinMeshTool']
        self.BiasMaxSize = data['toolData']['createMeshInformation']['biasMaxMeshTool']
        self.FaceMashSize = data['toolData']['createMeshInformation']['sizeMeshFace']


    def createPart(self):
        # Creating Sketch
        s = self.m.ConstrainedSketch(name='SketchTool', sheetSize=200.0)
        # Creating "References lines"
        s.Line(point1=(0.0, 0.0), point2=(10.6401720046997, 0.0))
        s.HorizontalConstraint(addUndoState=False, entity=s.geometry[2])
        s.Line(point1=(0.0, 10.0), point2=(0.0, 1.25))
        s.VerticalConstraint(addUndoState=False, entity=s.geometry[3])
        s.CoincidentConstraint(entity1=s.vertices[3], entity2=s.vertices[0])
        s.setAsConstruction(objectList=(s.geometry[3], s.geometry[2]))
        s.FixedConstraint(entity=s.geometry[3])
        # Creating Geometry Lines
        s.Line(point1=(3.31129169464111, 1.25408506393433), point2=(11.7126932144165, 5.62865686416626))
        s.Line(point1=(11.98082447052, 7.72666597366333), point2=(11.98082447052, 13.75))
        s.Line(point1=(9.38889980316162, 13.6635837554932), point2=(3.17722415924072, 13.6635837554932))
        s.Line(point1=(3.75, 12.5), point2=(2.99847316741943, 3.93239545822144))
        s.HorizontalConstraint(addUndoState=False, entity=s.geometry[6])
        s.VerticalConstraint(addUndoState=False, entity=s.geometry[5])
        s.CoincidentConstraint(entity1=s.vertices[4], entity2=s.vertices[0])
        s.CoincidentConstraint(entity1=s.vertices[6], entity2=s.vertices[5])
        s.CoincidentConstraint(entity1=s.vertices[8], entity2=s.vertices[7])
        s.CoincidentConstraint(entity1=s.vertices[10], entity2=s.vertices[9])
        s.CoincidentConstraint(entity1=s.vertices[11], entity2=s.vertices[0])
        # Defining Dimension and Angle of the Clearance Face
        s.AngularDimension(line1=s.geometry[4], line2=s.geometry[2], textPoint=(18.2371864318848, 2.41468572616577), value=self.ReliefAngle)
        s.ObliqueDimension(textPoint=(10.5507974624634, -1.29030799865723), value=self.clearanceFaceDimension, vertex1=s.vertices[0], vertex2=s.vertices[5])
        # Defining Dimension and Angle of the Rake Face
        s.AngularDimension(line1=s.geometry[7], line2=s.geometry[3], textPoint=(0.31717586517334, 7.36955785751343), value=self.RakeAngle)
        s.ObliqueDimension(textPoint=(0.0, 8.75), value=self.rakeFaceDimension, vertex1=s.vertices[9], vertex2=s.vertices[0])
        # Defining tool radius
        self.Radius = 0.0001 if self.Radius == 0 else self.Radius
        s.FilletByRadius(curve1=s.geometry[4], curve2=s.geometry[7], nearPoint1=(3.86042213439941, 1.10268461704254), nearPoint2=(4.32205963134766, 0.249606490135193), radius=self.Radius)
        # Align Tool with the coordinate system
        s.CoincidentConstraint(entity1=s.vertices[4], entity2=s.geometry[2])
        s.CoincidentConstraint(entity1=s.vertices[11], entity2=s.geometry[3])
        # Creating Tool Body
        self.p = self.m.Part(dimensionality=THREE_D, name=self.Name, type=DEFORMABLE_BODY)
        self.p.BaseSolidExtrude(depth=self.Trickness, sketch=s)


    def createPartition(self):
        # Creating Sketch Tool Particion     
        s = mdb.models['Model-1'].ConstrainedSketch(gridSpacing=0.03, name='__profile__', sheetSize=1.41, transform=self.p.MakeSketchTransform(sketchPlane=self.p.faces[5], sketchPlaneSide=SIDE1, sketchUpEdge=self.p.edges[7], sketchOrientation=RIGHT, origin=(0.259921, 0.250539, 0.02)))
        self.p.projectReferencesOntoSketch(filter=COPLANAR_EDGES, sketch=s)
        s.Line(point1=(-0.1425, -0.225), point2=(0.135, -0.2025))
        s.Line(point1=(-0.2025, -0.165), point2=(-0.1725, -0.015))
        s.Line(point1=(-0.250097722407341, -0.243631335760593), point2=(-0.25009772240734, -0.24750000002794))
        s.VerticalConstraint(addUndoState=False, entity=s.geometry[9])
        s.Line(point1=(-0.257777099158525, -0.239467180187941), point2=(-0.25196271459572, -0.239467180187941))
        s.HorizontalConstraint(addUndoState=False, entity=s.geometry[10])
        s.delete(objectList=(s.constraints[33], s.constraints[30]))
        s.CoincidentConstraint(entity1=s.vertices[12], entity2=s.vertices[0])
        s.CoincidentConstraint(entity1=s.vertices[13], entity2=s.vertices[5])
        s.CoincidentConstraint(entity1=s.vertices[10], entity2=s.vertices[13])
        s.CoincidentConstraint(entity1=s.vertices[11], entity2=s.vertices[4])
        s.CoincidentConstraint(entity1=s.vertices[8], entity2=s.vertices[10])
        s.CoincidentConstraint(entity1=s.vertices[6], entity2=s.vertices[8])
        s.CoincidentConstraint(entity1=s.vertices[9], entity2=s.geometry[3])
        s.CoincidentConstraint(entity1=s.vertices[7], entity2=s.geometry[4])
        s.ParallelConstraint(entity1=s.geometry[2], entity2=s.geometry[8])
        s.ParallelConstraint(entity1=s.geometry[5], entity2=s.geometry[7])
        self.p.PartitionFaceBySketch(faces=self.p.faces.getSequenceFromMask(('[#20 ]', ), ), sketch=s, sketchUpEdge=self.p.edges[7])
        # Creating Partition
        self.p.PartitionCellByExtrudeEdge(cells=self.p.cells.getSequenceFromMask(('[#1 ]', ), ), edges=(self.p.edges[3], self.p.edges[7]), line=self.p.edges[15], sense=REVERSE)
        self.p.PartitionCellByExtrudeEdge(cells=self.p.cells.getSequenceFromMask(('[#2 ]', ), ), edges=(self.p.edges[12], self.p.edges[14]), line=self.p.edges[20], sense=REVERSE)


    def createSetsandSections(self):
        # Defining the Reference Point
        self.p.ReferencePoint(point=self.p.InterestingPoint(self.p.edges[8], MIDDLE))
        # Creating RF Set
        self.p.Set(name='ToolRP', referencePoints=(self.p.referencePoints[5], ))
        # # Creating Domain Set - Without RF
        self.p.Set(cells=self.p.cells.getSequenceFromMask(('[#7f ]', ), ), name='ToolDomain')
        # Creating Sections
        self.m.HomogeneousSolidSection(material='EMT210 - Extramet', name=self.SectionName, thickness=None)
        self.p.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE, region=self.m.parts['Tool'].sets['ToolDomain'], sectionName=self.SectionName, thicknessAssignment=FROM_SECTION)
        # # Creating Temperature Set
        # self.p.Set(name='ToolTemperatureOutputSet', vertices=self.p.vertices.getSequenceFromMask(('[#4000 ]', ), ))
        # Creating Surfaces
        self.p.Surface(name='ToolSurface', side1Faces=self.p.faces.getSequenceFromMask(('[#19000 ]', ), ))


    def createMesh(self):
        # Creating Mesh
        self.p.setMeshControls(algorithm=ADVANCING_FRONT, regions=self.p.cells.getSequenceFromMask(('[#f ]', ), ), technique=SWEEP)
        self.p.seedPart(deviationFactor=self.DeviationFactor, minSizeFactor=self.MinSizeFactor, size=self.GlobalSize)
        self.p.setElementType(elemTypes=(ElemType(elemCode=C3D8T, elemLibrary=EXPLICIT, secondOrderAccuracy=OFF, distortionControl=DEFAULT), ElemType(elemCode=C3D6T, elemLibrary=EXPLICIT), ElemType(elemCode=C3D4T, elemLibrary=EXPLICIT)), regions=(self.p.cells.getSequenceFromMask(('[#f ]', ), ), ))
        self.p.seedEdgeByBias(biasMethod=SINGLE, constraint=FINER, end1Edges=self.p.edges.getSequenceFromMask(('[#2242490 ]', ), ), end2Edges=self.p.edges.getSequenceFromMask(('[#480a40 ]', ), ), maxSize=self.BiasMaxSize, minSize=self.BiasMinSize)
        self.p.seedEdgeBySize(constraint=FINER, deviationFactor=0.1, edges=self.p.edges.getSequenceFromMask(('[#3190d005 ]', ), ), minSizeFactor=0.1, size=self.FaceMashSize)
        self.p.deleteMesh(regions=self.p.cells.getSequenceFromMask(('[#8 ]', ),))
        self.p.seedEdgeByNumber(constraint=FINER, edges=self.p.edges.getSequenceFromMask(('[#10000000 ]', ), ), number=4)
        self.p.generateMesh()

# if __name__ == "__main__":
#     ToolModel()



