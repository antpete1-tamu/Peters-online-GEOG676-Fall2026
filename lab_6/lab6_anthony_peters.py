
# -*- coding: utf-8 -*-

import arcpy
import time
import os


class Toolbox:
    def __init__(self):
        self.label = "Homework 06 Map Generation"
        self.alias = "homework06"
        self.tools = [Tool]


class Tool:
    def __init__(self):
        self.label = "Map Generation Tool"
        self.description = "Generate Graduated Colors or Unique Values maps."

    def getParameterInfo(self):
        """Define parameter definitions."""

        param0 = arcpy.Parameter(
            displayName="Input ArcGIS Pro Project Name",
            name="aprxInputName",
            datatype="DEFile",
            parameterType="Required",
            direction="Input"
        )
        param0.filter.list = ["aprx"]

        param1 = arcpy.Parameter(
            displayName="Layer to Classify",
            name="LayertoClassify",
            datatype="GPLayer",
            parameterType="Required",
            direction="Input"
        )

        param2 = arcpy.Parameter(
            displayName="Output Location",
            name="OutputLocation",
            datatype="DEFolder",
            parameterType="Required",
            direction="Input"
        )

        param3 = arcpy.Parameter(
            displayName="Output Project Name",
            name="OutputProjectName",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )

        param4 = arcpy.Parameter(
            displayName="Map Renderer Type",
            name="MapRendererType",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )

        param4.filter.type = "ValueList"
        param4.filter.list = ["Graduated Colors", "Unique Values"]
        param4.value = "Graduated Colors"

        param5 = arcpy.Parameter(
            displayName="Classification Field",
            name="ClassificationField",
            datatype="Field",
            parameterType="Required",
            direction="Input"
        )

        param5.parameterDependencies = [param1.name]

        params = [param0, param1, param2, param3, param4, param5]
        return params

    def isLicensed(self):
        return True

    def updateParameters(self, parameters):
        return

    def updateMessages(self, parameters):
        return

    def execute(self, parameters, messages):
        """Generate a classified map and save the project."""

        aprxInputName = parameters[0].valueAsText
        LayertoClassify = parameters[1].valueAsText
        OutputLocation = parameters[2].valueAsText
        OutputProjectName = parameters[3].valueAsText
        MapRendererType = parameters[4].valueAsText
        ClassificationField = parameters[5].valueAsText

        arcpy.SetProgressor(
            "step",
            "Starting map generation...",
            0,
            100,
            1
        )

        try:
            arcpy.SetProgressorPosition(0)
            arcpy.AddMessage("Starting map generation...")
            time.sleep(1)

            # Open the ArcGIS Pro project
            aprx = arcpy.mp.ArcGISProject(aprxInputName)

            # Find the layer to classify
            target_layer = None

            for m in aprx.listMaps():
                for layer in m.listLayers():
                    if layer.name == LayertoClassify:
                        target_layer = layer
                        break

                if target_layer is not None:
                    break

            if target_layer is None:
                raise ValueError(
                    "The selected layer was not found in the project."
                )

            if not target_layer.isFeatureLayer:
                raise ValueError(
                    "The selected layer must be a feature layer."
                )

            if not target_layer.supports("SYMBOLOGY"):
                raise ValueError(
                    "The selected layer does not support symbology."
                )

            arcpy.SetProgressorLabel(
                "Layer found. Preparing symbology..."
            )
            arcpy.SetProgressorPosition(33)
            arcpy.AddMessage("Layer successfully located.")
            time.sleep(1)

            # Get layer symbology
            symbology = target_layer.symbology

            # Graduated Colors map
            if MapRendererType == "Graduated Colors":

                numeric_types = {
                    "SmallInteger", "Integer", "Single",
                    "Double", "BigInteger"
                }

                field = next(
                    (f for f in arcpy.ListFields(
                        target_layer.dataSource
                    ) if f.name == ClassificationField),
                    None
                )

                if field is None or field.type not in numeric_types:
                    raise ValueError(
                        "Graduated Colors requires a numeric field."
                    )

                symbology.updateRenderer(
                    "GraduatedColorsRenderer"
                )

                symbology.renderer.classificationField = (
                    ClassificationField
                )
                symbology.renderer.breakCount = 5

                color_ramps = aprx.listColorRamps("Orange*")

                if color_ramps:
                    symbology.renderer.colorRamp = color_ramps[0]

                arcpy.AddMessage(
                    "Graduated Colors renderer applied."
                )

            # Unique Values map
            elif MapRendererType == "Unique Values":

                symbology.updateRenderer(
                    "UniqueValueRenderer"
                )

                symbology.renderer.fields = [
                    ClassificationField
                ]

                color_ramps = aprx.listColorRamps(
                    "Basic Random"
                )

                if color_ramps:
                    symbology.renderer.colorRamp = color_ramps[0]

                arcpy.AddMessage(
                    "Unique Values renderer applied."
                )

            else:
                raise ValueError("Invalid renderer type.")

            # Apply symbology
            target_layer.symbology = symbology

            arcpy.SetProgressorLabel(
                "Map symbology applied..."
            )
            arcpy.SetProgressorPosition(66)
            time.sleep(1)

            # Save the completed project
            output_project = os.path.join(
                OutputLocation,
                OutputProjectName + ".aprx"
            )

            if os.path.exists(output_project):
                raise ValueError(
                    "Output project already exists: "
                    + output_project
                )

            arcpy.SetProgressorLabel(
                "Saving ArcGIS Pro project..."
            )
            arcpy.SetProgressorPosition(99)

            aprx.saveACopy(output_project)

            arcpy.AddMessage(
                "Project successfully saved to: "
                + output_project
            )

            arcpy.SetProgressorLabel(
                "Map generation complete!"
            )
            arcpy.SetProgressorPosition(100)

        except Exception as error:
            arcpy.AddError(str(error))
            raise

        finally:
            arcpy.ResetProgressor()

    def postExecute(self, parameters):
        return
