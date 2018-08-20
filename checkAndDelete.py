import arcpy

#Function checks to see if a feature class exists and then deletes it
def checkAndDelete(path):
    if arcpy.Exists(path):
        print(path +": Exists, Deleted")
        arcpy.Delete_management(path)
    else:
        print(path +": Does Not Exist")