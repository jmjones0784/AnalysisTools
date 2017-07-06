################################################################################
##James Jones
##23 June 2016
##ID_Features.py
##Version 1.0
##Code contained in this tool is UNCLASSIFIED
##This tool designed to work with ArcGIS 10.1 or higher
################################################################################

import arcpy, time, re, os, traceback
from arcpy.sa import *

inDSM = arcpy.GetParameterAsText(0)
inDTM = arcpy.GetParameterAsText(1)
outGDB = arcpy.GetParameterAsText(2)
temp = []

try:
    print "Starting at " + time.strftime("%c")

    ## This section returns the system information for the user.  This is used to help
    ## debug any potential errors returned by the tool.  This information does not compromise
    ## the annonymity of the user or their system.
    ##---------------------------------------------------------------------------------------

    # Get information about ArcGIS version installed...
    arcpy.SetProgressorLabel("Reading installation information...")
    arcpy.AddMessage("--------------------------------")
    installList = arcpy.ListInstallations()
    for install in installList:
        arcpy.AddMessage("Product: ArcGIS for " + install + " " + arcpy.GetInstallInfo(install)["Version"] + " SP " + arcpy.GetInstallInfo()["SPNumber"] + ", Build " + arcpy.GetInstallInfo()["BuildNumber"])
        print("Product: ArcGIS for " + install + " " + arcpy.GetInstallInfo(install)["Version"] + " SP " + arcpy.GetInstallInfo()["SPNumber"] + ", Build " + arcpy.GetInstallInfo()["BuildNumber"])
        arcpy.AddMessage("Installed on: " + arcpy.GetInstallInfo()["InstallDate"] + " " + arcpy.GetInstallInfo()["InstallTime"])
        print("Installed on: " + arcpy.GetInstallInfo()["InstallDate"] + " " + arcpy.GetInstallInfo()["InstallTime"])
        arcpy.AddMessage("Using " + arcpy.ProductInfo() + " license level")
        print("Using " + arcpy.ProductInfo() + " license level")
        arcpy.AddMessage("Script Version 1.0")
        print("Script Version 1.0")
    arcpy.AddMessage("--------------------------------")

    ## This portion of the script will begin by checking the validity of the input files.
    ## It will then subsequently perform the first step of the script which is to subtract the
    ##Digital Terrain Model (DTM) from the Digital Surface Model (DSM).
    ##---------------------------------------------------------------------------------------

    arcpy.SetProgressorLabel("Validating input data...")

    if arcpy.Exists(inDSM) == True:
        print("Input DSM is valid")
        arcpy.AddMessage("Input DSM is valid")
    else:
        print("Error with input DSM, exiting...")
        arcpy.AddMessage("Error with input DSM, exiting...")
        exit

    if arcpy.Exists(inDTM) == True:
        print("Input DTM is valid")
        arcpy.AddMessage("Input DTM is valid")
    else:
        print("Error with input DTM, exiting...")
        arcpy.AddMessage("Error with input DTM, exiting...")
        exit

    arcpy.SetProgressorLabel("Subtracting DTM from DSM...")

    if arcpy.CheckExtension("Spatial") == "Available":
        arcpy.CheckOutExtension("Spatial")
        print("Spatial Analyst successfully checked out")
        arcpy.AddMessage("Spatial Analyst successfully checked out")

    rasDSM = Raster(inDSM)
    rasDTM = Raster(inDTM)
    outRas = os.path.join(outGDB, "TempRas")
    temp.append(outRas)

    arcpy.AddMessage("Subtracting DTM from DSM")
    print("Subtracting DTM from DSM")
    arcpy.env.overwriteOutput == True
    outRas = os.path.join(outGDB, "TempRas")
    outMinus = Minus(inDSM, inDTM)
    outMinus.save(os.path.join(outGDB, "TempRas"))
    arcpy.AddMessage("Successfully subtracted DTM from DSM")
    print("Successfully subtracted DTM from DSM")

    arcpy.SetProgressorLabel("Reclassifying Raster")
    arcpy.AddMessage("Reclassifying raster")
    print("Reclassifying raster")
    reclass = os.path.join(outGDB, "Reclass")
    temp.append(reclass)
    arcpy.gp.Reclassify_sa(outRas, "VALUE", "-1000 0.000000 NODATA;0.000010 1 1; 1 2 2; 2 3 2; 3 4 4; 4 5 4; 5 500 5", reclass, "NODATA")
    arcpy.AddMessage("Successfully reclassified raster")
    print("Successfully reclassified raster")

    arcpy.SetProgressorLabel("Converting Raster features to Vector")
    arcpy.AddMessage("Converting Raster features to Vector")
    print("Converting Raster features to Vector")
    tempFC = os.path.join(outGDB, "PossBuildings")
    arcpy.RasterToPolygon_conversion(reclass, tempFC, "SIMPLIFY", )
    arcpy.AddMessage("Successfully converted Raster features to Vector")
    print("Successfully converted Raster features to Vector")

    arcpy.SetProgressorLabel("Calculating Shape Compactness")
    arcpy.AddMessage("Calculating Shape Compactness")
    print("Calculating Shape Compactness")
    arcpy.AddField_management(tempFC, "Compactness", "FLOAT")
    arcpy.AddField_management(tempFC, "Feature", "SHORT")
    fields = [f.name for f in arcpy.ListFields(tempFC)]
    with arcpy.da.UpdateCursor(tempFC, fields) as cursor:
        for row in cursor:
            row[6] = (row[4]**1.5) / row[5]

            cursor.updateRow(row)

    del cursor
    arcpy.AddMessage("Successfully calculated shape compactness")
    print("Successfully calculated shape compactness")

    arcpy.SetProgressorLabel("Calculating feature likelihood")
    arcpy.AddMessage("Calculating feature likelihood")
    print("Calculating feature likelihood")
    arcpy.AddField_management(tempFC, "Feature", "SHORT")
    fields = [f.name for f in arcpy.ListFields(tempFC)]
    with arcpy.da.UpdateCursor(tempFC, fields) as cursor:
        for row in cursor:
            if (row[3] >= 3 and row[5] >= 25 and row[6] <= 14):
                row[7] = 1
            else:
                row[7] = 0
            cursor.updateRow(row)

    arcpy.AddMessage("Successfully calculated feature likelihood")
    print("Successfully calculated feature likelihood")

    del cursor


except:
    arcpy.SetProgressorLabel("Error")
    print("Uh oh!")
    print("Error at " + time.strftime("%c"))
    tb = sys.exc_info()[2]
    tbinfo = traceback.format_tb(tb)[0]
    pymsg  = "PYTHON ERRORS:\n Traceback info:\n" + tbinfo + "Error info:\n" + str(sys.exc_info()[1])
    msg = "\nArcPy ERRORS:\n" + arcpy.GetMessages(2) + "\n"
    print pymsg
    print msg
    arcpy.AddMessage(pymsg)
    arcpy.AddMessage(msg)
    exit

finally:
    arcpy.SetProgressorLabel("Finishing Script")

    arcpy.AddMessage("Deleting Temporary Rasters and Features")
##    for t in temp:
##        if arcpy.Exists(t) == True:
##            arcpy.Delete_management(t)

    arcpy.CheckInExtension("Spatial")
    print("Returned Spatial Analyst Extension")
    arcpy.AddMessage("Returned Spatial Analyst Extension")
    print("All Finished!")
    arcpy.AddMessage("All Finished!")
    print "Finished at " + time.strftime("%c")
    arcpy.AddMessage("Finished at " + time.strftime("%c"))