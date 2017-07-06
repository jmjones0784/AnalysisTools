import arcpy, time, re, os, traceback


##gdb = r''
##inFC = os.path.join(gdb, "")
inFC = r''
outPath = r''

type  = []


try:
    field = [u'RptGroup']
    with arcpy.da.SearchCursor(inFC, field) as scursor:
        for row in scursor:
            items = row[0].split("/")
            if items not in type:
                type.append(items)

    del scursor

    for t in type:
        expression = "RptGroup LIKE '%" + t[0] + "%'"
        tempWS = r"in_memory"
        fc = t[0] + "_H"
        gFC = arcpy.ValidateTableName(fc, tempWS)
        tempFC = os.path.join(tempWS, gFC)
        outFC = os.path.join(outPath, gFC)
        print expression, gFC

        if arcpy.Exists(outFC) == False:
            print("Selecting Data")

            arcpy.CreateFeatureclass_management(tempWS, gFC, "MULTIPOINT", inFC, "DISABLED", "DISABLED", inFC)
            f = [u'OBJECTID', u'Shape', u'MsgSerial', u'RptGroup']
            f1 = [u'OBJECTID', u'Shape', u'RptGroup']
            iCursor = arcpy.da.InsertCursor(tempFC, f1)
            with arcpy.da.SearchCursor(inFC, f1, expression) as cursor:
                for row in cursor:
                    iCursor.insertRow(row)

            del cursor, iCursor

            result = arcpy.GetCount_management(tempFC)
            count = int(result.getOutput(0))
            if count > 0:
                arcpy.CopyFeatures_management(tempFC, outFC)
                print("Successfully selected " + gFC)
            else:
                print("No Features Selected")

except:
    print("Uh oh!")
    print("Error at " + time.strftime("%c"))

    tb = sys.exc_info()[2]
    tbinfo = traceback.format_tb(tb)[0]
    pymsg  = "PYTHON ERRORS:\n Traceback info:\n" + tbinfo + "Error info:\n" + str(sys.exc_info()[1])
    msg = "\nArcPy ERRORS:\n" + arcpy.GetMessages(2) + "\n"
    print pymsg
    print msg
    exit

finally:
    print("All Finished!")
    print "Finished at " + time.strftime("%c")