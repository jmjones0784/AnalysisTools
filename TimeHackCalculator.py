import arcpy, sys, traceback, time

inputFC = arcpy.GetParameterAsText(0)
speed = arcpy.GetParameterAsText(1)
units = arcpy.GetParameterAsText(2)
fieldType = "FLOAT"

mphDict = {"5":"133.3", "10":"266.7", "15":"400.0", "20":"533.3", "25":"666.7", "30":"800", "35":"933.3", "40":"1066.7", "45":"1200", "50":"1333.3", "55":"1466.7", "60":"1600"}
kphDict = {"5":'80', '10':'186.7', '15':'240', '20':'346.7', '25':'426.7', '30':'506.7', '35':'586.7', '40':'668.7', '45':'746.7', '50':'853.3', '55':'906.7', '60':'1013.3'}

def exitScript():
    tb = sys.exc_info()[2]
    tbinfo = traceback.format_tb(tb)[0]
    pymsg  = "PYTHON ERRORS:\n Traceback info:\n" + tbinfo + "Error info:\n" + str(sys.exc_info()[1])
    msg = "\nArcPy ERRORS:\n" + arcpy.GetMessages(2) + "\n"
    arcpy.AddError(pymsg)
    arcpy.AddError(msg)
    print pymsg
    print msg
    exit

try:
    print("STARING SYNC AT " + time.strftime("%c"))
    arcpy.AddMessage("STARING SYNC AT " + time.strftime("%c"))

    if units == 'MPH':

        distance = mphDict[speed]

        fieldName = "Time_" + str(speed) + "mph"

        expression = "[Shape_Length] /" + distance

        arcpy.AddField_management(inputFC, fieldName, fieldType)

        arcpy.CalculateField_management(inputFC, fieldName, expression)

    elif units == 'KPH':

        distance = kphDict[speed]

        fieldName = "Time_" + str(speed) + "kph"

        expression = "[Shape_Length] /" + distance

        arcpy.AddField_management(inputFC, fieldName, fieldType)

        arcpy.CalculateField_management(inputFC, fieldName, expression)

except:
    exitScript()

finally:
    print("Successfully added " + fieldName + " at " + time.strftime("%c"))
    arcpy.AddMessage("Successfully added " + fieldName + " at " + time.strftime("%c"))