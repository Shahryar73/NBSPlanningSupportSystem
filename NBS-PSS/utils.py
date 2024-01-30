import arcpy
import os
from arcpy.sa import *
arcpy.CheckOutExtension("3D")
arcpy.CheckOutExtension("Spatial")


#########################################
#PARAMETHERS

BGT_NBS_dict={'RainGarden':{"begroeidterreindeel": 10,"functioneelgebied": 0,"gebouwinstallatie":0,"kunstwerkdeel": 3,"onbegroeidterreindeel": 5,"ondersteunendwaterdeel": 0,"berm": 6,"verkeerseiland": 6,"overburggingsdeel": 0,"overigbouwwerk": 0,"overigescheiding": 0,' ': 0,"Bouwterrein": 0,"Park en plantsoen": 7,"Woongebied": 0,"Bedrijfsterrein": 0,"Openbare voorziening": 0,"Vliegveld": 0,"Sportterrein": 0,"Hoofdweg": 0,"Sociaal-culturele voorziening": 0,"Detailhandel en horeca": 0,"Begraafplaats": 8,"Volkstuin": 9,"Dagrecreatief terrein": 7,"Spoorweg": 0,"scheiding": 0,"tunneldeel": 0,"vegetatieobject": 8,"waterdeel": 0,"rijbaan lokale weg": 0,"baan voor vliegverkeer": 0,"voetpad": 2,"voetpad area": 5,"inrit": 0,"parkeervlak": 7,"voetpad op trap": 0,"fietspad": 0,"rijbaan regionale weg": 0,"OV-baan": 0,"voetgangersgebied": 8,"rijbaan autosnelweg": 0,"rijbaan autoweg": 0,"woonerf": 0,"spoorbaan":0,"overweg": 0,"berm gr":5},
              'BioSwale':{"begroeidterreindeel": 4,"functioneelgebied": 0,"gebouwinstallatie":0,"kunstwerkdeel": 3,"onbegroeidterreindeel": 0,"ondersteunendwaterdeel": 0,"berm": 9,"verkeerseiland": 8,"overburggingsdeel": 0,"overigbouwwerk": 0,"overigescheiding": 0,' ': 0,"Bouwterrein": 0,"Park en plantsoen": 9,"Woongebied": 0,"Bedrijfsterrein": 0,"Openbare voorziening": 0,"Vliegveld": 0,"Sportterrein": 0,"Hoofdweg": 0,"Sociaal-culturele voorziening": 0,"Detailhandel en horeca": 0,"Begraafplaats": 4,"Volkstuin": 9,"Dagrecreatief terrein": 9,"Spoorweg": 0,"scheiding": 0,"tunneldeel": 0,"vegetatieobject": 8,"waterdeel": 0,"rijbaan lokale weg": 0,"baan voor vliegverkeer": 0,"voetpad": 2,"voetpad area": 3 ,"inrit": 0,"parkeervlak": 9,"voetpad op trap": 0,"fietspad": 0,"rijbaan regionale weg": 0,"OV-baan": 0,"voetgangersgebied": 6,"rijbaan autosnelweg": 0,"rijbaan autoweg": 0,"woonerf": 0,"spoorbaan":0,"overweg": 0,"berm gr":9},
              'Tree':{"begroeidterreindeel": 7,"functioneelgebied": 0,"gebouwinstallatie":0,"kunstwerkdeel": 1,"onbegroeidterreindeel": 0,"ondersteunendwaterdeel": 0,"berm": 9,"verkeerseiland": 4,"overburggingsdeel": 0,"overigbouwwerk": 0,"overigescheiding": 0,' ': 0,"Bouwterrein": 0,"Park en plantsoen": 9,"Woongebied": 0,"Bedrijfsterrein": 0,"Openbare voorziening": 0,"Vliegveld": 0,"Sportterrein": 0,"Hoofdweg": 0,"Sociaal-culturele voorziening": 0,"Detailhandel en horeca": 0,"Begraafplaats": 8,"Volkstuin": 5,"Dagrecreatief terrein": 7,"Spoorweg": 0,"scheiding": 0,"tunneldeel": 0,"vegetatieobject": 8,"waterdeel": 0,"rijbaan lokale weg": 0,"baan voor vliegverkeer": 0,"voetpad": 8,"voetpad area": 6,"inrit": 0,"parkeervlak": 9,"voetpad op trap": 0,"fietspad": 0,"rijbaan regionale weg": 0,"OV-baan": 0,"voetgangersgebied": 0,"rijbaan autosnelweg": 0,"rijbaan autoweg": 0,"woonerf": 0,"spoorbaan":0,"overweg": 0,"berm gr":6},
              'permeable_pavement':{"begroeidterreindeel": 6,"functioneelgebied": 0,"gebouwinstallatie":0,"kunstwerkdeel": 1,"onbegroeidterreindeel": 0,"ondersteunendwaterdeel": 0,"berm": 8,"verkeerseiland": 8,"overburggingsdeel": 0,"overigbouwwerk": 0,"overigescheiding": 0,' ': 0,"Bouwterrein": 0,"Park en plantsoen": 6,"Woongebied": 0,"Bedrijfsterrein": 0,"Openbare voorziening": 0,"Vliegveld": 0,"Sportterrein": 3,"Hoofdweg": 0,"Sociaal-culturele voorziening": 4,"Detailhandel en horeca": 2,"Begraafplaats": 3,"Volkstuin": 4,"Dagrecreatief terrein": 4,"Spoorweg": 0,"scheiding": 0,"tunneldeel": 0,"vegetatieobject": 4,"waterdeel": 0,"rijbaan lokale weg": 0,"baan voor vliegverkeer": 0,"voetpad": 3,"voetpad area": 2 ,"inrit": 0,"parkeervlak": 5,"voetpad op trap": 0,"fietspad": 0,"rijbaan regionale weg": 0,"OV-baan": 0,"voetgangersgebied": 0,"rijbaan autosnelweg": 0,"rijbaan autoweg": 0,"woonerf": 0,"spoorbaan":0,"overweg": 0,"berm gr":1},
              'DetentionPond':{"begroeidterreindeel": 5,"functioneelgebied": 0,"gebouwinstallatie":0,"kunstwerkdeel": 0,"onbegroeidterreindeel": 5,"ondersteunendwaterdeel": 0,"berm": 0,"verkeerseiland": 0,"overburggingsdeel": 0,"overigbouwwerk": 0,"overigescheiding": 0,' ': 0,"Bouwterrein": 0,"Park en plantsoen": 5,"Woongebied": 0,"Bedrijfsterrein": 0,"Openbare voorziening": 0,"Vliegveld": 0,"Sportterrein": 2,"Hoofdweg": 0,"Sociaal-culturele voorziening": 0,"Detailhandel en horeca": 0,"Begraafplaats": 3,"Volkstuin": 5,"Dagrecreatief terrein": 5,"Spoorweg": 0,"scheiding": 0,"tunneldeel": 0,"vegetatieobject": 0,"waterdeel": 0,"rijbaan lokale weg": 0,"baan voor vliegverkeer": 0,"voetpad": 0,"voetpad area": 0 ,"inrit": 0,"parkeervlak": 0,"voetpad op trap": 0,"fietspad": 0,"rijbaan regionale weg": 0,"OV-baan": 0,"voetgangersgebied": 0,"rijbaan autosnelweg": 0,"rijbaan autoweg": 0,"woonerf": 0,"spoorbaan":0,"overweg": 0,"berm gr":1},
              'RetentionPond':{"begroeidterreindeel": 0,"functioneelgebied": 0,"gebouwinstallatie":0,"kunstwerkdeel": 0,"onbegroeidterreindeel": 0,"ondersteunendwaterdeel": 0,"berm": 0,"verkeerseiland": 0,"overburggingsdeel": 0,"overigbouwwerk": 0,"overigescheiding": 0,' ': 0,"Bouwterrein": 0,"Park en plantsoen": 0,"Woongebied": 0,"Bedrijfsterrein": 0,"Openbare voorziening": 0,"Vliegveld": 0,"Sportterrein": 0,"Hoofdweg": 0,"Sociaal-culturele voorziening": 0,"Detailhandel en horeca": 0,"Begraafplaats": 0,"Volkstuin": 0,"Dagrecreatief terrein": 0,"Spoorweg": 0,"scheiding": 0,"tunneldeel": 0,"vegetatieobject": 0,"waterdeel": 10,"rijbaan lokale weg": 0,"baan voor vliegverkeer": 0,"voetpad": 0,"voetpad area": 0,"inrit": 0,"parkeervlak": 0,"voetpad op trap": 0,"fietspad": 0,"rijbaan regionale weg": 0,"OV-baan": 0,"voetgangersgebied": 0,"rijbaan autosnelweg": 0,"rijbaan autoweg": 0,"woonerf": 0,"spoorbaan":0,"overweg": 0,"berm gr":0}
              ,'Intensive_greenroof': {"Openbare voorziening": 10, ' ': 1, "Hoofdweg": 1, "Vliegveld": 1, "Bouwterrein": 5,
                              "Woongebied": 7, "Park en plantsoen": 1,
                              "Bedrijfsterrein": 8, "Sportterrein": 2, "Dagrecreatief terrein": 10,
                              "Sociaal-culturele voorziening": 8,
                              "Overig agrarisch gebruik": 6, "Detailhandel en horeca": 10, "Begraafplaats": 8,
                              "Volkstuin": 6, "Spoorweg": 6,
                              "Stortplaats": 5, "NODATA": 1},
                'Extensive_greenroof': {"Openbare voorziening": 10, ' ': 1, "Hoofdweg": 1, "Vliegveld": 1,
                                        "Bouwterrein": 5,
                                        "Woongebied": 7, "Park en plantsoen": 1,
                                        "Bedrijfsterrein": 8, "Sportterrein": 2, "Dagrecreatief terrein": 10,
                                        "Sociaal-culturele voorziening": 8,
                                        "Overig agrarisch gebruik": 6, "Detailhandel en horeca": 10, "Begraafplaats": 8,
                                        "Volkstuin": 6, "Spoorweg": 6,
                                        "Stortplaats": 5, "NODATA": 1}}


