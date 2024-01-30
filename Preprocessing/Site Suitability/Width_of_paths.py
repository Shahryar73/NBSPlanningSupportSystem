import arcpy
import os
from arcpy.sa import *
arcpy.CheckOutExtension("3D")
arcpy.CheckOutExtension("Spatial")

# Neighbourhood_dir= "define a directory"
# BGT=r"Indicate the path to the BGT file"
site_type_field="NBS_new"
verges='berm'
sidewalk='voetpad'


#Select the transport corridors (sidewalks and verges)
arcpy.MakeFeatureLayer_management(BGT, "BGT")
arcpy.SelectLayerByAttribute_management(in_layer_or_view="BGT", selection_type="NEW_SELECTION",where_clause=""" {} = {} OR {} = {} """.format(site_type_field,verges,site_type_field,sidewalk))
os.makedirs(Neighbourhood_dir+r"\Width"+r"\BGT")
BGT_vector=Neighbourhood_dir+r"\Width"+r"\BGT"
arcpy.FeatureClassToFeatureClass_conversion("BGT", BGT_vector, "BGT")
BGT_vector_path = os.path.join(BGT_vector, "BGT.shp")

#Dissolve the polygons
os.makedirs(Neighbourhood_dir + r"\Width" +r"\BGT"+r"Dissolved")
BGT_dissoved=os.path.join(Neighbourhood_dir + r"\Width" +r"\BGT"+r"Dissolved","dissolved.shp")
arcpy.Dissolve_management(in_features=BGT_vector_path,out_feature_class=BGT_dissoved,
                          dissolve_field="", statistics_fields="", multi_part="MULTI_PART",
                          unsplit_lines="DISSOLVE_LINES")

# Make lines from the polygons
os.makedirs(Neighbourhood_dir + r"\Width" + r"\line")
BGT_line = os.path.join(Neighbourhood_dir + r"\Width" + r"\line","line.shp")
arcpy.PolygonToLine_management(in_features=BGT_dissoved,out_feature_class=BGT_line,neighbor_option="IDENTIFY_NEIGHBORS")

# Generate points along the line each 1 meter
os.makedirs(Neighbourhood_dir + r"\Width" + r"\Points")
BGT_point = os.path.join(Neighbourhood_dir + r"\Width" + r"\Points", "points.shp")
arcpy.GeneratePointsAlongLines_management(Input_Features=BGT_line,Output_Feature_Class=BGT_point,Point_Placement="DISTANCE", Distance="1 Meters", Percentage="",Include_End_Points="")
# Generate Thiessen polyons from the points
os.makedirs(Neighbourhood_dir + r"\Width" + r"\Tissen")
Tissen = os.path.join(Neighbourhood_dir + r"\Width" + r"\Tissen", "Tissen.shp")
arcpy.CreateThiessenPolygons_analysis(in_features=BGT_point,out_feature_class=Tissen,fields_to_copy="ONLY_FID")

#Cliped the tissen polygon with boundries of the city
Tissen_clip=os.path.join(Neighbourhood_dir + r"\Width" + r"\Tissen", "Tiss_c.shp")
arcpy.Clip_analysis(in_features=Tissen, clip_features=BGT_vector_path,out_feature_class=Tissen_clip,cluster_tolerance="")
# Calculate the area of polygons
arcpy.AddField_management(in_table=Tissen_clip, field_name="Area", field_type="DOUBLE", field_precision="",field_scale="", field_length="", field_alias="", field_is_nullable="NULLABLE",field_is_required="NON_REQUIRED", field_domain="")
arcpy.CalculateField_management(in_table=Tissen_clip, field="Area", expression='"!shape.area@squaremeters!"',expression_type="PYTHON_9.3", code_block="")
os.makedirs(Neighbourhood_dir + r"\Width" + r"\Tissen"+r"\Tiss_BGT_join")

# Join the function field with the area field in Tissen polygons
Tissen_BGT=os.path.join(Neighbourhood_dir + r"\Width" + r"\Tissen"+r"\Tiss_BGT_join","Tiss_join.shp")
arcpy.SpatialJoin_analysis(target_features=Tissen_clip, join_features=BGT_vector_path,out_feature_class=Tissen_BGT)
arcpy.AddField_management(in_table=Tissen_BGT, field_name="width", field_type="DOUBLE", field_precision="",field_scale="", field_length="", field_alias="", field_is_nullable="NULLABLE",field_is_required="NON_REQUIRED", field_domain="")

# Make a boolean raster from the areas considering the type of surface
with arcpy.da.UpdateCursor(Tissen_BGT,["Area","NBS_new","width"]) as wides:
    for wide in wides:
        if wide[1]==verges and float(wide[0]) > 0.5:
            wide[2]=1
        elif wide[1] == sidewalk and float(wide[0]) > 2.5:
            wide[2] = 1
        else:
            wide[2]=0
        wides.updateRow(wide)

# Make a raster from the polygon
os.makedirs(Neighbourhood_dir+r"\Width"+r"\output")
NBS_width=os.path.join(Neighbourhood_dir+r"\Width"+r"\output","widt.tif")
arcpy.PolygonToRaster_conversion(in_features=Tissen_BGT, value_field="width", out_rasterdataset=NBS_width,cell_assignment="CELL_CENTER", priority_field="NONE", cellsize="1")
NBS_width_expanded=os.path.join(Neighbourhood_dir+r"\Width"+r"\output","widt_expnd.tif")
arcpy.gp.Expand_sa(NBS_width, NBS_width_expanded, "2", "1")
os.makedirs(Neighbourhood_dir + r"\Width" + r"\output" +r"\True")
NBS_width_true = os.path.join(Neighbourhood_dir + r"\Width" + r"\output" +r"\True", "NBS_wide.tif")
arcpy.gp.Reclassify_sa(NBS_width_expanded, "Value", "0 0;1 1;NODATA 1", NBS_width_true, "DATA")
