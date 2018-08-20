import arcpy

class Toolbox (object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "CheckUnique"
        self.alias = "CheckUnique"

        # List of tool classes associated with this toolbox
        self.tools = [CheckUnique]

class CheckUnique(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "CheckUnique"
        self.description = ""
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        param0 = arcpy.Parameter(
            displayName="Input Polygons:",
            name="polys",
            datatype="GPFeatureLayer",
            parameterType="Required",
            direction="Input")

        param1 = arcpy.Parameter(
            displayName="Label Points:",
            name="labels",
            datatype="GPFeatureLayer",
            parameterType="Required",
            direction="Input")

        param2 = arcpy.Parameter(
            displayName="Workspace:",
            name="workspace",
            datatype="DEWorkspace",
            parameterType="Required",
            direction="Input")


        params = [param0, param1, param2]
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

        # returns 0 if different 1 if same (code from: http://stackoverflow.com/questions/3844801/check-if-all-elements-in-a-list-are-identical)
        def checkEqual1(iterator):
            iterator = iter(iterator)
            try:
                first = next(iterator)
            except StopIteration:
                return True
            return all(first == rest for rest in iterator)

        #arcpy.env.overwriteOutput = True
        #arcpy.AddMessage(arcpy.env.scratchGDB)
        #arcpy.AddMessage(arcpy.env.scratchFolder)
        #Inputs
        polys = parameters[0].valueAsText
        labels = parameters[1].valueAsText
        workspace = parameters[2].valueAsText
        #arcpy.AddMessage(workspace)
        #output = parameters[2].valueAsText
        field = "mapunit"
        arcpy.env.workspace = workspace
        #arcpy.env.scratchGDB
        #polysLayer = arcpy.env.scratchFolder + r'\polysLayer'

        fieldList = arcpy.ListFields(polys)
        #arcpy.AddMessage(fieldList)
        if "UniqueCount" not in fieldList:
            arcpy.AddMessage("  adding the field")
            arcpy.AddField_management(polys, "UniqueCheck", "SHORT")
            arcpy.AddField_management(polys, "MultipleLabels", "TEXT")
        else:
            arcpy.AddMessage(" the field is already present")

        arcpy.MakeFeatureLayer_management(polys, "polysLayer")
        arcpy.SelectLayerByAttribute_management("polysLayer", "CLEAR_SELECTION")
        arcpy.MakeFeatureLayer_management(labels, "labelsLayer")
        arcpy.SelectLayerByAttribute_management("labelsLayer", "CLEAR_SELECTION")
        mapUnitList = []
        with arcpy.da.UpdateCursor(polys, ["OBJECTID","UniqueCheck","MultipleLabels"]) as cursor:
            for id in cursor:
                arcpy.AddMessage("  "+str(id[0]))
                Expression = "OBJECTID = {}".format(id[0])
                arcpy.SelectLayerByAttribute_management("polysLayer", "NEW_SELECTION", Expression)
                arcpy.CopyFeatures_management(in_features="polysLayer",
                                              out_feature_class="SELECTEDpolys")
                arcpy.SelectLayerByLocation_management(in_layer="labelsLayer",
                                                       overlap_type="WITHIN",
                                                       select_features="SELECTEDpolys",
                                                       search_distance="#",
                                                       selection_type="NEW_SELECTION")
                arcpy.CopyFeatures_management(in_features="labelsLayer",
                                              out_feature_class="SELECTEDlabels")
                with arcpy.da.SearchCursor("labelsLayer", "mapunit") as cursor2:
                    count=1
                    for mapunit, in cursor2:
                        #arcpy.AddMessage("  "+mapunit)
                        mapUnitList.append(mapunit)
                        count=count+1
                    arcpy.AddMessage("  "+str(mapUnitList))
                    if len(str(mapUnitList))>255:
                        arcpy.AddMessage("  Crazy amount of label points!!!!!!")
                        id[2] = "Crazy amount of label points!!!!!"
                    else:
                        id[2] = str(mapUnitList)
                    if checkEqual1(mapUnitList) == 1: #returns 0 if different 1 if same
                        id[1]=1
                        arcpy.AddMessage("  same")
                    elif checkEqual1(mapUnitList) == 0:
                        id[1]=0
                        cursor.updateRow(id)
                        arcpy.AddMessage("  different")
                    else:
                        arcpy.AddMessage("  Something is wrong!!!")
                    #arcpy.AddMessage(id[1])
                    mapUnitList[:]=[] #empties the list
                cursor.updateRow(id)

        return