ownership_reclass_dict={'RainGarden':{'public':10,'private':8},
                'BioSwale':{'public':10,'private':5},
                'permeable_pavement':{'public':10,'private':8},
                'DetentionPond': {'public':10,'private':0},
                'RetentionPond':{'public':10,'private':0},
                'Tree':{'public':10,'private':5},
                'Intensive_greenroof':{'public':10,'private':6},
                'Extensive_greenroof':{'public':10,'private':8},
                           }



slope_reclass_dict={'RainGarden':[[0, 2, 10], [2, 5, 10], [5, 10, 6], [10, 15, 2], [15, 100, 0], ['NODATA', 0]],
                'BioSwale':[[0, 2, 9], [2, 5, 7], [5, 10, 3], [10, 15, 0], [15, 100, 0], ['NODATA', 0]],
                'permeable_pavement':[[0, 2, 9], [2, 5, 7], [5, 10, 3], [10, 15, 0], [15, 100, 0], ['NODATA', 0]],
                'DetentionPond':[[0, 5, 10], [5, 10, 10], [10, 15, 0], [15, 100, 0], ['NODATA', 0]],
                'RetentionPond':[[0, 5, 10], [5, 10, 10], [10, 15, 0], [15, 100, 0], ['NODATA', 0]],
                'Tree':[[0, 5, 10], [5, 10, 10], [10, 15, 0], [15, 100, 0], ['NODATA', 0]],
                    'Intensive_greenroof':[[0, 5, 10], [5, 10, 0], [10, 15, 0], [15, 100, 0], ['NODATA', 0]],
                   'Extensive_greenroof':[[0, 5, 10], [5, 10, 8], [10, 15, 6], [15, 35, 4],[35, 100, 0], ['NODATA', 0]]}



