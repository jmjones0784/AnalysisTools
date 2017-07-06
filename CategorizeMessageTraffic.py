import arcpy, datetime, re

source = r''
f = [f.name for f in arcpy.ListFields(source)]

try:
    ##rType = 'HARC'
    rType = 'Message Traffic'
    addField = True

    print("Updating Feature Class")

    lCount = 0
    rCount = 0
    wCount = 0
    cCount = 0
    tCount = 0
    pCount = 0
    hCount = 0
    eCount = 0
    mCount = 0
    pCount = 0

    if addField == True:
        print("Adding Field")
        arcpy.AddField_management(source, 'RptGroup', "TEXT", "", "",  255, "Report Group")

    if rType == 'HARC':
        fields = [u'Report', u'RptGroup']
    elif rType == 'Message Traffic':
        fields = [u'TxtSnippet', u'RptGroup']

    print("Categorizing Reporting")
    with arcpy.da.UpdateCursor(source, fields) as cursor:
        for row in cursor:
            iRow = []
            if re.search("Amir", row[0]) or re.search("Leader", row[0]) or re.search("leader", row[0]) or re.search("amir", row[0]) or re.search("Leadership", row[0]) or re.search("commander", row[0]) or re.search("Commander", row[0]):
                if "Leader" not in iRow:
                    if len(iRow) == 0:
                        iRow.append("Leader")
                        lCount +=1
                    else:
                        iRow.append("/Leader")
                        lCount +=1
            if re.search("recruit", row[0]) or re.search("recruitment", row[0]) or re.search("Recruitment", row[0]) or re.search("Recruiting", row[0]):
                if "Recruitment" not in iRow:
                    if len(iRow) == 0:
                        iRow.append("Recruitment")
                        rCount +=1
                    else:
                        iRow.append("/Recruitment")
                        rCount +=1
            if re.search("chemical", row[0]) or re.search("Chemical", row[0]):
                if "Chemical Weapons" not in iRow:
                    if len(iRow) == 0:
                        iRow.append("Chemical Weapons")
                        cCount +=1
                    else:
                        iRow.append("/Chemical Weapons")
                        cCount +=1
            if re.search("weapons", row[0]) or re.search("missile", row[0]) or re.search("artillery", row[0]) or re.search("VBIED", row[0]) or re.search("IED", row[0]):
                if "Chemical" or "chemical" not in row[0]:
                    if 'Weapons' not in iRow:
                        if len(iRow) == 0:
                            iRow.append("Weapons")
                            wCount +=1
                        else:
                            iRow.append("/Weapons")
                            wCount +=1
            if re.search("camp", row[0]) or re.search("Camp", row[0]) or re.search("Staging", row[0]):
                if 'Camps' not in iRow:
                    if len(iRow) == 0:
                        iRow.append("Camps")
                        tCount +=1
                    else:
                        iRow.append("/Camps")
                        tCount +=1
            if re.search("Hisbah", row[0]) or re.search("Shariah", row[0]):
                if 'Law Enforcement' not in iRow:
                    if len(iRow) == 0:
                        iRow.append("Law Enforcement")
                        hCount += 1
                    else:
                        iRow.append("/Law Enforcement")
                        hCount += 1
            if re.search("GSB", row[0]) or re.search("Amniyah", row[0]):
                if "Internal\External Security" not in iRow:
                    if len(iRow) == 0:
                        iRow.append("Internal\External Security")
                        eCount += 1
                    else:
                        iRow.append("/Internal\External Security")
                        eCount += 1
            if re.search("finance", row[0]) or re.search("financial", row[0]) or re.search("hawala", row[0]) or re.search("financier", row[0]) or re.search("money", row[0]) or re.search("Financial", row[0]) or re.search("Finance", row[0]):
                if "Finance" not in iRow:
                    if len(iRow) == 0:
                        iRow.append("Finance")
                        mCount +=1
                    else:
                        iRow.append("/Finance")
                        mCount +=1
            if re.search("media", row[0]) or re.search("Media", row[0]):
                if "Media" not in iRow:
                    if len(iRow) == 0:
                        iRow.append("Media")
                        pCount +=1
                    else:
                        iRow.append("/Media")
                        pCount +=1

            if len(iRow) == 0:
                aRow = ["Presence"]
                pCount +=1
            elif len(iRow) == 1:
                aRow = [iRow[0]]
            else:
                l = len(iRow) - 1
                aRow = [''.join(iRow[0:l])]

            print aRow

            row[1] = aRow[0]
            cursor.updateRow(row)

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