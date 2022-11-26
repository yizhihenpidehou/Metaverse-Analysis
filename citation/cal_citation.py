import json
from collections import defaultdict
import matplotlib.pyplot as plt

# 计算团队混合情况与citation的关系，横坐标是团队大小，纵坐标是这类团队拥有citation占前5%的论文数量
def team_mix_citation(lst):
    citation_lst=[]
    mix_team_size_dict = defaultdict(int)
    same_team_size_dict=defaultdict(int)
    for i in range(0,len(lst)-1):
        json_str=json.loads(lst[i])
        citation=json_str["citation"]
        gender=json_str["gender"]
        mix_flag=0
        if 0 in gender and 1 in gender:
            mix_flag=1
        team_size=len(gender)
        title=json_str["title"]
        citation_lst.append((title,citation,team_size,mix_flag))
    citation_lst_len=len(citation_lst)
    citation_lst=sorted(citation_lst,key=lambda x:x[1],reverse=True)
    num=int(0.1*citation_lst_len)
    print("top 10%:",num)
    for i in range(0,num+1):
        print("citation_lst[i]:",citation_lst[i])
        if citation_lst[i][2] >=6 and citation_lst[i][3] == 1:
            mix_team_size_dict[6]+=1
        elif citation_lst[i][2] <6 and citation_lst[i][3] == 1:
            mix_team_size_dict[citation_lst[i][2]]+=1
        elif citation_lst[i][2] >=6 and citation_lst[i][3] == 0:
            same_team_size_dict[6]+=1
        elif citation_lst[i][2] <6 and citation_lst[i][3] == 0:
            same_team_size_dict[citation_lst[i][2]]+=1

    mix_team_num_lst=[]
    same_team_num_lst = []
    for i in range(1,7):
        mix_team_num_lst.append(mix_team_size_dict[i])
        same_team_num_lst.append(same_team_size_dict[i])

    plt.plot(range(1,7),mix_team_num_lst,color='red',linestyle="dotted",linewidth=3,label="Mixed GenderTeam")
    plt.plot(range(1, 7), same_team_num_lst, color='black', linestyle="dashed",linewidth=3,label="Same Gender Team")
    plt.legend()
    plt.savefig("teamsize_impactful_paper.png")
    plt.show()

def top_paper_citation(lst):
    top_paper_citation_lst=[]
    total_citation=0
    for i in range(0,len(lst)-1):
        json_str=json.loads(lst[i])
        citation=json_str["citation"]
        title=json_str["title"]
        top_paper_citation_lst.append((title,citation))
        total_citation+=citation

    top_paper_citation_lst=sorted(top_paper_citation_lst,key=lambda x:x[1],reverse=True)
    top_paper_citation_lst_len=int(0.1*len(top_paper_citation_lst))
    print("top_paper_citation_lst_len:",top_paper_citation_lst_len)
    top_citation=0
    for i in range(0,top_paper_citation_lst_len):
        print("top_paper_citation_lst[i]:",top_paper_citation_lst[i])
        top_citation+=top_paper_citation_lst[i][1]
    print("occupy:",top_citation/total_citation*100)

# 计算某个作者的citation
def author_citation(lst):
    author_citation_dict=defaultdict(int)
    for i in range(0,len(lst)-1):
        json_str=json.loads(lst[i])
        citation=json_str["citation"]
        author_lst=json_str["author"]
        for author in author_lst:
            author_citation_dict[author]+=citation
    return author_citation_dict
    # author_citation_lst=sorted(author_citation_dict.items(),key=lambda x:x[1],reverse=True)
    # top_num=int(0.1*len(author_citation_lst))
    # for i in range(0,top_num+1):
    #     print("top_author:",author_citation_lst[i])