GW_reclass_dict={'RainGarden':[[-4.573300, 0.3, 0], [0.3, 0.6, 0], [0.6, 1.2, 3], [1.2, 1.8, 6], [1.8, 20, 10], ['NODATA', 0]],
                'BioSwale':[[-4.573300, 0.3, 4], [0.3, 0.6, 6], [0.6, 1.2, 8], [1.2, 1.8, 10], [1.8, 20, 10], ['NODATA', 0]],
                'permeable_pavement':[[-4.573300, 0.3, 0], [0.3, 0.6, 2], [0.6, 1.2, 6], [1.2, 1.8, 8], [1.8, 20, 10], ['NODATA', 0]],
                'DetentionPond':[[-4.573300, 0.3, 0], [0.3, 0.6, 5], [0.6, 1.2, 8], [1.2, 1.8, 10], [1.8, 20, 10], ['NODATA', 0]],
                'RetentionPond': [[-4.573300, 0.3, 0], [0.3, 0.6, 5], [0.6, 1.2, 8], [1.2, 1.8, 10], [1.8, 20, 10], ['NODATA', 0]],
                'Tree':[[-4.573300, 0.3, 0], [0.3, 0.6, 0], [0.6, 1.2, 6], [1.2, 1.8, 8], [1.8, 20, 10], ['NODATA', 0]]}



##################################################


