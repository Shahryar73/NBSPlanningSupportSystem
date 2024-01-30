import arcpy
import os
from utils import add_field,integer_from_string_fields,slope_reclass_dict,GW_reclass_dict,BGT_NBS_dict
arcpy.CheckOutExtension("3D")
arcpy.CheckOutExtension("Spatial")

Neighbourhood_dir=arcpy.GetParameterAsText(0)
slope_path=Neighbourhood_dir + r"\slope" + r"\slope.tif"
storm_path=Neighbourhood_dir + r"\storm" + r"\storm.tif"
PET_path=Neighbourhood_dir +r"\PET"  r"\pet.tif"
roof_UHI=Neighbourhood_dir + r"\Roof" + r"\UHI" + r"\reclassified" + r"\UHI_nrm.tif"
ownership_path=Neighbourhood_dir + r"\ownership"  r"\ownership.tif"
landuse_path=Neighbourhood_dir + r"\landuse"  r"\landuse.tif"
groundwater_path=Neighbourhood_dir + r"\groundwater"  r"\groundwater.tif"
Selected_site=Neighbourhood_dir + r"\CostEstimation" + r"\CostEst.shp"
categorical_indicators=['ownership','landuse']

# type of site 0: land surface, 1:building, 2:both
type_of_site=2

#PARAMETERS
indicator_dict={'slope':slope_path,'storm':storm_path,'PET':PET_path,'ownership':ownership_path,'GW':groundwater_path,'landuse':landuse_path,'roof_uhi':roof_UHI}
on_building_nbs=['Intensive_greenroof','Extensive_greenroof']



NBS_list=['RainGarden','BioSwale','Intensive_greenroof','Extensive_greenroof','Tree','permeable_pavement','DetentionPond','RetentionPond']

storm_coefficients={'RainGarden':0.8,'BioSwale':0.6,'permeable_pavement':0.8,'DetentionPond':1,'Tree':0.3,'RetentionPond':1}

heat_coef = {'RainGarden': 0.5, 'BioSwale': 0.5, 'permeable_pavement': 0.5, 'DetentionPond': 0.4, 'Tree': 1,
             'RetentionPond': 0.4,'Extensive_greenroof':0.4,'Intensive_greenroof':0.8}

# 0:private, 1:Public
NBS_owner={'RainGarden':{'0':10,'1':10},'BioSwale':{'0':10,'1':10},'Intensive_greenroof':{'0':10,'1':10}
              ,'Extensive_greenroof':{'0':10,'1':10},'Tree':{'0':10,'1':10},'permeable_pavement':{'0':10,'1':10},'DetentionPond':{'0':10,'1':10}
    ,'RetentionPond':{'0':10,'1':10}}


Cost_dict={'tree':{'implementation': 570, 'maintenance':17},
           'extensive_greenroof':{'implementation': 50, 'maintenance':1.5},
           'intensive_greenroof':{'implementation': 120, 'maintenance':6},
           'raingarden':{'implementation': 60, 'maintenance':0.5},
           'permeable_pavement':{'implementation': 100, 'maintenance':0.47},
           'detention_basin':{'implementation': 65, 'maintenance':3},
           'swale':{'implementation': 50, 'maintenance':0.5},
                   }





"""
In this step the characteristics of the intervention area will be identified using the the data in the neighbourhood folder.
For each indicator(slope, ownership, etc. a field will be added to the intervention area layer)
"""


os.makedirs(Neighbourhood_dir + r"\CostEstimation" + r"\Table")
arcpy.CreateFileGDB_management(Neighbourhood_dir + r"\CostEstimation" + r"\Table", "nbs.gdb")
zonal_tables=Neighbourhood_dir+r"\CostEstimation"+r"\Table"+r"\nbs.gdb"+ r"\interv"


#Make a dictionary including the name of landuses and the assigned value to it
BGT_field_names=[]

indicator_value={}

for i,v in indicator_dict.items():
    indicator_value[i]=[]
    zonal_tables = Neighbourhood_dir + r"\CostEstimation" + r"\Table" + r"\nbs.gdb" + r"\{}".format(i)
    if i in categorical_indicators:
        zonal_type="MAJORITY"
    else:
        zonal_type = "MEAN"
    arcpy.gp.ZonalStatisticsAsTable_sa(Selected_site, "FID", v, zonal_tables, "DATA",zonal_type)
    arcpy.AlterField_management(in_table=zonal_tables, field=zonal_type, new_field_name=i, new_field_alias="")
    arcpy.JoinField_management(in_data=Selected_site, in_field="FID", join_table=zonal_tables, join_field="FID", fields=i)
    with arcpy.da.SearchCursor(Selected_site,["FID",i]) as values:
        for value in values:
            indicator_value[i].append({'{}'.format(value[0]):value[1]})






