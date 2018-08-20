import arcpy

arcpy.ImportToolbox(r"\\Igswzcwwgsrio\loco\Team\Crow\ArcTools\BuildPolygons.tbx")

#Gets time and date to add to export
time = datetime.datetime.now() #Get system time
if len(str(time.month))==1:
    month="0"+str(time.month)
else:
    month=str(time.month)
if len(str(time.day)) == 1:
    day = "0" + str(time.day)
else:
    day = str(time.day)
if len(str(time.hour)) == 1:
    hour = "0" + str(time.hour)
else:
    hour = str(time.hour)
if len(str(time.minute)) == 1:
    minute = "0" + str(time.minute)
else:
    minute = str(time.minute)

timeDateString = str(time.year) + month + day + "_" + hour + minute
print timeDateString

#sde = r"Database Connections\Connection to igswzcwggsmoki.wr.usgs.gov.sde\locogeo.sde.PKHGeologicMap"
sde = r"\\Igswzcwwgsrio\loco\Team\Crow\CRevolutionMerged\CRevolution2017.gdb\bigBrother"
exportDatabase = r"\\Igswzcwwgsrio\loco\Team\Crow\CRevolutionMerged\CRevolution2017.gdb\bigBrother"
exportFolder = r"\\Igswzcwwgsrio\loco\Team\Crow\CRevolutionMerged\bigBrother"

# lines = sde + r"\locogeo.sde.PKHContactsAndFaults"
# points = sde + r"\locogeo.sde.PKHMapUnitPoints"

lines = sde + r"\TestLines"
points = sde + r"\TestPoints"

justPoly = exportDatabase + r"\BuiltPoly" + timeDateString

outPolyCheck = exportDatabase + r"\PolyCheck" + timeDateString
outLayerPolyCheck = exportFolder + r"\PolyCheck" + timeDateString + ".lyr"
print(outLayerPolyCheck)

arcpy.FeatureToPolygon_management(lines, justPoly, "", "ATTRIBUTES", points)

arcpy.SpatialJoin_analysis(target_features=justPoly,
                           join_features=points,
                           out_feature_class=outPolyCheck,
                           join_operation="JOIN_ONE_TO_ONE",
                           join_type="KEEP_ALL",
                           field_mapping="""mapunit "MapUnit" true true false 10 Text 0 0 ,First,#,"""+justPoly+""",mapunit,-1,-1""",
                           match_option="INTERSECT", search_radius="", distance_field_name="")

arcpy.MakeFeatureLayer_management(in_features=outPolyCheck,
                                  out_layer=outLayerPolyCheck,
                                  where_clause="",
                                  workspace="",
                                  field_info="OBJECTID OBJECTID VISIBLE NONE;SHAPE SHAPE VISIBLE NONE;Join_Count Join_Count VISIBLE NONE;TARGET_FID TARGET_FID VISIBLE NONE;mapunit mapunit VISIBLE NONE;SHAPE_Length SHAPE_Length VISIBLE NONE;SHAPE_Area SHAPE_Area VISIBLE NONE")

arcpy.ApplySymbologyFromLayer_management(in_layer=outLayerPolyCheck,
                                         in_symbology_layer=r"\\Igswzcwwgsrio\loco\Geology\SDE_Stuff\LayerFilesAndStyles\BuildAndCheckTemplate.lyr")

arcpy.SaveToLayerFile_management(in_layer=outLayerPolyCheck,
                                 out_layer=outLayerPolyCheck,
                                 is_relative_path="", version="CURRENT")


# #Containers to add selected to
# sBouseGood = exportDatabase + '/sBouseGood' + "_" + timeDateString
# sBouseBad = exportDatabase + '/sBouseBad' + "_" + timeDateString
#
# #Select
# arcpy.Select_analysis(outPolyCheck, sBouseGood, "Join_Count =1 AND mapunit LIKE 'Tbo%'")
# arcpy.Select_analysis(outPolyCheck, sBouseBad, "Join_Count >1 AND mapunit LIKE 'Tbo%'")
