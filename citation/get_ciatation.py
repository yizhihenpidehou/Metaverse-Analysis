import json

tar_file=open("../动态分析/arxiv_withsource_updatedauthor2022-11_withgender.json",'r')
tar_str=tar_file.read()
tar_lst=tar_str.split("-------------------------------------\n")




supple_file=open("../2022-02/fourpublisher_arxiv_withsource_updatedauthor2022-02_withgender.json",'r')
supple_str=supple_file.read()
supple_lst=supple_str.split("---------------------------------\n")
res_file=open("../2022-02/fourpublisher_arxiv_withsource_updatedauthor_citation2022-02.json",'w')
for i in range(0,len(supple_lst)-1):
    supple_json=json.loads(supple_lst[i])
    supple_title=supple_json["title"]
    for j in range(0, len(tar_lst) - 1):
        print("tar_lst[j]:",tar_lst[j])
        tar_str = json.loads(tar_lst[j])
        tar_title=tar_str["title"]
        if supple_title == tar_title:
            citation = tar_str["citation"]
            supple_json["citation"]=citation
            res_file.write(json.dumps(supple_json)+"\n")
            res_file.write("---------------------------------\n")
            break

tar_file.close()
supple_file.close()
res_file.close()