#!/usr/bin/env python
"""Creates points spaced such that Thiessen polygons will be hexagons.

ArcGIS Version:  10
Author:  Tim Whiteaker
Remarks:
    It's best if a projected coordinate system is used.

"""

import math
import os

import arcpy

def create_thiessen_points(study_area, side_length, output_fc):
    """Creates points spaced such that Thiessen polygons will be hexagons.

    Arguments:
        study_area -- feature class defining area of interest
        side_length -- length of regular hexagon side
        output_fc -- name and location of output feature class

    Remarks:
        Hexagons can be created for Thiessen polygons built from points spaced
        in a pattern like the one below.

        *   *   *   *
          *   *   *
        *   *   *   *
          *   *   *
        *   *   *   *

    """

    # Validate inputs
    count = int(str(arcpy.GetCount_management(study_area)))
    if count == 0:
        arcpy.AddError('Error: No features found in ' + str(study_area))
        return
    side_length = float(side_length)
    if side_length <= 0:
        arcpy.AddError('Error: Hexagon side length must be greater than zero.')
        return

    # Determine point spacing
    dx = 3.0 * side_length
    dy = side_length / 2.0 * math.sqrt(3.0)
    indent = dx / 2

    # Get the extent of the study area.
    # If in ArcMap, make sure we use feature coordinates, not map coordinates.
    desc = arcpy.Describe(study_area)
    if desc.dataType == "FeatureLayer":
        desc = arcpy.Describe(desc.featureClass.catalogPath)
    ext = desc.extent

    # Determine number of rows and columns.  Add extra just to be sure.
    xmin = ext.XMin - dx
    ymin = ext.YMin - dy * 3.0
    xmax = ext.XMax + dx
    ymax = ext.YMax + dy * 3.0
    num_rows = int((ymax - ymin) / dy) + 1
    num_cols = int((xmax - xmin) / dx) + 2

    # Create the output feature class
    spatial_ref = desc.spatialReference
    workspace = os.path.dirname(output_fc)
    fc_name = os.path.basename(output_fc)
    fc = arcpy.CreateFeatureclass_management(
        workspace, fc_name, "POINT", "", "", "", spatial_ref)

    # Populate output features
    arcpy.AddMessage('Creating ' + str(num_rows * num_cols) + ' points...')
    cursor = arcpy.InsertCursor(output_fc)
    feature = None

    try:
        y = ymin
        for r in range(num_rows):
            x = xmin - indent / 2
            if r % 2 != 0:
                x += indent

            for c in range(num_cols):
                feature = cursor.newRow()
                p = arcpy.Point()
                p.X = x
                p.Y = y
                feature.shape = p
                cursor.insertRow(feature)
                x += dx

            y += dy

    finally:
        if feature:
            del feature
        if cursor:
            del cursor


if __name__ == '__main__':
    is_test = False

    if is_test:
        raise Exception(' Testing not yet implemented')
    else:
        study_area = arcpy.GetParameterAsText(0)
        side_length = arcpy.GetParameterAsText(1)
        side_unit = arcpy.GetParameterAsText(2)

        final_fc = arcpy.GetParameterAsText(3)
        clipData = arcpy.GetParameterAsText(4)
        projected_data = os.path.join(os.path.split(final_fc)[0], "Proj_Thiessen")
        tempWS = arcpy.GetParameterAsText(5)
        output_fc = os.path.join(tempWS, "Temp_Thiessen_Points")
        intermediate_fc = os.path.join(tempWS,"Temp_Thiessen_Polygons")
        feature_layer = "in_mempory\Thiessen_layer"


        geo = arcpy.SpatialReference("WGS 1984")
        mercator = arcpy.SpatialReference("WGS 1984 World Mercator")


        if side_unit == "Geographic Lat Long":
            arcpy.Project_management(study_area, projected_data, geo)
        elif side_unit == "Meters":
            arcpy.Project_management(study_area, projected_data, mercator)

        create_thiessen_points(projected_data, side_length, output_fc)
        arcpy.CreateThiessenPolygons_analysis(output_fc, intermediate_fc)

        if clipData == True:
            arcpy.MakeFeatureLayer_management(intermediate_fc, feature_layer)
            arcpy.SelectLayerByLocation_management(feature_layer, "INTERSECT", study_area)

            matchcount = int(arcpy.GetCount_management(feature_layer).getOutput(0))

            if matchcount == 0:
                print("No features were matched...")
                arcpy.AddMessage("No features were matched...")

            else:
                arcpy.CopyFeatures_management(feature_layer, final_fc)
                print "Finished processing"
                arcpy.AddMessage("Finished Processing")

        if clipData == False:
            arcpy.CopyFeatures_management(intermediate_fc, final_fc)