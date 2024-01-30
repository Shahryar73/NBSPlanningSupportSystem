import arcpy
import os
from arcpy.sa import *
from utils import extract_shape,buffer_around_shape,clip_vector,clip_raster,normalize,exclude_raster_value,distance_to_object,integer_from_string_fields,challenge_reclassify,range_reclass,buffer_to_objects,binary_threshold,binary_threshold_vector,add_field,raster_to_vector_zonal,save_raster,ownership_reclass,BGT_for_NBS,slope_reclass_dict,GW_reclass_dict,opportunity,challenge_generate

Neighbourhoods=arcpy.GetParameterAsText(0)
buildings=arcpy.GetParameterAsText(1)
Slope=arcpy.GetParameterAsText(2)
Ownership=arcpy.GetParameterAsText(3)
BGT=rarcpy.GetParameterAsText(4)
Building_use=arcpy.GetParameterAsText(5)
Trees=arcpy.GetParameterAsText(6)
PET=arcpy.GetParameterAsText(7)
width=arcpy.GetParameterAsText(8)
Electricity=arcpy.GetParameterAsText(9)
Flood=arcpy.GetParameterAsText(10)
groundwater=arcpy.GetParameterAsText(11)
Folder=arcpy.GetParameterAsText(12)


# #



params={'Storm_Weight':1,'AirQ_weight':0,'UHI_weight':1,'Challenge_Opportunity':1,'Ownership_class':2,'ownership_weight':1,'slope_weight':1,'LandUse_weight':1,'Size_weight':1,
        'GroundWater_weight':1,'WaterDistance_weight':1,'max_degree':35,'Min_roof_area':100,'Mimimum_Construction_year':0,'Width_as_a_criteria':0,'TreeProtectionZone':1}
# params={'Storm_Weight':Storm_Weight,'AirQ_weight':AirQ_weight,'UHI_weight':UHI_weight,'Challenge_Opportunity':Challenge_Opportunity,'Ownership_class':Ownership_class,'ownership_weight':ownership_weight,'slope_weight':slope_weight,'LandUse_weight':LandUse_weight,'Size_weight':Size_weight,
#         'GroundWater_weight':GroundWater_weight,'WaterDistance_weight':WaterDistance_weight,'max_degree':max_degree,'Min_roof_area':Min_roof_area,'Mimimum_Construction_year':Mimimum_Construction_year,'Width_as_a_criteria':Width_as_a_criteria,'TreeProtectionZone':TreeProtectionZone}


NBS_dic = {'RainGarden': 1, 'BioSwale': 0, 'permeable_pavement': 0,
           'DetentionPond': 0, 'Tree': 1, 'RetentionPond': 0,'Intensive_greenroof':1,'Extensive_greenroof':0}
NBS_list = []
for nbs, value in NBS_dic.items():
    if value == 1:
        NBS_list.append(nbs)



