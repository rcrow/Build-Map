import arcpy

class Toolbox (object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "BuildMap"
        self.alias = ""

        # List of tool classes associated with this toolbox
        self.tools = [BuildAndSymbolize]

class BuildAndSymbolize(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "BuildAndSymbolize"
        self.description = ""
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        param0 = arcpy.Parameter(
            displayName="Input Lines:",
            name="lines",
            datatype="DEFeatureClass",
            parameterType="Required",
            direction="Input")

        param1 = arcpy.Parameter(
            displayName="Input Points:",
            name="points",
            datatype="DEFeatureClass",
            parameterType="Required",
            direction="Input")

        param2 = arcpy.Parameter(
            displayName="Quad Boundary:",
            name="quad",
            datatype="DEFeatureClass",
            parameterType="Required",
            direction="Input")

        param3 = arcpy.Parameter(
            displayName="Reference Layer:",
            name="layer",
            datatype="GPFeatureLayer",
            parameterType="Required",
            direction="Input")

        param4 = arcpy.Parameter(
            displayName="Output all polygons:",
            name="polys",
            datatype="DEFeatureClass",
            parameterType="Required",
            direction="Output")

        param5 = arcpy.Parameter(
            displayName="Output polygons in quad:",
            name="selectPolys",
            datatype="DEFeatureClass",
            parameterType="Required",
            direction="Output")

        param6 = arcpy.Parameter(
            displayName="Output Layer:",
            name="layerOut",
            datatype="GPFeatureLayer",
            parameterType="Required",
            direction="Output")

        params = [param0, param1, param2, param3, param4, param5, param6]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""

        #Inputs
        lines = parameters[0].valueAsText

        points = parameters[1].valueAsText

        quad = parameters[2].valueAsText

        layer = parameters[3].valueAsText #reference layer

        #Outputs
        polys = parameters[4].valueAsText

        selectPolys = parameters[5].valueAsText

        layerOut = parameters[6].valueAsText

        #Builds polyons
        arcpy.FeatureToPolygon_management(in_features=lines+";"+quad,out_feature_class=polys,cluster_tolerance="#",attributes="ATTRIBUTES",label_features=points)
        arcpy.AddMessage("Built")

        arcpy.MakeFeatureLayer_management(polys, "polyLayer")

        #Selects polygons within quad boundary
        arcpy.SelectLayerByLocation_management(in_layer="polyLayer",overlap_type="WITHIN",select_features=quad,search_distance="#",selection_type="NEW_SELECTION")
        arcpy.AddMessage("Selected")

        #Export selected polygons
        arcpy.CopyFeatures_management(in_features="polyLayer",out_feature_class=selectPolys)
        arcpy.AddMessage("Exported")

        arcpy.MakeFeatureLayer_management(selectPolys, "selectLayer")

        #Apply symbology from layer
        arcpy.ApplySymbologyFromLayer_management(in_layer="selectLayer",in_symbology_layer=layer)

        arcpy.AddMessage("Symbolized")

        #Export layer
        arcpy.SaveToLayerFile_management(in_layer="selectLayer",out_layer=layerOut,is_relative_path="#",version="CURRENT")
        arcpy.AddMessage("Exported Layer")

        return
