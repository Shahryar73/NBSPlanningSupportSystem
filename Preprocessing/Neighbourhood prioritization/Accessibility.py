import arcpy
import os
from arcpy import env
arcpy.CheckOutExtension("Network")


Folder=arcpy.GetParameterAsText(1)
# Population point data
incident=arcpy.GetParameterAsText(2)
# The name of the field with the number of population
population_field=arcpy.GetParameterAsText(3)
#Specify the access points for green spaces
Facilities=arcpy.GetParameterAsText(4)
city=arcpy.GetParameterAsText(5)
#specify name of the field that the is unique for each neighborhood
unique_zonecode=arcpy.GetParameterAsText(6)
#Specify the folder where the data generated through the analysis can be stored in
zones=arcpy.GetParameterAsText(7)
# The network file should be generated in ArcGIS for walking mode
network=arcpy.GetParameterAsText(8)


#Find the closets faclities and calculate the walking travel time
output=os.path.join(Folder,'closest.gdb')
outRoutes="Routes"
outDirection="Direction"
outClosestfacility="ClosestFacilities"
measurement_units = "Minutes"

arcpy.na.FindClosestFacilities(incident, Facilities, measurement_units,
                                    network, output, outRoutes,
                                    outDirection, outClosestfacility,
                                    Number_of_Facilities_to_Find=1)

##########################
# Add the travel time information to the population points
route=os.path.join(output,'Routes')
diction={}
with arcpy.da.SearchCursor(route,["IncidentOID","Total_Minutes"]) as rows:
    for row in rows:
        diction[row[0]]=row[1]

arcpy.AddField_management(in_table=incident, field_name="travel_tim", field_type='DOUBLE', field_precision="", field_scale="", field_length="", field_alias="", field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")
for key in diction:
    with arcpy.da.UpdateCursor(incident,["FID","travel_tim"]) as times:
        for time in times:
            if int(key)==int(time[0]):
                time[1]=diction[key]
            times.updateRow(time)

###############
# Generate the zones (Separate neighbourhoods)
arcpy.MakeFeatureLayer_management(city,unique_zonecode)
list=[]
with arcpy.da.SearchCursor(city,[unique_zonecode]) as rows:
    for row in rows:
        list.append(row[0])
    for i in list:
        arcpy.SelectLayerByAttribute_management('neighbour',"NEW_SELECTION",""" "{}" = {} """.format(unique_zonecode,str(i)))
        arcpy.FeatureClassToFeatureClass_conversion('neighbour',zones,"{}".format(str(i)))


#################################
#Seperate the points located at each zone
zones=r"C:\Users\20184183\surfdrive\NBSplanningsupportsystem\Biodiversity\biodiversity\buurten"
zone_point=r"C:\Users\20184183\surfdrive\NBSplanningsupportsystem\Access\Python_project\Points_postcode6\Point_per_zone"

arcpy.MakeFeatureLayer_management(incident, 'time')
for i in os.listdir(zones):
    if i.endswith("shp"):
        arcpy.SelectLayerByLocation_management("time", "intersect", os.path.join(zones, i))
        arcpy.FeatureClassToFeatureClass_conversion('time', zone_point,
                                                    'zone_{}'.format(i.split("_")[1].split(".")[0]))



#####################

#Calculate the total number of population with travel time more than 10 minutes in each neighbourhood
buurt_pop10={}
for i in os.listdir(zone_point):
    if i.endswith("shp"):
        with arcpy.da.SearchCursor(os.path.join(zone_point,i),["travel_tim",population_field]) as tra_bols:
            pop10=0
            for bol in tra_bols:
                if bol[0] >=10:
                    pop10 += int(bol[1])
            buurt_pop10[i.split("_")[1].split(".")[0]]=pop10

arcpy.AddField_management(in_table=city, field_name="pop_tra_10", field_type='DOUBLE', field_precision="", field_scale="", field_length="", field_alias="", field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")
with arcpy.da.UpdateCursor(city, ["FID", "pop_tra_10"]) as st:
    for s in st:
        for b,p in buurt_pop10.items():
            if int(s[0]) == int(int(b) -1):
                s[1] = int(p)
                st.updateRow(s)

