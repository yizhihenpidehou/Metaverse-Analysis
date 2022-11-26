import json
uncertain_file=open("新增关键词后/2021new/geotext_google_2021_res.json",'r')
uncertain_str=uncertain_file.read()
uncertain_lst=uncertain_str.split("---------------------------------\n")
geotext_geogle_res_final=open("新增关键词后/2021new/geotext_google_2021_res_final.json",'w')
ctmighterror_file=open("新增关键词后/2021new/ctmighterror_2021_file.json",'w')
count=0
def existUncertain(country_lst):
    for country in country_lst:
        if country == 'uncertain':
            return True
    return False

for i in range(0,len(uncertain_lst)-1):
    line = json.loads(uncertain_lst[i])
    ctmighterror = line["ctmighterror"]
    country_lst=line["country"]
    print("ctmighterror:",ctmighterror)
    print("country_lst:",country_lst)
    if len(ctmighterror) >= 1 or existUncertain(country_lst):
        ctmighterror_file.write(json.dumps(line)+'\n')
        ctmighterror_file.write('---------------------------------\n')
        count+=1
    else:
        geotext_geogle_res_final.write(json.dumps(line)+'\n')
        geotext_geogle_res_final.write('---------------------------------\n')


print("count:",count)
uncertain_file.close()
geotext_geogle_res_final.close()
ctmighterror_file.close()