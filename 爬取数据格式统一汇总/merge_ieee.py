#对ieee数据进行格式统一与整合
import json
ieee_data_res=open("../crawlers/11新增/ieee_res_finalfinal.json", "r")
ieee_data_str=ieee_data_res.read()
ieee_data_lst=ieee_data_str.split("---------------------------------\n")
ieee_data_merge=open('../crawlers/11新增/ieee_crawl_result_merge.json', 'w')
count=0
for i in range(0,len(ieee_data_lst)-1):
    print("count:",count)
    print("第",i,"个")
    ieee_info_dict={}
    ieee_info_dict["title"] = ""
    ieee_info_dict["date"] = ""
    ieee_info_dict["publish"] = ""
    ieee_info_dict["abstract"] = ""
    ieee_info_dict["source"] = "ieee_unknown"
    ieee_info_dict["author"] = []
    ieee_info_dict["author_location"] = []
    ieee_info_dict["keywords"] = []
    # 将Json字符串解码成python对象
    line = json.loads(ieee_data_lst[i])
    print(line)
    print(type(line))
    if line["abstract"] == "not found":
        continue
    count+=1
    ieee_info_dict["title"] = line["title"]
    ieee_info_dict["date"] = line["date"]
    ieee_info_dict["link"] = line["link"]
    ieee_info_dict["abstract"] = line["abstract"]
    ieee_info_dict["publish"] = line["publish"]
    ieee_info_dict["author"] = line["author"]
    author_location=[]
    author_location_possess=line["author_location"]
    if len(author_location_possess) ==1 and author_location_possess[0] == 'no_location':
        author_location .append("no location")
    else:
        for location in author_location_possess:
            author_location.append(location[0])
    ieee_info_dict["author_location"] = author_location
    print("author_location:",author_location)
    print("ieee_info_dict:", ieee_info_dict)
    ieee_data_merge.write(json.dumps(ieee_info_dict) + "\n")
    ieee_data_merge.write("---------------------------------\n")

ieee_data_merge.close()
