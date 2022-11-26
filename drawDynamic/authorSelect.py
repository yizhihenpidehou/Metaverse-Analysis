import json
from author_cooperation import author_nx
basedir="../2022-"
if __name__=='__main__':
    author_dict = {}
    for i in range(1,12):
        if i<10:
            filename=basedir+'0'+str(i)+'/'+'fourpublisher_arxiv_withsource_updatedauthor2022-0'+str(i)+'.json'
        else:
            filename=basedir+str(i)+'/'+'fourpublisher_arxiv_withsource_updatedauthor2022-'+str(i)+'.json'
        tarfile=open(filename,'r')

        res_dict = author_nx.author_analysis_pipeline(filename, None)
        effective_size_res = res_dict["effective_size_res"]
        effective_size_res=sorted(list(effective_size_res.items()),key=lambda x:x[1],reverse=True)[:10]
        for item in effective_size_res:
            if item[0] not in author_dict.keys():
                author_dict[item[0]]=1
            else:
                author_dict[item[0]]+=1
        tarfile.close()
    candidate_author=[]
    for k,v in author_dict.items():
        print("v:",v)
        if v==11:
            candidate_author.append(k)
    print("candidate_author:",candidate_author)
    print("candidate_author len:",len(candidate_author))
