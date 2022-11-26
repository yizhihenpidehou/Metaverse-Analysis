import json
import math
import matplotlib.pyplot as plt
import networkx as nx
import easygraph as eg
from collections import defaultdict
from networkx.algorithms import community
from functools import cmp_to_key
#排序算法，优先按effective_size降序排序，然后按照citation进行降序排序
def custom_sorted(x,y):
    if x[1]["effective_size"]>y[1]["effective_size"]:
        return 1
    elif x[1]["effective_size"]<y[1]["effective_size"]:
        return -1
    else:
        if  x[1]["citation"] > y[1]["citation"]:
            return 1
        elif x[1]["citation"] < y[1]["citation"]:
            return -1
        else:
            return 0
def team_citation(lst):
    team_size_dict={}
    team_size_paper_dict=defaultdict(int)
    for i in range(0,len(lst)-1):
        json_str = json.loads(lst[i])
        citation = json_str["citation"]
        author_lst = json_str["author"]
        team_size=len(author_lst)
        if team_size not in team_size_dict.keys():
            team_size_dict[team_size]={}

        if "citation" not in team_size_dict[team_size].keys():
            team_size_dict[team_size]["citation"]=0
        if "paper_num" not in team_size_dict[team_size].keys():
            team_size_dict[team_size]["paper_num"] = 0
        team_size_dict[team_size]["citation"]+=citation
        team_size_dict[team_size]["paper_num"]+=1
    team_avg_size_dict={}
    for k,v in team_size_dict.items():
        # print(k,v)
        if k==0:
            team_size_dict[k]["avg_citation"]=v["citation"]
        else:
            team_size_dict[k]["avg_citation"]=v["citation"]/v["paper_num"]
    return team_avg_size_dict,team_size_dict
#返回每个作者的citation
def author_citation(lst):
    author_citation_dict=defaultdict(int)
    author_publish= {}
    for i in range(0,len(lst)-1):
        json_str=json.loads(lst[i])
        citation=json_str["citation"]
        author_lst=json_str["author"]
        for author in author_lst:
            author_citation_dict[author]+=citation
            if author not in author_publish:
                author_publish[author]=1
            else:
                author_publish[author]+=1
    author_avg_citation={}
    for k in author_publish.keys():
        author_avg_citation[k]={}
        author_avg_citation[k]["avg_citation"]=author_citation_dict[k]/author_publish[k]
        author_avg_citation[k]["paper_num"] = author_publish[k]
        # print(k,author_avg_citation[k],author_publish[k])
    # print(sorted(author_avg_citation.items(),key=lambda x:x[1]["avg_citation"],reverse=True))
    return author_citation_dict,author_avg_citation
#作者citation权重分布
def author_weight_distribution(G):
    # print("edges:",nx.get_edge_attributes(G,name="weight"))
    edge_attr=nx.get_edge_attributes(G,name="weight")
    wd=defaultdict(int)
    for k,v in edge_attr.items():
        wd[v]+=1

    return sorted(wd.items(),key=lambda x:x[0],reverse=True)


def author_effective_size(G):
    effective_size_res = nx.effective_size(G)
    for effective_size in effective_size_res.items():
        if math.isnan(effective_size[1]):
            effective_size_res[effective_size[0]] = 0
    return effective_size_res

def author_generate_graph(file_path):
    author_sum = set()
    author_num = 0
    with open(file_path, 'r') as ww:
        ww_str = ww.read()
        lst = ww_str.split('---------------------------------\n')
        G = nx.Graph()
        for i in range(0, len(lst) - 1):
            # print(i,lst[i])
            json_str = json.loads(lst[i])
            author_lst = json_str["author"]
            author_num += len(author_lst)
            for author in author_lst:
                author_sum.update(author)
                if G.has_node(author) == False:
                    G.add_node(author)
            for j in range(0, len(author_lst)):
                for z in range(j + 1, len(author_lst)):
                    if G.has_edge(author_lst[j], author_lst[z]) == False:
                        G.add_edge(author_lst[j], author_lst[z], weight=1)
                    else:
                        G[author_lst[j]][author_lst[z]]["weight"] += 1
    ww.close()
    return G

def author_HIS(file_path,G_nx):
    author_num = 0
    author_sum=set()
    with open(file_path, 'r') as ww:
        ww_str = ww.read()
        lst = ww_str.split('---------------------------------\n')
        G = eg.Graph()
        for i in range(0, len(lst) - 1):
            # print(i,lst[i])
            json_str = json.loads(lst[i])
            author_lst = json_str["author"]
            author_num += len(author_lst)
            for author in author_lst:
                author_sum.update(author)
                if G.has_node(author) == False:
                    G.add_node(author)
            for j in range(0, len(author_lst)):
                for z in range(j + 1, len(author_lst)):
                    if G.has_edge(author_lst[j], author_lst[z]) == False:
                        G.add_edge(author_lst[j], author_lst[z], weight=1)
                    else:
                        G[author_lst[j]][author_lst[z]]["weight"] += 1
    ww.close()


    res=eg.ICC(G,5)
    res2=eg.AP_Greedy(G,5)
    print("res2:",res2)
    return res

def author_community(G):
    return list(community.girvan_newman(G))

