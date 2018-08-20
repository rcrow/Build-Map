import arcpy
from checkAndDelete import checkAndDelete
import os

class Toolbox (object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "BuildMap"
        self.alias = "BuildMap"

        # List of tool classes associated with this toolbox
        self.tools = [BuildAndCheck]

class BuildAndCheck(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "BuildAndCheck"
        self.description = ""
        self.canRunInBackground = False

    def getParameterInfo(self):
        # """Define parameter definitions"""
        param0 = arcpy.Parameter(
            displayName="Input SDE connection name:",
            name="connection",
            datatype="GPString",
            parameterType="Required",
            direction="Input")
        #
        # param1 = arcpy.Parameter(
        #     displayName="Input Points:",
        #     name="points",
        #     datatype="GPFeatureLayer",
        #     parameterType="Required",
        #     direction="Input")
        #
        # param2 = arcpy.Parameter(
        #     displayName="Quad Boundary:",
        #     name="quad",
        #     datatype="GPFeatureLayer",
        #     parameterType="Optional",
        #     direction="Input")
        #
        # param3 = arcpy.Parameter(
        #     displayName="Output polygons in quad:",
        #     name="selectPolys",
        #     datatype="DEFeatureClass",
        #     parameterType="Required",
        #     direction="Output")
        #
        # param4 = arcpy.Parameter(
        #     displayName="Joined polygons in quad:",
        #     name="joinPolys",
        #     datatype="DEFeatureClass",
        #     parameterType="Required",
        #     direction="Output")
        #
        # param5 = arcpy.Parameter(
        #     displayName="Output Layer:",
        #     name="layerOut",
        #     datatype="GPLayer",
        #     parameterType="Required",
        #     direction="Output")
        #
        # param6 = arcpy.Parameter(
        #     displayName="Add to mxd?",
        #     name="addToMXD",
        #     datatype="Boolean",
        #     parameterType="Optional",
        #     direction="Input")
        #
        params = [param0]
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
        arcpy.env.overwriteOutput = True
        # connectionPath = r"\\igswzcwwgsrio\loco\GeologicMaps_InProgress\LOCOBigBrother"
        # server= "igswzdwgdbkiva"
        # db = "rscgeo"
        #
        # arcpy.CreateDatabaseConnection_management(connectionPath, "ConnectForBuildMap_" + server + "_" + db,
        #                                           "POSTGRESQL", server, "OPERATING_SYSTEM_AUTH", "#", "#", "#",
        #                                           db)
        #
        # connection = connectionPath + "\\" + "ConnectForBuildMap_"+server +"_"+ db+".sde"
        connection = parameters[0].valueAsText

        lines = connection +r"\rscgeo.dbo.RSCGeologicMap\rscgeo.dbo.RSCContactsAndFaults"

        points = connection +r"\rscgeo.dbo.RSCGeologicMap\rscgeo.dbo.RSCMapUnitPoints"

        quad = r"\\igswzcwwgsrio\loco\GeologicMaps_InProgress\LOCOBigBrother\LOCOBigBrother.gdb\SMSE_boundary"

        layer = r"\\Igswzcwwgsrio\loco\Geology\SDE_Stuff\LayerFilesAndStyles\BuildAndCheckTemplatev2.lyr"

        # Outputs
        selectPolys = r"\\igswzcwwgsrio\loco\GeologicMaps_InProgress\LOCOBigBrother\LOCOBigBrother.gdb\SMSE_BuildMapFiles\selectPolys"

        joinPolys = r"\\igswzcwwgsrio\loco\GeologicMaps_InProgress\LOCOBigBrother\LOCOBigBrother.gdb\SMSE_BuildMapFiles\joinedPolys"

        layerOut = r"\\igswzcwwgsrio\loco\GeologicMaps_InProgress\LOCOBigBrother\RSC_BigBrotherFiles\LOCO_RSC_PolyCheck.lyr"
        layerName = "LOCO_RSC_PolyCheck"

        addToMXD = True

        polys = r"\\igswzcwwgsrio\loco\GeologicMaps_InProgress\LOCOBigBrother\LOCOBigBrother.gdb\SMSE_BuildMapFiles\polys"

        if quad:
            arcpy.AddMessage("  Quad Name: " + quad)
            # Builds polyons
            arcpy.AddMessage("  Building Polygons")
            arcpy.FeatureToPolygon_management(in_features=lines + ";" + quad,
                                              out_feature_class=polys,
                                              cluster_tolerance="#",
                                              attributes="ATTRIBUTES",
                                              label_features=points)

            arcpy.AddMessage("  Making Layer")
            arcpy.MakeFeatureLayer_management(polys, "polyLayer")

            # Selects polygons within quad boundary
            arcpy.AddMessage("  Selecting Within Quad")
            arcpy.SelectLayerByLocation_management(in_layer="polyLayer",
                                                   overlap_type="WITHIN",
                                                   select_features=quad,
                                                   search_distance="#",
                                                   selection_type="NEW_SELECTION")

            # Export selected polygons
            arcpy.AddMessage("  Exporting")
            arcpy.CopyFeatures_management(in_features="polyLayer",
                                          out_feature_class=selectPolys)


        else:
            arcpy.AddMessage("  No Quad Boundary")
            # Builds polyons
            arcpy.AddMessage("  Building Polygons")
            arcpy.FeatureToPolygon_management(in_features=lines,
                                              out_feature_class=polys,
                                              cluster_tolerance="#",
                                              attributes="ATTRIBUTES",
                                              label_features=points)
            arcpy.AddMessage("  Making Layer")
            arcpy.MakeFeatureLayer_management(polys, "polyLayer")

            arcpy.AddMessage("  Exporting")
            arcpy.CopyFeatures_management(in_features="polyLayer",
                                          out_feature_class=selectPolys)

        arcpy.AddMessage("  Joining")
        arcpy.SpatialJoin_analysis(target_features=selectPolys,
                                   join_features=points,
                                   out_feature_class=joinPolys,
                                   join_operation="JOIN_ONE_TO_ONE",
                                   join_type="KEEP_ALL",
                                   # field_mapping="""type "Type" true false false 255 Text 0 0 ,First,#,locogeo.sde.PKHContactsAndFaults,type,-1,-1;isconcealed "IsConcealed" true false false 1 Text 0 0 ,First,#,locogeo.sde.PKHContactsAndFaults,isconcealed,-1,-1;existenceconfidence "ExistenceConfidence" true false false 50 Text 0 0 ,First,#,locogeo.sde.PKHContactsAndFaults,existenceconfidence,-1,-1;identityconfidence "IdentityConfidence" true false false 50 Text 0 0 ,First,#,locogeo.sde.PKHContactsAndFaults,identityconfidence,-1,-1;locationconfidencemeters "LocationConfidenceMeters" true false false 8 Double 8 38 ,First,#,locogeo.sde.PKHContactsAndFaults,locationconfidencemeters,-1,-1;symbol "Symbol" true true false 255 Text 0 0 ,First,#,locogeo.sde.PKHContactsAndFaults,symbol,-1,-1;label "Label" true true false 50 Text 0 0 ,First,#,locogeo.sde.PKHContactsAndFaults,label,-1,-1;datasourceid "DataSourceID" true false false 50 Text 0 0 ,First,#,locogeo.sde.PKHContactsAndFaults,datasourceid,-1,-1;notes "Notes" true true false 255 Text 0 0 ,First,#,locogeo.sde.PKHContactsAndFaults,notes,-1,-1;creator "Creator" false true false 255 Text 0 0 ,First,#,locogeo.sde.PKHContactsAndFaults,creator,-1,-1;createdate "CreateDate" false true false 36 Date 0 0 ,First,#,locogeo.sde.PKHContactsAndFaults,createdate,-1,-1;editor "Editor" false true false 255 Text 0 0 ,First,#,locogeo.sde.PKHContactsAndFaults,editor,-1,-1;editdate "EditDate" false true false 36 Date 0 0 ,First,#,locogeo.sde.PKHContactsAndFaults,editdate,-1,-1;datasourcenotes "datasourcenotes" true true false 150 Text 0 0 ,First,#,locogeo.sde.PKHContactsAndFaults,datasourcenotes,-1,-1;st_length_shape_ "st_length_shape_" false false true 0 Double 0 0 ,First,#,locogeo.sde.PKHContactsAndFaults,st_length(shape),-1,-1;mapunit "MapUnit" true false false 10 Text 0 0 ,First,#,locogeo.sde.PKHMapUnitPoints,mapunit,-1,-1;identityconfidence_1 "IdentityConfidence" true false false 50 Text 0 0 ,First,#,locogeo.sde.PKHMapUnitPoints,identityconfidence,-1,-1;label_1 "Label" true true false 50 Text 0 0 ,First,#,locogeo.sde.PKHMapUnitPoints,label,-1,-1;symbol_1 "Symbol" true true false 255 Text 0 0 ,First,#,locogeo.sde.PKHMapUnitPoints,symbol,-1,-1;notes_1 "Notes" true true false 255 Text 0 0 ,First,#,locogeo.sde.PKHMapUnitPoints,notes,-1,-1;datasourceid_1 "DataSourceID" true false false 50 Text 0 0 ,First,#,locogeo.sde.PKHMapUnitPoints,datasourceid,-1,-1;mapunit2 "MapUnit2" true true false 50 Text 0 0 ,First,#,locogeo.sde.PKHMapUnitPoints,mapunit2,-1,-1;origunit "OrigUnit" true true false 50 Text 0 0 ,First,#,locogeo.sde.PKHMapUnitPoints,origunit,-1,-1;creator_1 "Creator" false true false 255 Text 0 0 ,First,#,locogeo.sde.PKHMapUnitPoints,creator,-1,-1;createdate_1 "CreateDate" false true false 36 Date 0 0 ,First,#,locogeo.sde.PKHMapUnitPoints,createdate,-1,-1;editor_1 "Editor" false true false 255 Text 0 0 ,First,#,locogeo.sde.PKHMapUnitPoints,editor,-1,-1;editdate_1 "EditDate" false true false 36 Date 0 0 ,First,#,locogeo.sde.PKHMapUnitPoints,editdate,-1,-1;datasourcenotes_1 "datasourcenotes_1" true true false 150 Text 0 0 ,First,#,locogeo.sde.PKHMapUnitPoints,datasourcenotes,-1,-1;facies "facies" true true false 50 Text 0 0 ,First,#,locogeo.sde.PKHMapUnitPoints,facies,-1,-1""",
                                   match_option="INTERSECT",
                                   search_radius="",
                                   distance_field_name="")
        arcpy.MakeFeatureLayer_management(joinPolys, layerName)

        # Apply symbology from layer
        arcpy.AddMessage("  Symbolizing")
        arcpy.ApplySymbologyFromLayer_management(in_layer=layerName,
                                                 in_symbology_layer=layer)

        # Export layer
        arcpy.SaveToLayerFile_management(in_layer=layerName,
                                         out_layer=layerOut,
                                         is_relative_path="#",
                                         version="CURRENT")
        arcpy.AddMessage("  Exporting")

        if addToMXD:
            arcpy.AddMessage("  Adding / Removing from the MXD")
            mxd = arcpy.mapping.MapDocument("CURRENT")
            df = arcpy.mapping.ListDataFrames(mxd, "*")[0]

            sourceLayer3 = arcpy.mapping.Layer(layerOut)
            arcpy.mapping.AddLayer(df, sourceLayer3, "AUTO_ARRANGE")

        # os.remove(connection)
        arcpy.env.overwriteOutput = False
        return

# class BuildAndSymbolize(object):
#     def __init__(self):
#         """Define the tool (tool name is the name of the class)."""
#         self.label = "BuildAndSymbolize"
#         self.description = ""
#         self.canRunInBackground = False
#
#     def getParameterInfo(self):
#         """Define parameter definitions"""
#         param0 = arcpy.Parameter(
#             displayName="Input Lines:",
#             name="lines",
#             datatype="GPFeatureLayer",
#             parameterType="Required",
#             direction="Input")
#
#         param1 = arcpy.Parameter(
#             displayName="Input Points:",
#             name="points",
#             datatype="GPFeatureLayer",
#             parameterType="Required",
#             direction="Input")
#
#         param2 = arcpy.Parameter(
#             displayName="Quad Boundary:",
#             name="quad",
#             datatype="GPFeatureLayer",
#             parameterType="Optional",
#             direction="Input")
#
#         param3 = arcpy.Parameter(
#             displayName="Reference Layer:",
#             name="layer",
#             datatype="GPFeatureLayer",
#             parameterType="Required",
#             direction="Input")
#
#         param4 = arcpy.Parameter(
#             displayName="Output all polygons:",
#             name="polys",
#             datatype="DEFeatureClass",
#             parameterType="Required",
#             direction="Output")
#
#         param5 = arcpy.Parameter(
#             displayName="Output polygons in quad:",
#             name="selectPolys",
#             datatype="DEFeatureClass",
#             parameterType="Required",
#             direction="Output")
#
#         param6 = arcpy.Parameter(
#             displayName="Output Layer:",
#             name="layerOut",
#             datatype="GPLayer",
#             parameterType="Required",
#             direction="Output")
#
#         param7 = arcpy.Parameter(
#             displayName="Add to mxd?",
#             name="addToMXD",
#             datatype="Boolean",
#             parameterType="Optional",
#             direction="Input")
#
#         params = [param0, param1, param2, param3, param4, param5, param6, param7]
#         return params
#
#     def isLicensed(self):
#         """Set whether tool is licensed to execute."""
#         return True
#
#     def updateParameters(self, parameters):
#         """Modify the values and properties of parameters before internal
#         validation is performed.  This method is called whenever a parameter
#         has been changed."""
#         return
#
#     def updateMessages(self, parameters):
#         """Modify the messages created by internal validation for each tool
#         parameter.  This method is called after internal validation."""
#         return
#
#     def execute(self, parameters, messages):
#         """The source code of the tool."""
#
#         #Inputs
#         lines = parameters[0].valueAsText
#
#         points = parameters[1].valueAsText
#
#         quad = parameters[2].valueAsText
#
#         layer = parameters[3].valueAsText #reference layer
#
#         #Outputs
#         polys = parameters[4].valueAsText
#
#         selectPolys = parameters[5].valueAsText
#
#         layerOut = parameters[6].valueAsText
#
#         addToMXD = parameters[6].valueAsText
#
#         arcpy.env.overwriteOutput = True
#
#         if quad:
#             #Builds polyons
#             arcpy.FeatureToPolygon_management(in_features=lines+";"+quad,
#                                               out_feature_class=polys,
#                                               cluster_tolerance="#",
#                                               attributes="ATTRIBUTES",
#                                               label_features=points)
#             arcpy.AddMessage("Built")
#             checkAndDelete("polyLayer")
#             arcpy.MakeFeatureLayer_management(polys, "polyLayer")
#
#             #Selects polygons within quad boundary
#             arcpy.SelectLayerByLocation_management(in_layer="polyLayer",
#                                                    overlap_type="WITHIN",
#                                                    select_features=quad,
#                                                    search_distance="#",
#                                                    selection_type="NEW_SELECTION")
#             arcpy.AddMessage("Selected")
#         else:
#             arcpy.FeatureToPolygon_management(in_features=lines,
#                                               out_feature_class=polys,
#                                               cluster_tolerance="#",
#                                               attributes="ATTRIBUTES",
#                                               label_features=points)
#             arcpy.AddMessage("Built")
#             checkAndDelete("polyLayer")
#             arcpy.MakeFeatureLayer_management(polys, "polyLayer")
#
#         #Export selected polygons
#         arcpy.CopyFeatures_management(in_features="polyLayer",
#                                       out_feature_class=selectPolys)
#         arcpy.AddMessage("Exported")
#
#         checkAndDelete("Symbolized Map")
#         arcpy.MakeFeatureLayer_management(selectPolys, "Symbolized Map")
#
#         #Apply symbology from layer
#         arcpy.ApplySymbologyFromLayer_management(in_layer="Symbolized Map",
#                                                  in_symbology_layer=layer)
#
#         arcpy.AddMessage("Symbolized")
#
#         #Export layer
#         arcpy.SaveToLayerFile_management(in_layer="Symbolized Map",
#                                          out_layer=layerOut,
#                                          is_relative_path="#",
#                                          version="CURRENT")
#         arcpy.AddMessage("Exported Layer")
#
#         if addToMXD:
#             arcpy.AddMessage("  Adding / Removing from the MXD")
#             mxd = arcpy.mapping.MapDocument("CURRENT")
#             df = arcpy.mapping.ListDataFrames(mxd, "*")[0]
#
#             sourceLayer2 = arcpy.mapping.Layer(selectPolys)
#             arcpy.mapping.RemoveLayer(df, sourceLayer2)
#
#             sourceLayer1 = arcpy.mapping.Layer(polys)
#             arcpy.mapping.RemoveLayer(df, sourceLayer1)
#
#             sourceLayer3 = arcpy.mapping.Layer("Symbolized Map")
#             arcpy.mapping.AddLayer(df, sourceLayer3, "TOP")
#
#         arcpy.env.overwriteOutput = False
#
#         return


