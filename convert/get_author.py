import json

def authors2list(firstfilter_path,output_path):
    print("author2list start!")
    # 打开初筛合并的文件
    ff = open(firstfilter_path, "r")

    ff_str = ff.read()
    lst = ff_str.split("---------------------------------\n")


    resfile = open(output_path, 'w')

    # 将初筛合并文件中所有文章的作者合成一个list，作为后续查询
    for i in range(0, len(lst) - 1):
        json_dict={}
        title = lst[i].split("title:")[1].split("\n")[0]
        link=lst[i].split('ee:')[1].split('\n')[0]
        if len(lst[i].split('journal:'))<2:
            publisher = lst[i].split('booktitle:')[1].split('\n')[0]
        else:
            publisher = lst[i].split('journal:')[1].split('\n')[0]
        date=lst[i].split('Year:')[1].split('\n')[0]
        source=lst[i].split('source:')[1].split('\n')[0]
        author = lst[i].split("title:")[0]
        tmp = author.split("author:")
        author_lst = []
        for j in range(1, len(tmp)):
            author_lst.append(tmp[j].split("\n")[0])
        # 若当前文章没有作者则省略
        if len(author_lst) > 0:
            json_dict["title"]=title
            json_dict['date']=date
            json_dict['link']=link
            json_dict['source']=source
            json_dict['publish']=publisher
            json_dict['author']=author_lst
            resfile.write(json.dumps(json_dict)+'\n')
            resfile.write('---------------------------------\n')

    ff.close()
    resfile.close()
    print("author2list finished!")
    return output_path
# authors2list('../publisher_divide/first_filtered_all_withsource.txt', 'first_filtered_all_withsource_updatedauthor.json')
def initial_authors2list():
    ff=open("../firstFilter/11月新增爬取数据.txt", "r")

    ff_str=ff.read()
    lst=ff_str.split("---------------------------------\n")

    tarfile=open("../crawlers/11新增/arxiv_res.json", 'r')
    tarfile_str=tarfile.read()
    tar_lst=tarfile_str.split("---------------------------------\n")


    author_dict={}
    print("initial:",len(tar_lst)-1)
    for i in range(0,len(lst)-1):
        title=lst[i].split("title:")[1].split("\n")[0]
        # print("title:",title)
        author=lst[i].split("title:")[0]
        tmp=author.split("author:")
        author_lst=[]
        for j in range(1,len(tmp)):
            author_lst.append(tmp[j].split("\n")[0])
        author_dict[title.lower().strip()]=author_lst

    res_f=open("../firstFilter/11月_arxiv_crawl_result_updateauthors_final.json", 'w')
    count=0
    for i in range(0,len(tar_lst)-1):
        tar_json=json.loads(tar_lst[i])
        title=tar_json["title"]
        for k in author_dict.keys():
            if title.lower().strip() in k:
                tar_json["author"]=author_dict[title.lower().strip()]
                count+=1
                res_f.write(json.dumps(tar_json) + '\n')
                res_f.write("---------------------------------\n")
                break



    print("count:",count)
    ff.close()
    tarfile.close()
    res_f.close()