import arcpy

#Inputs
lines = r"E:/users/rcrow/Documents/GOOGLEDRIVE/Python/BuildMap/LocoSDE_20160617_162700.gdb/PKHContactsAndFaults"

points = r"E:/users/rcrow/Documents/GOOGLEDRIVE/Python/BuildMap/LocoSDE_20160617_162700.gdb/PKHMapUnitPoints"

quad = r"E:/users/rcrow/Documents/GOOGLEDRIVE/Python/BuildMap/castleRockQuad.shp"

layer = r"E:/users/rcrow/Documents/GOOGLEDRIVE/Python/BuildMap/referenceLayer.lyr"

#Outputs
polys = r"E:/users/rcrow/Documents/GOOGLEDRIVE/Python/BuildMap/LocoSDE_20160617_162700.gdb/TestPoly4"

selectPolys = r"E:/users/rcrow/Documents/GOOGLEDRIVE/Python/BuildMap/LocoSDE_20160617_162700.gdb/selectPoly4"

layerOut = r"E:/users/rcrow/Documents/GOOGLEDRIVE/Python/BuildMap/MapTest4.lyr"

#Builds polyons
arcpy.FeatureToPolygon_management(in_features=lines+";"+quad,out_feature_class=polys,cluster_tolerance="#",attributes="ATTRIBUTES",label_features=points)
print "Built"

arcpy.MakeFeatureLayer_management(polys, "polyLayer")

#Selects polygons within quad boundary
arcpy.SelectLayerByLocation_management(in_layer="polyLayer",overlap_type="WITHIN",select_features=quad,search_distance="#",selection_type="NEW_SELECTION")
print "Selected"

#Export selected polygons
arcpy.CopyFeatures_management(in_features="polyLayer",out_feature_class=selectPolys)
print "Exported"

arcpy.MakeFeatureLayer_management(selectPolys, "selectLayer")

#Apply symbology from layer
arcpy.ApplySymbologyFromLayer_management(in_layer="selectLayer",in_symbology_layer=layer)
print "Symbolized"

#Export layer
arcpy.SaveToLayerFile_management(in_layer="selectLayer",out_layer=layerOut,is_relative_path="#",version="CURRENT")
print "Exported Layer"
