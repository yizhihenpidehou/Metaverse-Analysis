import json
#对acm数据进行格式统一与整合
acm_crawl_data=open("../crawlers/11新增/acm_res1.json", "r")
#---------------------acm_inproceedings---------------------
acm_crawl_data_str=acm_crawl_data.read()
acm_crawl_data_lst=acm_crawl_data_str.split("---------------------------------\n")
acm_data_merge_res=open("../crawlers/11新增/acm_crawl_result_merge.json", "w")
for i in range(0,len(acm_crawl_data_lst)-1):
    print("i:",i)
    acm_info_dict = {}
    acm_info_dict["title"] = ""
    acm_info_dict["date"] = ""
    acm_info_dict["publish"] = ""
    acm_info_dict["abstract"] = ""
    acm_info_dict["source"]="acm"
    acm_info_dict["author"] = []
    acm_info_dict["author_location"] = []
    acm_info_dict["keywords"] = []
    # 将Json字符串解码成python对象
    line=json.loads(acm_crawl_data_lst[i])
    print(line)
    print(type(line))
    acm_info_dict["title"]=line["title"]
    acm_info_dict["date"]=line["date"]
    acm_info_dict["link"]=line["link"]
    acm_info_dict["abstract"]=line["abstract"]
    acm_info_dict["publish"]=line["publish"]
    acm_info_dict["author"]=line["author"]
    acm_info_dict["author_location"]=line["author_location"]
    print("acm_info_dict:",acm_info_dict)
    acm_data_merge_res.write(json.dumps(acm_info_dict)+"\n")
    acm_data_merge_res.write("---------------------------------\n")
acm_data_merge_res.close()
acm_crawl_data.close()