#对elsevier数据进行格式统一与整合
import json
elsevier_crawl_data=open("elsevier_crawl_results.json","r")
elsevier_crawl_data_str=elsevier_crawl_data.read()
elsevier_crawl_data_lst=elsevier_crawl_data_str.split("---------------------------------\n")
elsevier_crawl_data.close()
elsevier_data_merge_res=open("elsevier_crawl_result_merge.json",'w')
count=0
for i in range(0,len(elsevier_crawl_data_lst)-1):
    print("article 第",i,"个")
    count+=1
    elsevier_info_dict = {}
    elsevier_info_dict["title"] = ""
    elsevier_info_dict["date"] = ""
    elsevier_info_dict["publish"] = ""
    elsevier_info_dict["abstract"] = ""
    elsevier_info_dict["link"]=""
    elsevier_info_dict["source"] = "elsevier_unknown"
    elsevier_info_dict["author"] = []
    elsevier_info_dict["author_location"] = []
    elsevier_info_dict["keywords"] = []
    # 将Json字符串解码成python对象
    line = json.loads(elsevier_crawl_data_lst[i])
    print(line)
    print(type(line))
    elsevier_info_dict["title"] = line["title"]
    elsevier_info_dict["date"] = line["Year"]
    elsevier_info_dict["link"] = line["url"]
    elsevier_info_dict["abstract"] = line["abstract"]
    elsevier_info_dict["publish"] = line["journal"]
    elsevier_info_dict["author"] = line["author"]
    elsevier_info_dict["author_location"] = line["author_location"]
    elsevier_info_dict["keywords"] = line["keywords"]
    print("elsevier_info_dict:", elsevier_info_dict)
    elsevier_data_merge_res.write(json.dumps(elsevier_info_dict) + "\n")
    elsevier_data_merge_res.write("---------------------------------\n")
elsevier_data_merge_res.close()
elsevier_crawl_data.close()
