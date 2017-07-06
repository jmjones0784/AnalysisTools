################################################################################
##James Jones
##7 June 2016
##EllipseDensity_NGA.py
##Version 1.0
##Code contained in this tool is UNCLASSIFIED
##This tool designed to work with ArcGIS 10.1
################################################################################

# Import arcpy module
import sys, os, traceback, arcpy
from arcpy import env
arcpy.env.overwriteOutput = 1

# Script arguments
inputPoly = arcpy.GetParameterAsText(0)
Output = arcpy.GetParameterAsText(1)
tempWS = "D:\Iraq\Working.gdb"

# Local variables:
outUnion = os.path.join(tempWS, "outUnion")
outSinglepart = os.path.join(tempWS, "outSinglepart")
outPts = os.path.join(tempWS, "outPts")
outSpatialjoin = os.path.join(tempWS, "outSpatialjoin")

## -----------------------------    Main Script   ---------------------------

try:

    # Shenanigans to Get Spatial Join to Work Correctly
    arcpy.AddMessage("Adding Field...")
    arcpy.SetProgressorLabel("Step 1:  Adding relevant field...")
    arcpy.AddField_management(inputPoly, "one", "SHORT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    arcpy.AddMessage("Calculating...")
    arcpy.SetProgressorLabel("Step 2:  Calculating relevant field...")
    arcpy.CalculateField_management(inputPoly, "one", "1", "VB", "")
    arcpy.AddMessage("Unioning...")
    arcpy.SetProgressorLabel("Step 3:  Unioning data to itself...")
    arcpy.Union_analysis(inputPoly, outUnion, "ALL", "", "GAPS")
    arcpy.AddMessage("Multipart To Singlepart...")
    arcpy.SetProgressorLabel("Step 4:  Converting to singlepart feature...")
    arcpy.MultipartToSinglepart_management(outUnion, outSinglepart)
    # Generation of Point Data for Spatial Join
    arcpy.AddMessage("Feature to Point...")
    arcpy.SetProgressorLabel("Step 5:  Converting Features to Points...")
    arcpy.FeatureToPoint_management(outSinglepart, outPts, "INSIDE")
    arcpy.AddMessage("Spatial Join...")
    arcpy.SetProgressorLabel("Step 6:  Joining data spatially...")
    arcpy.SpatialJoin_analysis(outSinglepart, outPts, outSpatialjoin, "JOIN_ONE_TO_ONE","KEEP_ALL", "", "INTERSECT", "", "")
    # Final Dissolve
    arcpy.AddMessage('Dissolving...\n')
    arcpy.SetProgressorLabel("Step 7:  Dissolving...")
    arcpy.Dissolve_management (outSpatialjoin, Output, "Join_count", "", "", "")
    arcpy.AddMessage("Adding frequency count field...")
    arcpy.SetProgressorLabel("Step 8:  Adding frequency count field...")
    arcpy.AddField_management(Output, "freqCount", "LONG", "", "", "", "Frequency Count", "NULLABLE", "NON_REQUIRED", "")
    arcpy.CalculateField_management(Output, "freqCount", "!Join_count!", "PYTHON_9.3")
    arcpy.DeleteField_management(Output, "Join_count")
    # Adds Output to MXD
    arcpy.SetParameterAsText(1, Output)

except:
    # Code block to handle errors...
    tb = sys.exc_info()[2]
    tbinfo = traceback.format_tb(tb)[0]
    pymsg = "Python Errors:\nTraceback Info:\n" + tbinfo + "\nError Info:\n    " + str(sys.exc_type) + ": " + str(sys.exc_value) + "\n"
    arcpy.AddError(pymsg)
    msgs = "ArcPy Errors:\n" + arcpy.GetMessages(2) + "\n"
    arcpy.AddError(msgs)
    raise Exception

finally:
    # Process: Process Successful
    arcpy.AddMessage('Process Successfully Completed!!!\n')



