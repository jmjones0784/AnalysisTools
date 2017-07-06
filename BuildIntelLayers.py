import arcpy, os, traceback, time

try:

    dataWS = r''
    binWS = r''
    buildings = r''
    completedFC = []

    print "Starting at " + time.strftime("%c")

    featCount = 0

    for dirpath, dirnames, filenames in arcpy.da.Walk(dataWS, datatype="FeatureClass"):
        for file in filenames:
            filepath = os.path.join(dataWS, file)
            outFile = file + "_FP"
            outfeature = os.path.join(binWS, outFile)

            featCount += 1

            print "Joining Spatially..."

            if featCount == 1:
                arcpy.SpatialJoin_analysis(buildings, filepath, outfeature)
            else:
                newFP = completedFC[len(completedFC) - 1]
                arcpy.SpatialJoin_analysis(newFP, filepath, outfeature)

            fieldN = arcpy.ValidateFieldName(file, binWS)

            print "Adding field..."

            arcpy.AddField_management(outfeature, fieldN, "SHORT")

            print "Calculating Field..."
            arcpy.CalculateField_management(in_table=outfeature, field=fieldN, expression="!Join_Count!", expression_type="PYTHON_9.3", code_block="")

            print "Deleting Field..."

            arcpy.DeleteField_management(outfeature, ["Join_Count", "TARGET_FID"])

            completedFC.append(outfeature)

            print "Completed " + file + ", beginning next feature..."

except:
    print("Uh oh!")
    print("Error at " + time.strftime("%c"))

    tb = sys.exc_info()[2]
    tbinfo = traceback.format_tb(tb)[0]
    pymsg  = "PYTHON ERRORS:\n Traceback info:\n" + tbinfo + "Error info:\n" + str(sys.exc_info()[1])
    msg = "\nArcPy ERRORS:\n" + arcpy.GetMessages(2) + "\n"
    arcpy.AddError(pymsg)
    arcpy.AddError(msg)
    print pymsg
    print msg
    exit

finally:
    print("All Finished!")
    print "Finished at " + time.strftime("%c")