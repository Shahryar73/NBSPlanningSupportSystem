import arcpy
from utils import add_field

Neighbourhoods_Map=arcpy.GetParameterAsText(0)
challenge1path=arcpy.GetParameterAsText(1)
challenge1name=arcpy.GetParameterAsText(2)
challenge2path=arcpy.GetParameterAsText(3)
challenge2name=arcpy.GetParameterAsText(4)
challenge3path=arcpy.GetParameterAsText(5)
challenge3name=arcpy.GetParameterAsText(6)
challenge4path=arcpy.GetParameterAsText(7)
challenge4name=arcpy.GetParameterAsText(8)
challenge5path=arcpy.GetParameterAsText(9)
challenge5name=arcpy.GetParameterAsText(10)
challenge1weight=arcpy.GetParameterAsText(11)
challenge2weight=arcpy.GetParameterAsText(12)
challenge3weight=arcpy.GetParameterAsText(13)
challenge4weight=arcpy.GetParameterAsText(14)
challenge5weight=arcpy.GetParameterAsText(15)
join_field=arcpy.GetParameterAsText(16)





# #
join_field='buurtnaam'
challenge1name='air_quality'
challenge2name='StormWater_management'
challenge3name='UHI'
challenge4name='biodiversity'
challenge5name='environmental_equity'


#############################################
"""
1- Get the data from each challenge map, normalize it and add it as a new field to the neighbourhood map
2- Calculate the total score using weighted linear combination(WLC) method considering the user-defined weights
"""

FieldName='chalng'
challenges={'challenge1':{'challenge_name':challenge1name,'challenge_field':'value','challenge_file':challenge1path,'challenge_weight':challenge1weight},
            'challenge2':{'challenge_name':challenge2name,'challenge_field':'value','challenge_file':challenge2path,'challenge_weight':challenge2weight},
            'challenge3':{'challenge_name':challenge3name,'challenge_field':'value','challenge_file':challenge3path,'challenge_weight':challenge3weight},
            'challenge4':{'challenge_name':challenge4name,'challenge_field':'value','challenge_file':challenge4path,'challenge_weight':challenge4weight},
            'challenge5':{'challenge_name':challenge5name,'challenge_field':'value','challenge_file':challenge5path,'challenge_weight':challenge5weight},
            }

NBS_dict={'tree':{'UHI':5,'StormWater_management':3,'air_quality':5,'biodiversity':4,'environmental_equity':3},
          'extensive_greenroof':{'UHI':3,'StormWater_management':2,'air_quality':3,'biodiversity':3,'environmental_equity':2},
          'intensive_greenroof':{'UHI':4,'StormWater_management':4,'air_quality':5,'biodiversity':4,'environmental_equity':4},
          'raingarden':{'UHI':3,'StormWater_management':5,'air_quality':2,'biodiversity':3,'environmental_equity':1},
          'swale':{'UHI':2,'StormWater_management':4,'air_quality':2,'biodiversity':2,'environmental_equity':2},
          'permeable_pavement':{'UHI':2,'StormWater_management':3,'air_quality':1,'biodiversity':1,'environmental_equity':1},
          'detention_basin':{'UHI':2,'StormWater_management':3,'air_quality':1,'biodiversity':2,'environmental_equity':3},
          'retention_pond':{'UHI':3,'StormWater_management':2,'air_quality':1,'biodiversity':4,'environmental_equity':4},
          }
#########################################



new_fields={}
for k,v in challenges.items():
    chlg_list = []
    neighbourhood_challenges = []
    new_field = "{}_nrm".format(v['challenge_name'][:3])
    new_fields[k] = new_field
    fields = arcpy.ListFields(v['challenge_file'])
    add_field(v['challenge_file'],new_field)
    # add_field(Neighbourhoods_Map,new_field)
    with arcpy.da.SearchCursor(v['challenge_file'], [v['challenge_field']]) as rows:
        for row in rows:
            chlg_list.append(row[0])
    chlg_min = min(chlg_list)
    chlg_max = max(chlg_list)

    with arcpy.da.UpdateCursor(v['challenge_file'], [v['challenge_field'],new_field]) as datas:
        for data in datas:
            if chlg_min != 0 and chlg_max != 1:
                data[1] = (data[0] - chlg_min) / (chlg_max - chlg_min)
            else:
                data[1] = data[0]
            datas.updateRow(data)
    arcpy.JoinField_management(in_data=Neighbourhoods_Map, in_field=join_field, join_table=v['challenge_file'],
                               join_field=join_field, fields=new_field)


add_field(Neighbourhoods_Map, FieldName)
field_list = sorted(new_fields.values())
challenge_list = sorted(new_fields.keys())
field_list_n = field_list[:]
with arcpy.da.UpdateCursor(Neighbourhoods_Map, field_list_n + [FieldName]) as rows:
    for row in rows:
        for i in range(len(field_list)):
            row[-1] += row[i] * float(challenges[challenge_list[i]]['challenge_weight'])
        rows.updateRow(row)

"""
Calculate the score for each NBS in each neighbourhood considering the challenges in each neighbourhood and the performance of each NBS
"""

field_list_nbs=field_list[:]
for NBS in NBS_dict.keys():
    add_field(Neighbourhoods_Map,NBS[:5])
    with arcpy.da.UpdateCursor(Neighbourhoods_Map,field_list_nbs + [NBS[:5]]) as rows:
        for row in rows:
            for i in range(len(field_list)):
                row[-1] += row[i]*float(NBS_dict[NBS][challenges[challenge_list[i]]['challenge_name']])
            rows.updateRow(row)