def author_draw_graph(G,res_path,threshold=2):
    effective_size_res = author_effective_size(G)
    fig = plt.figure()
    fig.set_figheight(15)
    fig.set_figwidth(15)
    pos = nx.random_layout(G)
    node_count = 0
    node_size = []
    label2draw = {}
    avaliable_node = []
    for v in G.nodes():
        if effective_size_res[v]>=threshold and node_count<20:
            node_size.append(250 * (effective_size_res[v]))
            label2draw[v]=str(v)
            avaliable_node.append(v)
            node_count+=1
    nx.draw_networkx_nodes(G, pos, nodelist=avaliable_node, node_size=node_size,
                                   node_color='mediumpurple')
    nx.draw_networkx_labels(G,pos,labels=label2draw, font_size=12, font_family='sans-serif')
    for e in G.edges():
        if e[0] in avaliable_node and e[1] in avaliable_node:
            ewidth = G[e[0]][e[1]]['weight']
            nx.draw_networkx_edges(G, pos, edgelist=[e], width=ewidth*2, edge_color='darkgray')
    if res_path!=None:
        plt.savefig(res_path+".png")
    plt.show()


def cal_author_citation_perform(author_citation_dict,effective_size_res):
    author_citation_perform = {}
    for a1, cita in author_citation_dict.items():
        for a2, eff in effective_size_res.items():
            if a1 == a2:
                author_citation_perform[a1] = {}
                author_citation_perform[a1]["citation"] = cita
                author_citation_perform[a1]["effective_size"] = eff
                break
    ww=open("corr.txt",'w')
    for k,v in author_citation_perform.items():
        print('k:',k,' v:',v)

        ww.write(str(v['effective_size'])+'\n')

    ww.close()
    return author_citation_perform

#
def author_analysis_pipeline(inputpath,graphpath=None):
    res_dict={}
    file_path = inputpath
    file=open(file_path,'r')
    file_str=file.read()
    lst=file_str.split("---------------------------------\n")
    file.close()
    G = author_generate_graph(file_path=inputpath)
    # author_draw_graph(G,res_path=graphpath,threshold=5)
    # 图的结点、边数量
    print("node:", len(G.nodes), "edges:", len(G.edges))


    # 聚类系数
    cluster_coefficient=nx.average_clustering(G)
    print("cluster_coefficient:",cluster_coefficient)
    # 度中心性
    # centrality = nx.degree_centrality(G)
    # print("centrality:", sorted(centrality.items(), key=lambda x: x[1], reverse=True)[:10])
    # 图的边权分布情况
    print("weight distribution", author_weight_distribution(G))
    # 计算effective size
    effective_size_res = author_effective_size(G)
    print("effective_size:", sorted(effective_size_res.items(), key=lambda x: x[1], reverse=True)[0:10])
    # 作者引用的情况
    author_citation_dict,author_avg_citation=author_citation(lst)
    # print("author_citation_dict:",sorted(author_citation_dict.items(),key=lambda x:x[1],reverse=True)[:10])
    # print("author_avg_citation:",sorted(author_avg_citation.items(),key=lambda x:x[1]["avg_citation"],reverse=True)[:10])
    # 计算作者引用与作者影响力的对比
    author_citation_perform=cal_author_citation_perform(author_citation_dict,effective_size_res)
    print("author_citation_perform：",sorted(author_citation_perform.items(),key=cmp_to_key(custom_sorted),reverse=True)[:10])
    # 计算团队大小与平均citation的关系
    # team_size_avg_citation,team_size_dict=team_citation(lst)
    # print("team_size_avg_citation:",sorted(team_size_avg_citation.items(),key=lambda x:x[1],reverse=True))
    # print("team_size_dict:",team_size_dict)
    # print("team_size_dict:",sorted(team_size_dict.items(),key=lambda x:x[1]["avg_citation"],reverse=True))
    # 计算connected components ,找LCC（largest connected component)
    connected_component = sorted(nx.connected_components(G), key=len, reverse=True)
    # print("LCC:", connected_component[0], len(connected_component[0]))
    LCC_size=len(connected_component[0])
    # density=nx.density(G)
    # print("density:",nx.density(G))
    # bridge_num=len(list(nx.bridges(G)))
    # print("has_brige:",nx.has_bridges(G),len(list(nx.bridges(G))))
    # print("bridges:",list(nx.bridges(G)))
    # HIS
    # HIS_res=author_HIS(inputpath,G)
    # print("HIS:",HIS_res)
    #结果存储
    # res_dict["HIS"]=HIS_res
    res_dict["effective_size_res"]=effective_size_res
    res_dict["LCC_size"]=LCC_size
    res_dict["nodes"]=len(G.nodes)
    res_dict["edges"]=len(G.edges)
    print("nodes:",res_dict["nodes"]," edges:",res_dict["edges"])
    # res_dict["density"]=density
    # res_dict["bridge_num"]=bridge_num
    # res_dict["centrality"]=centrality
    res_dict["cluster_coefficient"]=cluster_coefficient
    # res_dict["author_citation_perform"]=author_citation_perform
    return res_dict
author_analysis_pipeline("../2022-11/fourpublisher_arxiv_withsource_updatedauthor_citation2022-11_final.json",                         "author_collaboration")