def extract_shape(Neighbourhood_dir,sourcefile,fieldvalue,fieldname,outputname='boundary'):
    os.makedirs(Neighbourhood_dir + r"\{}".format(fieldvalue) + r"\{}".format(outputname) + r"\{}_org".format(outputname))
    shape_org_dir = Neighbourhood_dir + r"\{}".format(fieldvalue) + r"\{}".format(outputname) + r"\{}_org".format(outputname)
    arcpy.MakeFeatureLayer_management(sourcefile, "{}".format(str(fieldvalue)))
    arcpy.SelectLayerByAttribute_management(in_layer_or_view="{}".format(str(fieldvalue)),
                                            selection_type="NEW_SELECTION",
                                            where_clause=""" "{}"='{}' """.format(fieldname,
                                                                                  fieldvalue))
    arcpy.FeatureClassToFeatureClass_conversion("{}".format(str(fieldvalue)), shape_org_dir, "{}_org".format(outputname))
    return os.path.join(shape_org_dir,"{}_org.shp".format(outputname))

def buffer_around_shape(Neighbourhood_dir,fieldvalue,shape_org_dir,buffer=50,outputname='boundary'):
    os.makedirs(Neighbourhood_dir+r"\{}".format(fieldvalue)+r"\{}".format(outputname)+r"\{}_buffer".format(outputname))
    boundary_buf_dir=Neighbourhood_dir+r"\{}".format(fieldvalue)+r"\{}".format(outputname)+r"\{}_buffer".format(outputname)
    Boundary=os.path.join(boundary_buf_dir,"bound_buff_{}.shp".format(buffer))
    arcpy.Buffer_analysis(in_features=shape_org_dir, out_feature_class=Boundary, buffer_distance_or_field="{} Meters".format(buffer), line_side="FULL", line_end_type="ROUND", dissolve_option="ALL", dissolve_field="", method="PLANAR")
    return Boundary


def integer_from_string_fields(map,string_field="NBS_new",integer_field="Value"):

    field_dict={}
    fields = arcpy.SearchCursor(map,"","","{};{}".format(string_field,integer_field),"")
    for field in fields:
        S_field=field.getValue(string_field)
        I_value=field.getValue(integer_field)
        field_dict[S_field] = I_value
    return field_dict


def clip_vector(Neighbourhood_dir,file,boundry,name):
    os.makedirs(Neighbourhood_dir+r"\{}".format(name)+ r"\Vector")
    cliped=os.path.join(Neighbourhood_dir+r"\{}".format(name)+r"\Vector","{}_clip.shp".format(name[:4]))
    arcpy.Clip_analysis(file,boundry, cliped, "")
    return cliped



def vector_to_raster(file,Neighbourhood_dir,field,map_name):
    os.makedirs(Neighbourhood_dir + r"\{}".format(map_name) + r"\Raster")
    Ras = os.path.join(Neighbourhood_dir + r"\{}".format(map_name) + r"\Raster", "{}.tif".format(map_name))
    arcpy.PolygonToRaster_conversion(in_features=file, value_field=field, out_rasterdataset=Ras, cell_assignment="CELL_CENTER", priority_field="NONE", cellsize="1")
    return Ras

def clip_raster(Neighbourhood_dir,Boundary,map,map_name):
    os.makedirs(Neighbourhood_dir + r"\{}".format(map_name))
    Ras = Raster(map)
    msk = ExtractByMask(Ras, Boundary)
    cliped = os.path.join(Neighbourhood_dir + r"\{}".format(map_name), "{}.tif".format(map_name))
    msk.save(cliped)
    return cliped
def normalize(Neighbourhood_dir,map,map_name,scalefactor=10):
    os.makedirs(Neighbourhood_dir + r"\{}".format(map_name) + r"\reclassified")
    map_nrm = os.path.join(Neighbourhood_dir + r"\{}".format(map_name) + r"\reclassified", "{}_nrm.tif".format(map_name[:4]))
    map_ras = Raster(map)
    ras_nrm = ((map_ras - map_ras.minimum) / (map_ras.maximum - map_ras.minimum)) * scalefactor
    ras_nrm.save(map_nrm)
    return map_nrm

def challenge_reclassify(Neighbourhood_dir,challenge_map,challenge_name,NBS,coefficient_dict):
    os.makedirs(Neighbourhood_dir + r"\{}".format(challenge_name) + r"\reclassified" + r"\{}".format(NBS))
    challenge_nbs = os.path.join(Neighbourhood_dir + r"\{}".format(challenge_name) + r"\reclassified" + r"\{}".format(NBS), '{}.tif'.format(challenge_name))
    challenge = Raster(challenge_map) * coefficient_dict[NBS]
    challenge.save(challenge_nbs)
    return challenge_nbs


