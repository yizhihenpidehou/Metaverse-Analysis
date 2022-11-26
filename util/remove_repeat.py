import json
for i in range(1,12):
    tarurl=""
    resurl=""
    month=i
    if month < 10:
        tarurl="../2022-0"+str(month)+"/fourpublisher_arxiv_withsource_updatedauthor_citation"+"2022-0"+str(month)+".json"
        resurl="../2022-0"+str(month)+"/fourpublisher_arxiv_withsource_updatedauthor_citation"+"2022-0"+str(month)+"_final.json"
    else:
        tarurl="../2022-"+str(month)+"/fourpublisher_arxiv_withsource_updatedauthor_citation"+"2022-"+str(month)+".json"
        resurl = "../2022-" + str(month) + "/fourpublisher_arxiv_withsource_updatedauthor_citation" + "2022-" + str(
            month) + "_final.json"
    tarfile = open(tarurl, 'r')

    tar_str=tarfile.read()
    lst=tar_str.split("---------------------------------\n")
    title_lst=list()
    print("ini:",len(lst)-1)
    resfile=open(resurl,'w')
    for i in range(0,len(lst)-1):
        json_str=json.loads(lst[i])
        title=json_str["title"]
        if title.lower() not in title_lst:
            title_lst.append(title.lower())
            resfile.write(json.dumps(json_str)+'\n')
            resfile.write("---------------------------------\n")
    print("size:",len(title_lst))
    tarfile.close()
    resfile.close()