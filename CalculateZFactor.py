################################################################################
##Anthony Calamito
##13 Oct 2014
##CalculateZFactorSingle.py
##Version 2.3
##Code contained in this tool is UNCLASSIFIED
##This tool designed to work with ArcGIS 10.0 or higher.
################################################################################

# Import required modules...
import arcpy, sys, math, decimal, traceback

# Script arguments...
inElevation = arcpy.GetParameterAsText(0)

# Local variables...
arcpy.env.overwriteOutput = 1

## -----------------------------    Main Script   ---------------------------

try:

    ## This section returns the system information for the user.  This is used to help
    ## debug any potential errors returned by the tool.  This information does not compromise
    ## the annonymity of the user or their system.
    ##---------------------------------------------------------------------------------------

    # Get information about ArcGIS version installed...
    arcpy.SetProgressorLabel("Reading install information...")
    arcpy.AddMessage("--------------------------------")
    installList = arcpy.ListInstallations()
    for install in installList:
        arcpy.AddMessage("Product: ArcGIS for " + install + " " + arcpy.GetInstallInfo(install)["Version"] + " SP" + arcpy.GetInstallInfo()["SPNumber"] + ", Build " + arcpy.GetInstallInfo()["BuildNumber"])
        arcpy.AddMessage("Installed on: " + arcpy.GetInstallInfo()["InstallDate"] + " " + arcpy.GetInstallInfo()["InstallTime"])
        arcpy.AddMessage("Using " + arcpy.ProductInfo() + " license level")
        arcpy.AddMessage("Script Version 2.3")
    arcpy.AddMessage("--------------------------------")

    ## This section of the code will analyze a raster dataset, and if necessary, will
    ## calculate its appropriate zFactor for analysis.  Projected and undefined datasets
    ## will not have a zFactor calculated.
    ##---------------------------------------------------------------------------------------

    # Describe input elevation dataset...
    try:
        rasObj = arcpy.Raster(inElevation)

        # Check the coordinate system of the input raster...
        if rasObj.spatialReference.type == "Projected":
            arcpy.AddMessage("Raster: " + rasObj.name + " is projected, no z-factor needed")
        elif rasObj.spatialReference.type == "Unknown":
            arcpy.AddMessage("Raster: " + rasObj.name + " has an unknown coordinate system")
        else:
            # Grab the top and bottom extents of the raster...
            top = float(rasObj.extent.YMax)
            bottom = float(rasObj.extent.YMin)

            # Find the mid-latitude of the raster...
            if (top > bottom):
                height = (top - bottom)
                mid = (height/2) + bottom
            elif (top < bottom):
                height = bottom - top
                mid = (height/2) + top
            else:	# top == bottom
                mid = top

            # Convert degrees to radians for calculation...
            mid = math.radians(mid)

            # Calculate Z-factor for image...
            decimal.getcontext().prec = 28
            decimal.getcontext().rounding = decimal.ROUND_UP
            a = decimal.Decimal("1.0")
            b = decimal.Decimal("111320.0")
            c = decimal.Decimal(str(math.cos(mid)))

            # Z-Factor = 1.0/(111320 * cos(mid-latitude in radians))
            zfactor = a/(b * c)
            zfactor = "%06f" % (zfactor.__abs__())
            arcpy.AddMessage("Raster: " + rasObj.name + " has Z-factor of " + str(zfactor))
    except:
        arcpy.AddWarning("Unable to process input raster.  Raster may be an unsupported type or corrupt.")

except:

    # Code block to handle errors...
    tb = sys.exc_info()[2]
    tbinfo = traceback.format_tb(tb)[0]
    pymsg = "Python Errors:\nTraceback Info:\n" + tbinfo + "\nError Info:\n    " + str(sys.exc_type) + ": " + str(sys.exc_value) + "\n"
    arcpy.AddError(pymsg)
    msgs = "ArcPy Errors:\n" + arcpy.GetMessages(2) + "\n"
    arcpy.AddError(msgs)