def exclude_raster_value(Neighbourhood_dir,map,map_name,exclude_value,field_dict):
    '''
    make a binary raster including only data of a specific value (e.g. roads, waterways..).
    Works for rasters with a string type field and a value. Suitable to be used on the outcome of the BGT_To_Raster function
    '''
    os.makedirs(Neighbourhood_dir + r"\{}".format(map_name) + r"\Raster")
    Ras= os.path.join(Neighbourhood_dir + r"\{}".format(map_name) + r"\Raster", "{}.tif".format(map_name))
    remap_list = []
    # field_dict = integer_from_string_fields(map)[0]
    field_names = field_dict.keys()
    for i in field_names:
        if exclude_value not in i:
            remap_list.append([field_dict[i], "NODATA"])
        else:
            remap_list.append([field_dict[i], 1])
    remap = RemapValue(remap_list)
    out = Reclassify(map, "Value", remap=remap)
    out.save(Ras)
    return Ras


def distance_to_object(Neighbourhood_dir,map,map_name="Roads"):
    os.makedirs(Neighbourhood_dir + r"\{}".format(map_name) + r"\Raster" + r"\euclidean")
    euclidean = os.path.join(Neighbourhood_dir + r"\{}".format(map_name) + r"\Raster" + r"\euclidean","{}_eucl.tif".format(map_name[:4]))
    arcpy.gp.EucDistance_sa(map, euclidean, "", "1", "")
    return euclidean



def range_reclass(Neighbourhood_dir,map,map_name,NBS,reclass_dict):
    os.makedirs(Neighbourhood_dir + r"\{}".format(map_name) + r"\{}".format(NBS))
    reclassed = os.path.join(Neighbourhood_dir + r"\{}".format(map_name) + r"\{}".format(NBS), "{}_recl.tif".format(map_name[:3]))
    out = Reclassify(map, "VALUE",
                           RemapRange(reclass_dict[NBS]))
    out.save(reclassed)
    return reclassed


def reclass_category(Neighbourhood_dir,NBS,Raster,reclass_dictionary,integer_string_dict,name,reclass_field='Value',filter=False):
    """
    reclass_dictionary: The dictionary that the name of the class is key and the value of scale is value
    integer_string_dict: The dictionary showing the integer value assigned to each categorical class in the raster file
    reclass_field: The name of the field in the raster file that is reclassified, default is 'value'

    """
    os.makedirs(Neighbourhood_dir + r"\{}".format(name) + r"\Raster" + r"\{}".format(NBS) + r"\Reclassified")
    Ras_NBS = os.path.join(Neighbourhood_dir + r"\{}".format(name) + r"\Raster" + r"\{}".format(NBS) + r"\Reclassified",
                               "{}.tif".format(NBS[:7]))
    os.makedirs(Neighbourhood_dir + r"\{}".format(NBS) + r"\Raster" + r"\{}".format(NBS) + r"\Filter")
    Filter_NBS = os.path.join(Neighbourhood_dir + r"\{}".format(NBS) + r"\Raster" + r"\{}".format(NBS) + r"\Filter",
                                  "{}.tif".format(NBS[:7]))
    NBS_dict = reclass_dictionary[NBS]
    if filter == True:
        filter_dict = {}
        for key, value in NBS_dict.items():
            if value != 0:
                filter_dict[key] = 1
            else:
                filter_dict[key] = 0
    remap_NBS_list = []
    remap_NBS_filter_list = []
    for i,v in integer_string_dict.items():
        remap_NBS_list.append([v, NBS_dict[i]])
        if filter == True:
            remap_NBS_filter_list.append([v, filter_dict[i]])
    remap = RemapValue(remap_NBS_list)
    out = Reclassify(Raster, reclass_field, remap=remap)
    out.save(Ras_NBS)
    if filter == True:
        remap_filter = RemapValue(remap_NBS_filter_list)
        out = Reclassify(Raster, reclass_field, remap=remap_filter)
        out.save(Filter_NBS)
        return Ras_NBS,Filter_NBS
    else:
        return Ras_NBS







