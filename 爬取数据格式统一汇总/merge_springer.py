#对springer数据进行格式统一与整合
import json
springer_crawl_data=open("../crawlers/11新增/springer_res1", "r")
springer_crawl_data_str=springer_crawl_data.read()
springer_crawl_data_lst=springer_crawl_data_str.split("---------------------------------\n")
springer_inproceeding_merge_res=open("../crawlers/11新增/springer_crawl_result_merge.json", "w")
for i in range(0,len(springer_crawl_data_lst)-1):
    print('第', i, '个')
    springer_info_dict = {}
    springer_info_dict["title"] = ""
    springer_info_dict["date"] = ""
    springer_info_dict["publish"] = ""
    springer_info_dict["abstract"] = ""
    springer_info_dict["source"] = "springer_unknown"
    springer_info_dict["author"] = []
    springer_info_dict["author_location"] = []
    springer_info_dict["keywords"] = []
    # 将Json字符串解码成python对象
    line = json.loads(springer_crawl_data_lst[i])
    print(line)
    print(type(line))
    springer_info_dict["title"] = line["title"]
    springer_info_dict["date"] = line["date"]
    springer_info_dict["link"] = line["link"]
    springer_info_dict["abstract"] = line["abstract"]
    springer_info_dict["publish"] = line["publish"]
    springer_info_dict["author"] = line["author"]
    springer_info_dict["keywords"]=[]
    author_location=[]
    # print(line["author_location"])

    for location in line["author_location"]:
        if len(location) == 1:
            author_location.append(location[0]["address"]["name"])
    springer_info_dict["author_location"] = author_location
    keywords = line["keywords"].split(',')
    springer_info_dict["keywords"]=keywords
    print("springer_info_dict:", springer_info_dict)
    springer_inproceeding_merge_res.write(json.dumps(springer_info_dict)+'\n')
    springer_inproceeding_merge_res.write("---------------------------------\n")


springer_crawl_data.close()

