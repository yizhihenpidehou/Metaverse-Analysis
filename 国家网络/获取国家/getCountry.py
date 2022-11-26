import json
from geotext import GeoText
second_filtered=open("../../2022-11/fourpublisher_arxiv_withsource_updatedauthor_citation2022-11_final.json",'r')
second_filtered_str=second_filtered.read()
second_filtered_lst=second_filtered_str.split("---------------------------------\n")
print("len:",len(second_filtered_lst))
print("len:",len(set(second_filtered_lst)))
geotext_res=open("11月location_certain_res.json",'w')
geotext_uncertain_res=open("11月location_uncertain.json",'w')
count=0
for i in range(0,len(second_filtered_lst)-1):#len(second_filtered_lst)-1
    print("第",i,"个")
    line=json.loads(second_filtered_lst[i])
    author_location=line["author_location"]
    flag=False
    country=[]
    for location in author_location:
        print("loca:",location)
        places=GeoText(location)
        print("places:",places.country_mentions)
        country_mentions=places.country_mentions
        certain_country=""
        if len(country_mentions.items())>0:
            #拿到最可能的国家缩写
            certain_country=list(country_mentions.items())
            print("certain country:",certain_country[0][0])
            country.append(certain_country[0][0])
        else:
            country.append("uncertain")
            flag=True
    print("country",country)
    line["country"] = country
    print("line:",line)
    if flag==True:
        geotext_uncertain_res.write(json.dumps(line)+'\n')
        geotext_uncertain_res.write('---------------------------------\n')
    else:
        geotext_res.write(json.dumps(line)+'\n')
        geotext_res.write('---------------------------------\n')

second_filtered.close()
geotext_res.close()
geotext_uncertain_res.close()