Neighbourhood_field="buurtnaam"
Neighbourhood_name_list="Strijp S"
Neighbourhood_name_list_r=str(Neighbourhood_name_list).split(";")
for Neighbourhood_name in Neighbourhood_name_list_r:

    #Clip the neighbourhood
    ##Make the boundry with buffer
    Neighbourhood_dir=Folder+r"\{}".format(Neighbourhood_name)
    Neighbourhood=extract_shape(Neighbourhood_dir,Neighbourhoods,Neighbourhood_name,Neighbourhood_field)
    Boundary=buffer_around_shape(Neighbourhood_dir,Neighbourhood_name,Neighbourhood)

    """
    Clip the challenge and opportunity indicator maps by the boundries of the selected neighbourhood(s)
    """
    ##Make Slope map
    Slope =clip_raster(Neighbourhood_dir, Neighbourhood, Slope, map_name='slope')
    ##Make a buffer around buildings and turn it to raster
    BAG_cliped=clip_vector(Neighbourhood_dir,buildings,Boundary,name='building')
    ##Convert BGT to raster and reclassify based on function
    BGT_Ras = clip_raster(Neighbourhood_dir, Neighbourhood, BGT, map_name='landuse')
    building_use = clip_raster(Neighbourhood_dir, Neighbourhood, Building_use, map_name='build_use')

    ##Convert Ownership to Raster and reclassify the values
    Own_Ras = clip_raster(Neighbourhood_dir, Neighbourhood, Ownership, map_name='ownership')

    ##MaskOut the groundWater Groundwater
    Groundwater_masked = clip_raster(Neighbourhood_dir, Neighbourhood, groundwater, map_name='groundwater')
    ##Tree protection Zone
    TPZ = clip_raster(Neighbourhood_dir, Neighbourhood, Trees, map_name='TPZ')

    #Make the heat stress map
    PET_msk_path=clip_raster(Neighbourhood_dir,Neighbourhood,PET,map_name='pet')
    PET_nrm=normalize(Neighbourhood_dir,PET_msk_path,map_name='pet')
    #make the stormwater map
    Str_Reclass_g = clip_raster(Neighbourhood_dir, Neighbourhood, Flood, map_name='storm')

    #map the fields
    field_dict=integer_from_string_fields(BGT_Ras)
    # Mask the water distance
    WaterWays_ras=exclude_raster_value(Neighbourhood_dir,BGT_Ras,map_name='WaterWay',exclude_value='water',field_dict=field_dict)
    #mask the road distance
    water_euclidean=distance_to_object(Neighbourhood_dir,WaterWays_ras,map_name='WaterWay')
    # RoadBuffer
    Roads_Ras_NBS = exclude_raster_value(Neighbourhood_dir, BGT_Ras, map_name='Roads', exclude_value='weg',field_dict=field_dict)
    Roads_euclidean = distance_to_object(Neighbourhood_dir, Roads_Ras_NBS, map_name='Roads')
    """
    Value scale the indicators for each NBS
    """

    for nbs in NBS_list:
        # reclassify the ownership
        Ownership_reclassed = ownership_reclass(Neighbourhood_dir,nbs, Own_Ras)
        # RoofTop analysis
        if nbs == 'Intensive_greenroof' or nbs == 'Extensive_greenroof':
            Roof_dir = Neighbourhood_dir + r"\Roof"
            # filter the slope
            if nbs=='Intensive_greenroof':
                Slope_binary = binary_threshold(Roof_dir, Slope, 15, map_name='slope',NBS=nbs)
            elif nbs == 'Extensive_greenroof':
                Slope_binary = binary_threshold(Roof_dir, Slope, 35, map_name='slope',NBS=nbs)
            # filter the Area
            add_field(BAG_cliped, field_name="flat_bool")
            out_area_raster = binary_threshold_vector(Roof_dir, BAG_cliped, columns=["area", "flat_bool"],threshold=100,map_name='area',field_name="flat_bool",NBS=nbs)

            # Add energy raster to UHI map
            roof_UHI=clip_raster(Roof_dir,Neighbourhood,Electricity,map_name='UHI')
            Roof_challenge_nrm_path=normalize(Roof_dir,roof_UHI,map_name='UHI',scalefactor=5)

            # LandUse data
            field_oms_dict = integer_from_string_fields(building_use, string_field="Omschrijvi", integer_field='Value')
            building_use_reclass, building_use_filter, a = BGT_for_NBS(Roof_dir, building_use,nbs,field_dict=field_oms_dict)

            # generate opportunity map
            # GreenRoof_opp = (Raster(Slope_binary) * Raster(out_area_raster) * (
            #         float(ownership_weight) * (Raster(Ownership_reclassed)) + (float(LandUse_weight)) * Raster(
            #     building_use_reclass))) / 4
            GreenRoof_opp_ras = (Raster(Slope_binary) * Raster(out_area_raster) * (
                    float(1) * (Raster(Ownership_reclassed)) + (float(1)) * Raster(
                building_use_reclass))) / 4
            os.makedirs(Roof_dir + r'\opportunity')
            GreenRoof_opp_path=os.path.join(Roof_dir + r'\opportunity','{}.tif'.format(nbs[:4]))
            GreenRoof_opp_ras.save(GreenRoof_opp_path)
            # combine the challenge and opportunity

            roof_combined = Raster(Roof_challenge_nrm_path) + Raster(GreenRoof_opp_path)
            os.makedirs(Roof_dir + r'\combined')
            roof_combined.save(os.path.join(Roof_dir + r'\combined','{}.tif'.format(nbs[:4])))

            #   Vectorize the green roof suitability
            # out_shape = raster_to_vector_zonal(Roof_dir, BAG_cliped, roof_ras_dir)

        else:

            # Make the StormWater management
            storm_coefficients={'RainGarden':0.8,'BioSwale':0.6,'permeable_pavement':0.8,'DetentionPond':1,'Tree':0.3,'RetentionPond':1}
            Str_Reclass=challenge_reclassify(Neighbourhood_dir,Str_Reclass_g,challenge_name='storm',NBS=nbs,coefficient_dict=storm_coefficients)
            # Make the heat stress
            heat_coef = {'RainGarden': 0.5, 'BioSwale': 0.5, 'permeable_pavement': 0.5, 'DetentionPond': 0.4, 'Tree': 1,
                         'RetentionPond': 0.4}
            heat_nrm_nbs=challenge_reclassify(Neighbourhood_dir,PET_nrm,challenge_name='pet',NBS=nbs,coefficient_dict=heat_coef)

            ##Make Slope map
            Slope_reclassed=range_reclass(Neighbourhood_dir,Slope,map_name='Slope',NBS=nbs,reclass_dict=slope_reclass_dict)

            ##Make a buffer around buildings and turn it to raster
            pond_buff_recl=buffer_to_objects(Neighbourhood_dir,BAG_cliped,map_name='building',NBS=nbs)

            ## Reclassify the landUse and LandCover
            BGT_Ras_NBS, BGT_Filter_NBS,Size_ras_recl=BGT_for_NBS(Neighbourhood_dir,BGT_Ras,NBS=nbs,field_dict=field_dict)

            #GroundWater
            Gr_Water_Reclass=range_reclass(Neighbourhood_dir,Groundwater_masked,map_name='groundwater',NBS=nbs,reclass_dict=GW_reclass_dict)


            if nbs =='Tree':
                TPZ_ex=os.path.join(Neighbourhood_dir + "/TPZ",'expand_tre.tif')
                arcpy.gp.Expand_sa(TPZ,TPZ_ex , "3",
                                   "0")
                TPZ=TPZ_ex
            """
            Generate the challenge and opportunity map and combine them
            """

            #Generate Opportunity map
            Opportunity_nrm_path=opportunity(Neighbourhood_dir,nbs=nbs,BGT_Filter_NBS=BGT_Filter_NBS,pond_buff_recl=pond_buff_recl,TPZ=TPZ,Ownership_reclass=Ownership_reclassed,
                                             BGT_Ras_NBS=BGT_Ras_NBS,Slope_reclassed=Slope_reclassed,Gr_Water_Reclass=Gr_Water_Reclass,Size_ras_recl=Size_ras_recl)

            #Make challenge map
            challenge_nrm_path=challenge_generate(Neighbourhood_dir,nbs=nbs,heat_nrm_nbs=heat_nrm_nbs,Str_Reclass=Str_Reclass)

            # Combine challenge and opportunity
            combined = Raster(width) * Raster(pond_buff_recl) * Raster(BGT_Filter_NBS) * Raster(TPZ) * (
                        Raster(challenge_nrm_path) + Raster(Opportunity_nrm_path))
            os.makedirs(Neighbourhood_dir + r"\output" + r"\combined" + r"\{}".format(nbs))
            combined_path = Neighbourhood_dir + r"\output" + r"\combined" + r"\{}".format(nbs)
            combined.save(os.path.join(combined_path,'combined.tif'))
            # combined_path=save_raster(Neighbourhood_dir,combined,map_name='combined')


    ## Make an empty Shapefile for cost estimation
    os.makedirs(Neighbourhood_dir+r"\CostEstimation")
    arcpy.CreateFeatureclass_management(Neighbourhood_dir+r"\CostEstimation","CostEst.shp","POLYGON")
