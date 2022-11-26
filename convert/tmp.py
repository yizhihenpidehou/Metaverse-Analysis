import json
ff=open("../2022-01/fourpublisher_arxiv_withsource_updatedauthor_citation2022-01.json",'r')
ff_str=ff.read()
lst=ff_str.split("---------------------------------\n")
res_ff=open("../2022-01/fourpublisher_arxiv_withsource_updatedauthor_citation2022-01final.json",'w')
for i in range(0,len(lst)-1):
    sstr=json.loads(lst[i])
    publish=sstr["publisher"]
    del sstr["publisher"]
    sstr["publish"]=publish
    res_ff.write(json.dumps(sstr)+'\n')
    res_ff.write('---------------------------------\n')

ff.close()
res_ff.close()