# 统计出版社的citation
def publisher_cal(lst):
    publisher_citation_dict=defaultdict(int)
    publisher_article_dict= {}
    for i in range(0,len(lst)-1):
        json_str=json.loads(lst[i])
        publisher=json_str["publish"]
        citation=json_str["citation"]
        publisher_citation_dict[publisher]+=citation
        if publisher not in publisher_article_dict.keys():
            publisher_article_dict[publisher]=[]
        publisher_article_dict[publisher].append(json_str)

    top_publisher=sorted(publisher_citation_dict.items(),key=lambda x:x[1],reverse=True)[:10]
    print("top_publisher:",top_publisher)
    yearly_citation_dict=defaultdict(int)
    for publisher in top_publisher:
        yearly_citation_dict[publisher[0]]=defaultdict(int)
        for article in publisher_article_dict[publisher[0]]:
            date=article["date"]
            citation=article["citation"]
            yearly_citation_dict[publisher[0]][int(date)]+=citation
    # print("yearly_citation_dict:",yearly_citation_dict)

    #计算每个出版社平均citation
    avg_citation_foreach_publisher_lst=[]
    for k,v in publisher_citation_dict.items():
        # print("publisher:",k," avg_citation:",v/len(publisher_article_dict[k]))
        publisher_key=k
        publisher_avg_citation_tuple=(publisher_key),v/len(publisher_article_dict[k]),len(publisher_article_dict[k])
        avg_citation_foreach_publisher_lst.append(publisher_avg_citation_tuple)
    print("avg_citation_foreach_publisher_lst:",sorted(avg_citation_foreach_publisher_lst,key=lambda x:x[1],reverse=True)[:10])
    key_lst=[]
    plt_lst=[]
    for key,value in yearly_citation_dict.items():
        citation_lst=[]
        label_lst=[]
        for j in range(2000,2023):
            if j not in value:
                value[j]=0
            citation_lst.append(value[j])
            label_lst.append(value[j])
            # print("year:",j,"publisher:",key,"citation:",value[j])
        # l后面必须加 , 因为plot返回的也是一个list，需要解构
        l,=plt.plot(range(2000,2023),citation_lst)
        plt_lst.append(l)
        key_lst.append(key)

    plt.xlabel('Year')
    plt.ylabel('Citation')
    plt.legend(handles=plt_lst, labels=key_lst, loc='best')
    plt.savefig("citation_change.png")
    plt.show()
    return top_publisher,avg_citation_foreach_publisher_lst
# def draw_publisher_citation_change(top_publisher):

def citation_distribution(lst,graphpath):
    weight_distribution = defaultdict(int)
    citation_lst = []
    for i in range(0, len(lst) - 1):
        json_str = json.loads(lst[i])
        citated_num = json_str["citation"]
        weight_distribution[citated_num] += 1
        citation_lst.append(citated_num)
    print("weight_distri:", sorted(weight_distribution.items(), key=lambda x: x[0], reverse=True))
    # density:是否归一化处理，默认为false
    n, bins, patches = plt.hist(citation_lst, bins=5, color="orange")
    # print("数字分布:", n)
    # print("间隔划分:", bins)
    for i in range(len(n)):
        plt.text((bins[i] + bins[i + 1]) / 2, n[i], int(n[i]), color='black', fontsize=16,
                 horizontalalignment="center")
    if graphpath:
        plt.savefig(graphpath)
    plt.show()

def citation_analysis_pipeline(inputpath,graphpath):
    file_path = inputpath
    ff = open(file_path,'r')
    ff_str=ff.read()
    lst=ff_str.split('---------------------------------\n')
    print("len:",len(lst)-1)
    citation_lst=[]
    for i in range(0,len(lst)-1):
        json_str=json.loads(lst[i])
        citation_num=json_str["citation"]
        citation_lst.append(citation_num)
    top_publisher,avg_citation_foreach_publisher_lst=publisher_cal(lst)
    author_citation(lst)
    print("top10:", top_publisher)
    citation_distribution(lst,graphpath)
    team_mix_citation(lst)
    top_paper_citation(lst)
    ff.close()
    return top_publisher,citation_lst,avg_citation_foreach_publisher_lst
# citation_analysis_pipeline("../2022-11/fourpublisher_arxiv_withsource_updatedauthor_citation2022-11_final.json",None)
