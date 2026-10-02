# -*- coding: utf-8 -*-

import arcpy


class Toolbox:
    def __init__(self):
        """Define the toolbox."""
        self.label = "Lab 05 Toolbox"
        self.alias = "lab05"

        # List of tool classes associated with this toolbox
        self.tools = [GarageBufferIntersect]


class GarageBufferIntersect:
    def __init__(self):
        """Define the tool."""
        self.label = "Garage Buffer and Intersect"
        self.description = "Buffers garage points and intersects the buffer with campus buildings."

    def getParameterInfo(self):
        """Define the tool parameters."""

        # Garage points input
        garage_points = arcpy.Parameter(
            displayName="Garage Points",
            name="garage_points",
            datatype="GPFeatureLayer",
            parameterType="Required",
            direction="Input"
        )

        # Buildings input
        buildings = arcpy.Parameter(
            displayName="Buildings",
            name="buildings",
            datatype="GPFeatureLayer",
            parameterType="Required",
            direction="Input"
        )

        # Buffer distance input
        buffer_distance = arcpy.Parameter(
            displayName="Buffer Distance",
            name="buffer_distance",
            datatype="GPLinearUnit",
            parameterType="Required",
            direction="Input"
        )

        # Garage buffer output
        garage_buffered = arcpy.Parameter(
            displayName="Garage Buffered",
            name="garage_buffered",
            datatype="DEFeatureClass",
            parameterType="Required",
            direction="Output"
        )

        # Intersection output
        intersection_output = arcpy.Parameter(
            displayName="Intersection Output",
            name="intersection_output",
            datatype="DEFeatureClass",
            parameterType="Required",
            direction="Output"
        )

        params = [
            garage_points,
            buildings,
            buffer_distance,
            garage_buffered,
            intersection_output
        ]

        return params

    def isLicensed(self):
        """Set whether the tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        return

    def updateMessages(self, parameters):
        return

    def execute(self, parameters, messages):
        """Buffer garage points and intersect with buildings."""

        garage_points = parameters[0].valueAsText
        buildings = parameters[1].valueAsText
        buffer_distance = parameters[2].valueAsText
        garage_buffered = parameters[3].valueAsText
        intersection_output = parameters[4].valueAsText

        # Buffer the garages
        arcpy.Buffer_analysis(
            garage_points,
            garage_buffered,
            buffer_distance
        )

        # Intersect the garage buffers with buildings
        arcpy.Intersect_analysis(
            [garage_buffered, buildings],
            intersection_output,
            "ALL"
        )

        return

    def postExecute(self, parameters):
        return