"""
In this step the suitability score of all NBS will be calculated for the intervention area using the assigned characteristics
"""



NBS_fields=[]
# indicators_fields=indicators_non_bgt + indicators_bgt

def reclass_slope(nbs,slope_field,slope_reclass_dict=slope_reclass_dict):
    for i in slope_reclass_dict[nbs]:
        if slope_field >= i[0] and slope_field< i[1]:
            return i[2]



def reclass_coeff(nbs,value,coeff_dict):
    return value * coeff_dict[nbs]

def reclass_BGT(nbs,value,bgt_nbs_dict,name='landuse'):
    field_dict = integer_from_string_fields(indicator_dict[name])
    for k,v in field_dict.items():
        if v==value:
            return bgt_nbs_dict[nbs][k]
        else:
            pass


def reclass_owner(nbs,value,NBS_owner=NBS_owner):
    return NBS_owner[nbs][str(value)]



for nbs in NBS_list:
    nbs_field="{}_su".format(nbs[:4])
    add_field(Selected_site,nbs_field)
    with arcpy.da.UpdateCursor(Selected_site,['FID',nbs_field,'slope','storm','PET','ownership','GW','landuse','roof_uhi']) as fies:
        for fi in fies:
            if type_of_site==2 or type_of_site==1 :
                if nbs in on_building_nbs:
                    slope_value = reclass_slope(nbs, fi[2])
                    PET_value = reclass_coeff(nbs, fi[8], coeff_dict=heat_coef)
                    ownership_value = reclass_owner(nbs, fi[5])
                    impact=PET_value/2
                    effort=(slope_value +ownership_value)/4
            if type_of_site==2 or type_of_site==0:
                if nbs not in on_building_nbs:
                    slope_value = reclass_slope(nbs,fi[2])
                    storm_value = reclass_coeff(nbs, fi[3],coeff_dict=storm_coefficients)
                    PET_value = reclass_coeff(nbs, fi[4],coeff_dict=heat_coef)
                    ownership_value = reclass_owner(nbs,fi[5])
                    GW_value = reclass_slope(nbs,fi[6],slope_reclass_dict=GW_reclass_dict)
                    BGT_value = reclass_BGT(nbs, fi[7], BGT_NBS_dict)
                    impact=(storm_value+PET_value)/4
                    effort=(slope_value + ownership_value + BGT_value + GW_value)/8
            fi[1]=impact + effort
            fies.updateRow(fi)





"""
In this step the cost of implementation and maintanance of the intervention area will be estimated
"""



Fields_name=[]
area_field="Area"
add_field(Selected_site,area_field)
arcpy.CalculateField_management(in_table=Selected_site, field=area_field, expression='"!shape.area@squaremeters!"', expression_type="PYTHON_9.3", code_block="")
for NBS in Cost_dict.keys():
    add_field(Selected_site,NBS[:3] + "_imco")
    add_field(Selected_site,NBS[:3] + "_maco")

    if NBS=='tree':
        # Calculating the number of trees possible to implement
        os.makedirs(Neighbourhood_dir + r"\CostEstimation"+r"\polyline")
        polyline=os.path.join(Neighbourhood_dir + r"\CostEstimation"+r"\polyline","polyline.shp")
        arcpy.FeatureToLine_management(in_features=Selected_site,
                                       out_feature_class=polyline,
                                       cluster_tolerance="", attributes="ATTRIBUTES")
        lines_shp=os.path.join(Neighbourhood_dir + r"\CostEstimation"+r"\polyline","line.shp")
        arcpy.SplitLine_management(in_features=polyline,
                                   out_feature_class=lines_shp)
        lengths=[]
        lines_Fields = arcpy.ListFields(lines_shp)
        field_name=[name.name for name in lines_Fields]
        add_field(lines_shp,'length')
        arcpy.CalculateField_management(in_table=lines_shp, field="length", expression='"!shape.length@meters!"',
                                        expression_type="PYTHON_9.3", code_block="")
        with arcpy.da.SearchCursor(lines_shp,"length") as lines:
            for line in lines:
                lengths.append(line[0])
        max_length=max(lengths)
        #Each 7 meter there can be a tree
        number_of_trees=int(max_length/7)

    # Estimate the costs
    with arcpy.da.UpdateCursor(Selected_site, [area_field,NBS[:3] + "_imco",NBS[:3] + "_maco"]) as rows:
        for row in rows:
            if NBS=='tree':
                row[1] = number_of_trees * Cost_dict[NBS]['implementation']
                row[2] = number_of_trees * Cost_dict[NBS]['maintenance']

            else:
                row[1] = row[0] * Cost_dict[NBS]['implementation']
                row[2] = row[0] * Cost_dict[NBS]['maintenance']
            rows.updateRow(row)