building_buffer_dict={'RainGarden':3,'BioSwale':3,'permeable_pavement':3,'DetentionPond':10,'Tree':3,'RetentionPond':10}
def buffer_to_objects(Neighbourhood_dir,map,map_name,NBS,buffer_dict=building_buffer_dict):
    """
    Generate a boolean raster based on the buffer to objects(vector data)
    """
    os.makedirs(Neighbourhood_dir + r"\{}_buffer".format(map_name) + r"\{}".format(NBS) + r"\Vector")
    buffer = os.path.join(Neighbourhood_dir + r"\{}_buffer".format(map_name) + r"\{}".format(NBS) + r"\Vector",
                          "buffer_{}.shp".format(NBS[:3]))
    os.makedirs(Neighbourhood_dir + r"\{}_buffer".format(map_name) + r"\{}".format(NBS) + r"\raster")
    buff = os.path.join(Neighbourhood_dir + r"\{}_buffer".format(map_name) + r"\{}".format(NBS) + r"\raster", "{}_buf.tif".format(map_name[:3]))
    os.makedirs(Neighbourhood_dir + r"\{}_buffer".format(map_name) + r"\{}".format(NBS) + r"\raster" + r"\reclassified")
    buff_recl = os.path.join(
        Neighbourhood_dir + r"\{}_buffer".format(map_name) + r"\{}".format(NBS) + r"\raster" + r"\reclassified", "{}_recl.tif".format(map_name[:3]))
    if NBS in building_buffer_dict.keys():
        arcpy.Buffer_analysis(in_features=map, out_feature_class=buffer, buffer_distance_or_field="{} Meters".format(buffer_dict[NBS]),
                              line_side="FULL", line_end_type="ROUND", dissolve_option="ALL", dissolve_field="",
                              method="PLANAR")

        arcpy.PolygonToRaster_conversion(in_features=buffer, value_field="Id", out_rasterdataset=buff,
                                         cell_assignment="MAXIMUM_COMBINED_AREA", priority_field="NONE", cellsize="1")
        out = Reclassify(buff, "VALUE", RemapRange([[0, 0], [0, 1, 0], ['NODATA', 1]]))
        out.save(buff_recl)
        return buff_recl



def binary_threshold(Neighbourhood_dir,raster,threshold,map_name,NBS):

    arcpy.MakeRasterLayer_management(raster, "raster_layer")
    os.makedirs(Neighbourhood_dir + r"\{}".format(map_name) + r"\{}".format(NBS))
    raster_new = os.path.join(Neighbourhood_dir + r"\{}".format(map_name) + r"\{}".format(NBS), "{}_{}.tif".format(NBS, threshold))
    arcpy.gp.RasterCalculator_sa('"raster_layer"  <  {}'.format(threshold),raster_new)
    return raster_new


def binary_threshold_vector(Neighbourhood_dir,vector,columns,threshold,map_name,field_name,NBS):
    add_field(vector,columns[1])
    with arcpy.da.UpdateCursor(vector, columns) as rows:
        for row in rows:
            if row[0] >= int(threshold):
                row[1] = 1
            else:
                row[1] = 0
            rows.updateRow(row)
    os.makedirs(Neighbourhood_dir + r"\{}".format(map_name) + r"\{}".format(NBS))
    out_raster = os.path.join(Neighbourhood_dir + r"\{}".format(map_name) + r"\{}".format(NBS), "{}_{}.tif".format(NBS,threshold))
    arcpy.PolygonToRaster_conversion(in_features=vector, value_field="{}".format(field_name),
                                     out_rasterdataset=out_raster, cell_assignment="CELL_CENTER",
                                     priority_field="NONE", cellsize="1")
    return out_raster


