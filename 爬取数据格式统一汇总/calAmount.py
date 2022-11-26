import json
f=open("../fourpublisher_crawl_result_updateauthors_withcountry_final.json","r")
f_str=f.read()
lst=f_str.split('---------------------------------\n')
res_f=open("fourpublisher_crawl_result_updateauthors_withcountry_finalfinal.json","w")
print("len:",len(lst)-1)
title_set=set()
for i in range(0,len(lst)-1):
    json_str=json.loads(lst[i])
    link=json_str["link"].split("\n")[0]
    json_str["link"]=link
    print("link:",link)
    res_f.write(json.dumps(json_str)+'\n')
    res_f.write('---------------------------------\n')
    # if lst[i] in title_set:
    #     print(i)
    #
    #     break
    # else:
    #     title_set.add(lst[i])

print("set size:",len(title_set))
f.close()
res_f.close()