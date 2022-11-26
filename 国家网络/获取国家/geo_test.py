from geotext import GeoText
import json
# places=GeoText("Cardiff University, UK")
# print("places:",places.country_mentions)
uncertain_file=open("11月location_uncertain.json",'r')
uncertain_file_str=uncertain_file.read()
uncertain_file_lst=uncertain_file_str.split("---------------------------------\n")
#二次筛选
geotext_res2=open("11月location_certain_res2.json",'w')
geotext_uncertain_res2=open("11月location_uncertain2.json",'w')
count=0
def transformToCertain(country_lst):
    for country in country_lst:
        if country == 'uncertain':
            return False
    return True
for i in range(0,len(uncertain_file_lst)-1):
    line = json.loads(uncertain_file_lst[i])
    author_location = line["author_location"]
    country_lst=line["country"]
    for j in range(0,len(country_lst)):
        split_location=author_location[j].split(',')
        last_location=split_location[len(split_location)-1]
        print('last_location:',last_location)
        if last_location == " USA" and country_lst[j] == 'uncertain':
            count+=1
            country_lst[j]='US'
        elif last_location == " Korea" and country_lst[j] == 'uncertain':
            count+=1
            country_lst[j]='KR'
        elif last_location==' The Netherlands' and country_lst[j] == 'uncertain':
            count+=1
            country_lst[j]='NLD'
        elif last_location==' France' and country_lst[j] == 'uncertain':
            count+=1
            country_lst[j]='FR'
        elif last_location==' P. R. China' and country_lst[j] == 'uncertain':
            count+=1
            country_lst[j]='CN'
        elif last_location==' Mexico' and country_lst[j] == 'uncertain':
            count+=1
            country_lst[j]='MEX'
        elif last_location==' Switzerland' and country_lst[j]=='uncertain':
            count+=1
            country_lst[j]='CH'
        elif last_location==' Brazil' and country_lst[j]=='uncertain':
            count += 1
            country_lst[j] = 'BR'
        elif last_location==' UK' and country_lst[j] == 'uncertain':
            count+=1
            country_lst[j]='GB'
        elif (last_location==' Rep. of Korea' or last_location == ' Republic of Korea') and country_lst[j]=='uncertain':
            count += 1
            country_lst[j] = 'KR'
    if transformToCertain(country_lst) == True:
        geotext_res2.write(json.dumps(line)+'\n')
        geotext_res2.write("---------------------------------\n")
    else:
        geotext_uncertain_res2.write(json.dumps(line)+'\n')
        geotext_uncertain_res2.write("---------------------------------\n")
print("count:",count)
uncertain_file.close()
geotext_res2.close()
geotext_uncertain_res2.close()