import arcpy, time, re, os, traceback

sourceFD = r''

try:
    for dirpaths, dirnames, filenames in arcpy.da.Walk(sourceFD):
        for file in filenames:
            sFC = os.path.join(dirpaths, file)

            f = [f.name for f in arcpy.ListFields(sFC)]
            f.remove("OBJECTID")
            if "Shape" in f:
                f.remove("Shape")
            if "SHAPE" in f:
                f.remove("SHAPE")
            if "SHAPE_Area" in f:
                f.remove(u'SHAPE_Area')
            if "SHAPE_Length" in f:
                f.remove(u'SHAPE_Length')
            if "Shape_Area" in f:
                f.remove(u'Shape_Area')
            if "Shape_Length" in f:
                f.remove(u'Shape_Length')
            else:
                print("Shape field not in list...")

            if len(f) > 0:
                print("Deleting fields from " + file)
                arcpy.DeleteField_management(sFC, f)
            else:
                print("File already cleaned...")

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