def add_field(vector,field_name,field_type="DOUBLE"):
    fields=arcpy.ListFields(vector)
    if field_name not in fields:
        arcpy.AddField_management(in_table=vector, field_name=field_name, field_type=field_type, field_precision="", field_scale="", field_length="", field_alias="", field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")
    else:
        pass




def raster_to_vector_zonal(Neighbourhood_dir,zone_vector,raster):


    os.makedirs(Neighbourhood_dir + r"\output" + r"\Roof" + r"\table")
    table_dir = Neighbourhood_dir + r"\output" + r"\Roof" + r"\table"
    os.makedirs(Neighbourhood_dir + r"\output" + r"\Roof" + r"\Combined")
    out_path = Neighbourhood_dir + r"\output" + r"\Roof" + r"\Combined"
    arcpy.gp.ZonalStatisticsAsTable_sa(zone_vector, "FID", raster, os.path.join(table_dir, 'table'), "DATA",
                                       "MEAN")
    arcpy.JoinField_management(in_data=zone_vector, in_field="FID", join_table=os.path.join(table_dir, 'table'),
                               join_field="FID", fields="MEAN")
    arcpy.FeatureClassToFeatureClass_conversion(in_features=zone_vector,
                                                out_path=out_path,
                                                out_name="greenroof.shp", where_clause="",
                                                field_mapping='MEAN "MEAN" true true false 19 Double 0 0 ,First,#,build_clip,MEAN,-1,-1',
                                                config_keyword="")

    out=os.path.join(out_path,'greenroof.shp')
    return out



def save_raster(Neighbourhood_dir,map,map_name):

    os.makedirs(Neighbourhood_dir + r"\{}".format(map_name))
    raster_path = os.path.join(Neighbourhood_dir + r"\{}".format(map_name), r"\{}.tif".format(map_name[:4]))
    map.save(raster_path)
    return raster_path


################################################################






def BGT_for_NBS(Neighbourhood_dir,map,NBS,field_dict,BGT_NBS_dict=BGT_NBS_dict,BGT_vector=None,integer_field="Value",area_field="Shape_Area"):
    os.makedirs(Neighbourhood_dir + r"\BGT" + r"\Raster" + r"\{}".format(NBS) + r"\Reclassified")
    BGT_Ras_NBS = os.path.join(Neighbourhood_dir + r"\BGT" + r"\Raster" + r"\{}".format(NBS) + r"\Reclassified","{}.tif".format(NBS[:7]))
    os.makedirs(Neighbourhood_dir + r"\BGT" + r"\Raster" + r"\{}".format(NBS) + r"\Filter")
    BGT_Filter_NBS = os.path.join(Neighbourhood_dir + r"\BGT" + r"\Raster" + r"\{}".format(NBS) + r"\Filter","{}.tif".format(NBS[:7]))
    BGT_NBS_dict=BGT_NBS_dict[NBS]
    BGT_filter_dict = {}
    for key, value in BGT_NBS_dict.items():
        if value != 0:
            BGT_filter_dict[key] = 1
        else:
            BGT_filter_dict[key] = 0
    remap_NBS_BGT_list = []
    remap_NBS_BGT_filter_list = []
    field_names=field_dict.keys()
    for i in field_names:
        remap_NBS_BGT_list.append([field_dict[i], BGT_NBS_dict[i]])
        remap_NBS_BGT_filter_list.append([field_dict[i], BGT_filter_dict[i]])
    remap_NBS_BGT = RemapValue(remap_NBS_BGT_list)
    remap_NBS_BGT_filter = RemapValue(remap_NBS_BGT_filter_list)
    BGT_NBS_out = Reclassify(map, integer_field, remap=remap_NBS_BGT)
    BGT_NBS_out.save(BGT_Ras_NBS)
    BGT_NBS_filter_out = Reclassify(map, integer_field, remap=remap_NBS_BGT_filter)
    BGT_NBS_filter_out.save(BGT_Filter_NBS)
    if NBS=='DetentionPond' or NBS=='RetentionPond':
        if not os.path.exists(Neighbourhood_dir + r"\BGT" + r"\Size" + r"\Raster"):
            os.makedirs(Neighbourhood_dir + r"\BGT" + r"\Size" + r"\Raster")
            Size_ras = os.path.join(Neighbourhood_dir + r"\BGT" + r"\Size" + r"\Raster", "Size.tif")
            arcpy.PolygonToRaster_conversion(in_features=BGT_vector, value_field=area_field,
                                             out_rasterdataset=Size_ras,
                                             cell_assignment="CELL_CENTER", priority_field="NONE", cellsize="1")
            os.makedirs(Neighbourhood_dir + r"\BGT" + r"\Size" + r"\Raster" + r"\Reclassified")
            Size_ras_recl = os.path.join(Neighbourhood_dir + r"\BGT" + r"\Size" + r"\Raster" + r"\Reclassified",
                                         "Size_recl.tif")
            arcpy.gp.Reclassify_sa(Size_ras, integer_field,
                                   "0.031712 0;0.031712 1552.473624 1;1552.473624 3104.915535 2;3104.915535 6209.799358 3;6209.799358 10867.125093 3;10867.125093 18629.334651 4;18629.334651 29496.428032 4;29496.428032 51230.614793 5;51230.614793 94698.988317 5;94698.988317 397425.161069 5",
                                   Size_ras_recl, "DATA")
        else:
            Size_ras_recl = os.path.join(Neighbourhood_dir + r"\BGT" + r"\Size" + r"\Raster" + r"\Reclassified",
                                         "Size_recl.tif")
        return BGT_Ras_NBS,BGT_Filter_NBS,Size_ras_recl
    else:
        return BGT_Ras_NBS,BGT_Filter_NBS,None





###########


def ownership_reclass(Neighbourhood_dir,NBS,Own_Ras,ownership_field="EIGENAAR",ownership_reclass_dict=ownership_reclass_dict):
    """
    reclassify the cliped ownership file for each NBS
    """
    ownership_field_names = []
    os.makedirs(Neighbourhood_dir + r"\ownership" + r"\reclassified"+r"\{}".format(NBS))
    Ownership_reclass = os.path.join(Neighbourhood_dir + r"\ownership" + r"\reclassified"+r"\{}".format(NBS), "ownership.tif")
    owner_fields = arcpy.SearchCursor(Own_Ras, "", "", ownership_field, "")
    for owner_field in owner_fields:
        ow_field = owner_field.getValue(ownership_field)
        ownership_field_names.append(ow_field)
    remap_list = []
    for i in ownership_field_names:
        remap_list.append([i, ownership_reclass_dict[NBS]['public']])
    remap_list.append(["NODATA", ownership_reclass_dict[NBS]['private']])
    remap_ownership = RemapValue(remap_list)
    Owner_out = Reclassify(Own_Ras, ownership_field, remap=remap_ownership)
    Owner_out.save(Ownership_reclass)
    return Ownership_reclass



#############

###############################


def opportunity(Neighbourhood_dir,nbs,BGT_Filter_NBS,pond_buff_recl,TPZ,Ownership_reclass,BGT_Ras_NBS,Slope_reclassed,Gr_Water_Reclass,Size_ras_recl,ownership_weight=1
                ,LandUse_weight=1,slope_weight=1,GroundWater_weight=1,Size_weight=1):

    if nbs=='RetentionPond' or nbs=='DetentionPond':
        Output =float(Size_weight) * (Raster(Size_ras_recl)) + float(ownership_weight) * (Raster(Ownership_reclass)) + (float(LandUse_weight) * Raster(BGT_Ras_NBS)) + \
                (float(GroundWater_weight) * Raster(Gr_Water_Reclass)) + (float(slope_weight) * Raster(Slope_reclassed))
    else:
        Output = Raster(BGT_Filter_NBS) * Raster(pond_buff_recl) * Raster(TPZ) * (float(ownership_weight) * (Raster(Ownership_reclass)) + (
                float(LandUse_weight) * Raster(BGT_Ras_NBS)) + (float(slope_weight) * Raster(Slope_reclassed)) + (
                                                                 float(GroundWater_weight) * Raster(
                                                             Gr_Water_Reclass)))


    os.makedirs(Neighbourhood_dir + r"\output" + r"\Opportunity" + r"\{}".format(nbs))
    Output.save(os.path.join(Neighbourhood_dir + r"\output" + r"\Opportunity" + r"\{}".format(nbs),
                         "{}_opp.tif".format(nbs[:4])))
    Opportunity = os.path.join(Neighbourhood_dir + r"\output" + r"\Opportunity" + r"\{}".format(nbs),
                               "{}_opp.tif".format(nbs[:4]))
    opportunities_NBS = Raster(Opportunity)
    Opportunities_NBS_nrm = ((opportunities_NBS - 0) / (40 - 0)) * 5
    os.makedirs(Neighbourhood_dir + r"\output" + r"\Opportunity" + r"\{}".format(nbs) + r"\normal")
    Opportunities_NBS_nrm.save(
        os.path.join(Neighbourhood_dir + r"\output" + r"\Opportunity" + r"\{}".format(nbs) + r"\normal", "Opp_nrm.tif"))
    Opportunity_nrm_path = os.path.join(
        os.path.join(Neighbourhood_dir + r"\output" + r"\Opportunity" + r"\{}".format(nbs) + r"\normal", "Opp_nrm.tif"))

    return Opportunity_nrm_path





def challenge_generate(Neighbourhood_dir,nbs,heat_nrm_nbs,Str_Reclass,UHI_weight=1,Storm_Weight=1):
    challenge_ras = ((float(UHI_weight) * Raster(heat_nrm_nbs))) + ((float(Storm_Weight) * Raster(Str_Reclass)))

    os.makedirs(Neighbourhood_dir + r"\output" + r"\Challenge" + r"\{}".format(nbs))
    challenge_ras.save(os.path.join(Neighbourhood_dir + r"\output" + r"\Challenge" + r"\{}".format(nbs),
                                    "{}_chl.tif".format(nbs[:4])))
    challenge = os.path.join(Neighbourhood_dir + r"\output" + r"\Challenge" + r"\{}".format(nbs),
                             "{}_chl.tif".format(nbs[:4]))

    challenge_NBS = Raster(challenge)
    challlenge_NBS_nrm = ((challenge_NBS - 0) / (20 - 0)) * 5
    os.makedirs(Neighbourhood_dir + r"\output" + r"\Challenge" + r"\{}".format(nbs) + r"\normal")
    challlenge_NBS_nrm.save(
        os.path.join(Neighbourhood_dir + r"\output" + r"\Challenge" + r"\{}".format(nbs) + r"\normal",
                     "chl_nrm.tif"))
    challenge_nrm_path = os.path.join(
        os.path.join(Neighbourhood_dir + r"\output" + r"\Challenge" + r"\{}".format(nbs) + r"\normal",
                     "chl_nrm.tif"))
    return challenge_nrm_path