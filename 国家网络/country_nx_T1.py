# #!/usr/bin/python3
# # -*- coding: UTF-8 -*-
# #根据文献主题分析主题之间关联度网络图
# import networkx as nx
# import matplotlib.pylab as plt
# from matplotlib import font_manager as fm
# from  matplotlib import cm
# import numpy as np
# from numpy import *
# import json
# # from pywaffle import Waffle
# import random
# from matplotlib import colors as mcolors
# import sys
#
#
# def random_color():
#     colorArr = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
#     color = ""
#     for i in range(6):
#         color += colorArr[random.randint(0, 14)]
#     return "#" + color
#
#
# errorlst = ['n','c','not found','']
#
# colors1 = []
# colors2 = []
#
#
#
#
# year_lst=[(1993,2008),(2008,2014),(2014,2021)]
#
#
# with open('../dblp_final_dataset.json','r') as ww:
#
#     splist = [".","'"]
#     js=ww.read()
#
#     lst=js.split('---------------------------------\n')
#
#     for year_tuple in year_lst:
#         # 创建空的网格
#         G=nx.Graph()
#         avg_degree=0
#         existcountries = []
#         for i in range(0,len(lst)-1):
#             try:
#                 print(i)
#                 article =json.loads(lst[i])
#                 print(article['country'])
#                 country = article['country']
#                 date = article['date']
#             except:
#                 print(lst[i])
#
#             else:
#                 pass
#
#             if not (int(date) >year_tuple[0] and int(date) <=year_tuple[1]):
#                 print('invalid year:'+date)
#                 continue
#
#             if len(country) != 0:
#                 cp = ['','']
#                 for i in range(0,len(country)):
#                 # for j in country:
#                 #     j = j.upper()
#                     certain_country=country[i].upper()
#                     if certain_country.lower() not in errorlst:
#                         if certain_country not in existcountries:
#                             existcountries.append(certain_country)
#                         G.add_node(certain_country)
#                         cp[0] = certain_country
#                         for j in range(i,len(country)):
#                             another_country=country[j].upper()
#                             # k = k.upper()
#                             if another_country != certain_country and (another_country.lower() not in errorlst):
#
#                                 if certain_country not in existcountries:
#                                     existcountries.append(another_country)
#                                 G.add_node(another_country)
#                                 cp[1] = another_country
#                                 if G.has_edge(cp[0],cp[1]):
#                                     G[cp[0]][cp[1]]['weight']+=1
#                                     avg_degree += 1
#                                 else:
#                                     G.add_edge(cp[0],cp[1],weight = 1)
#                                     avg_degree += 1
#
#
#         avg_degree=avg_degree*1.0/len(existcountries)
#         print("avg:",avg_degree)
#         labels2draw = {}
#
#         pos=nx.random_layout(G)
#
#         # pos = nx.drawing.nx_agraph.graphviz_layout(G)
#
#         mediumnodes = []
#         strongnodes = []
#         othernodes = []
#         allvalidnodes = []
#
#
#         for node in G.nodes():
#             if G.degree(node) >=1.2*avg_degree:
#                 strongnodes.append(node)
#                 allvalidnodes.append(node)
#                 labels2draw[node]=str(node)
#             elif 1.2*avg_degree> G.degree(node) >=1.0*avg_degree:
#                 mediumnodes.append(node)
#                 allvalidnodes.append(node)
#                 labels2draw[node]=str(node)
#             elif avg_degree> G.degree(node)>=0.5*avg_degree:
#                 othernodes.append(node)
#                 allvalidnodes.append(node)
#                 labels2draw[node]=str(node)
#
#
#
#         stronglabels = {}
#         mediumlabels = {}
#         weaklabels = {}
#
#
#
#         for node in G.nodes():
#             if node in strongnodes:
#                 #set the node name as the key and the label as its value
#                 stronglabels[node] = node
#
#             elif node in mediumnodes:
#                 mediumlabels[node] = node
#
#             elif node in othernodes:
#                 weaklabels[node] = node
#
#         nodesizes = []
#
#         for v in G.nodes():
#             nodesizes.append(20*G.degree(v))
#
#         nodesizesstrong = []
#         nodesizesmedium = []
#         nodesizesothers = []
#
#         for v in strongnodes:
#             nodesizesstrong.append(15*G.degree(v))
#
#         for v in mediumnodes:
#             nodesizesmedium.append(15*G.degree(v))
#
#         for v in othernodes:
#             nodesizesothers.append(15*G.degree(v))
#
#         for i in range(0, len(strongnodes)):
#             colors1.append(random_color())
#
#
#
#         # print('nodes:')
#         # print(G.nodes())
#
#         nx.draw_networkx_nodes(G,pos,nodelist=list(strongnodes),label=stronglabels.items(),node_size=nodesizesstrong,node_color = 'mediumpurple')
#
#         nx.draw_networkx_nodes(G,pos,nodelist=list(mediumnodes),label=mediumlabels.items(),node_size=nodesizesmedium,node_color = 'lightsteelblue')
#
#         nx.draw_networkx_nodes(G,pos,nodelist=list(othernodes),label=weaklabels.items(),node_size=nodesizesothers,node_color = 'thistle')
#
#         #nx.draw_networkx_nodes(G,pos,nodelist=list(validcountries-existcountries),label=node_label.items(),node_size=0,node_color = white)
#
#         for e in G.edges():
#             ewidth = G[e[0]][e[1]]['weight']
#             if e[0] in allvalidnodes and e[1] in allvalidnodes:
#         #    print(e)
#         #    print(ewidth)
#         #    if ewidth <5:
#         #        ewidth=0
#                 nx.draw_networkx_edges(G,pos,edgelist=[e],width=ewidth/avg_degree,edge_color='darkgray')
#
#         nx.draw_networkx_labels(G, pos, labels2draw, font_size=5,font_family='sans-serif')
#
#         #nx.draw(G,pos=nx.circular_layout(G),with_labels=True)
#
#
#         nodedegrees = {}
#
#         # for n in G.nodes():
#         #     if n not in nodedegrees.keys():
#         #         nodedegrees.setdefault(n, 0)
#         #     nodedegrees[n] = G.degree(n)
#
#
#         #结构洞数据
#         print('constraint')
#         print(sorted((nx.constraint(G)).items(), key=lambda x: x[1]))
#
#         print('effective_size')
#         print(sorted((nx.effective_size(G)).items(), key=lambda x: x[1], reverse=True))
#
#         print('degree')
#         print(sorted(nodedegrees.items(), key=lambda x: x[1], reverse=True))
#
#
#         # #展示边的权重，只考虑交叉
#         edgewiths = {}
#         for n in G.edges():
#          if n not in edgewiths.keys():
#              edgewiths.setdefault(n, 0)
#          edgewiths[n] = G[n[0]][n[1]]['weight']
#
#         print('edgewiths')
#         print(sorted(edgewiths.items(), key=lambda x: x[1], reverse=True))
#
#         #plt.title('2012-2021')
#         plt.show()


#!/usr/bin/python3
# -*- coding: UTF-8 -*-
#根据文献主题分析主题之间关联度网络图
import networkx as nx
import matplotlib.pylab as plt
from matplotlib import font_manager as fm
from  matplotlib import cm
import numpy as np
from numpy import *
import json
# from pywaffle import Waffle
import random
from matplotlib import colors as mcolors
import sys


def random_color():
    colorArr = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
    color = ""
    for i in range(6):
        color += colorArr[random.randint(0, 14)]
    return "#" + color


errorlst = ['n','c','not found','']






time_interval=[(0,0),(1999,2022)]

index=0
with open('../fourpublisher_crawl_citation_res.json', 'r') as ww:
    splist = [".", "'"]
    js = ww.read()

    lst = js.split('---------------------------------\n')

    # 创建空的网格

    for index in range(1,2):
        #index+=1
        G = nx.Graph()
        max_degree=0
        total_degree=0
        existcountries = []
        colors1 = []
        colors2 = []
        for i in range(0, len(lst) - 1):
            try:
                tmp_country=[]
                # print(i)
                article = json.loads(lst[i])
                # print(article['country'])
                country = article['country']
                date = article['date']
            except:
                print(lst[i])

            else:
                pass
            if not (int(date) > time_interval[index][0] and int(date) <= time_interval[index][1]):
                # print('invalid year:' + date)
                continue

            if len(country) != 0:
                cp = ['', '']
                for j in country:
                    j = j.upper()
                    if j.lower() not in errorlst:
                        if j not in existcountries:
                            existcountries.append(j)
                        G.add_node(j)
                        cp[0] = j
                        for k in country:
                            k = k.upper()
                            if k != j and (k.lower() not in errorlst):
                                if j not in existcountries:
                                    existcountries.append(k)
                                G.add_node(k)
                                cp[1] = k
                                if G.has_edge(cp[0], cp[1]) and (cp[0], cp[1]) not in tmp_country:
                                    G[cp[0]][cp[1]]['weight'] += 1

                                elif G.has_edge(cp[0], cp[1]) == False:
                                    G.add_edge(cp[0], cp[1], weight=1)
                                    tmp_country.append((cp[0], cp[1]))
                                    tmp_country.append((cp[1], cp[0]))

                                if max_degree<G[cp[0]][cp[1]]['weight']:
                                    max_degree=G[cp[0]][cp[1]]['weight']

        # print("interval:",interval,str(index),"max_degree:",max_degree)

        labels2draw = {}

        # pos = nx.spring_layout(G,k=50)
        pos=nx.random_layout(G)
        # pos=nx.circular_layout(G,scale=20)
        # pos=nx.kamada_kawai_layout(G)
        # pos = nx.drawing.nx_agraph.graphviz_layout(G)
        for node in G.nodes:
            total_degree+=G.degree(node)
        # print("total_degree:",total_degree)
        average_degree=total_degree/len(G.nodes)
        # print("interval:", interval, str(index), "avg_degree:", average_degree)
        mediumnodes = []
        strongnodes = []
        othernodes = []
        allvalidnodes = []
        degree_lst=G.degree()
        degree_lst=sorted(degree_lst,key=lambda x:x[1],reverse=True)
        for node in G.nodes:
            # print("degree:",G.degree(node))
            if G.degree(node) >= average_degree and len(strongnodes) <= 6:
                strongnodes.append(node)
                allvalidnodes.append(node)
                labels2draw[node] = str(node)
            elif average_degree > G.degree(node) >= 0.8*average_degree and len(mediumnodes) <= 6:
                mediumnodes.append(node)
                allvalidnodes.append(node)
                labels2draw[node] = str(node)
            elif 0.8*average_degree > G.degree(node) >= 0.2*average_degree and len(othernodes) <= 6:
                othernodes.append(node)
                allvalidnodes.append(node)
                labels2draw[node] = str(node)

        stronglabels = {}
        mediumlabels = {}
        weaklabels = {}

        for node in G.nodes:
            if node in strongnodes:
                # set the node name as the key and the label as its value
                stronglabels[node] = node

            elif node in mediumnodes:
                mediumlabels[node] = node

            elif node in othernodes:
                weaklabels[node] = node

        nodesizes = []

        for v in G.nodes():
            nodesizes.append(20 * G.degree(v))

        nodesizesstrong = []
        nodesizesmedium = []
        nodesizesothers = []

        for v in strongnodes:
            nodesizesstrong.append(60 * G.degree(v))

        for v in mediumnodes:
            nodesizesmedium.append(50* G.degree(v))

        for v in othernodes:
            nodesizesothers.append(40 * G.degree(v))

        for i in range(0, len(strongnodes)):
            colors1.append(random_color())

        # print('nodes:')
        # print(G.nodes())

        nx.draw_networkx_nodes(G, pos, nodelist=list(strongnodes), label=stronglabels.items(), node_size=nodesizesstrong,
                               node_color='mediumpurple')

        nx.draw_networkx_nodes(G, pos, nodelist=list(mediumnodes), label=mediumlabels.items(), node_size=nodesizesmedium,
                               node_color='lightsteelblue')

        nx.draw_networkx_nodes(G, pos, nodelist=list(othernodes), label=weaklabels.items(), node_size=nodesizesothers,
                               node_color='thistle')

        # nx.draw_networkx_nodes(G,pos,nodelist=list(validcountries-existcountries),label=node_label.items(),node_size=0,node_color = white)

        for e in G.edges():
            ewidth = G[e[0]][e[1]]['weight']
            if e[0] in allvalidnodes and e[1] in allvalidnodes:
                #    print(e)
                # print(ewidth)
                #    if ewidth <5:
                #        ewidth=0
                #stage1 /1.5
                #stage2 /
                #stage3 /
                nx.draw_networkx_edges(G, pos, edgelist=[e], width=ewidth / (average_degree*0.5), edge_color='darkgray')

        nx.draw_networkx_labels(G, pos, labels2draw, font_size=12, font_family='sans-serif')

        # nx.draw(G,pos=nx.circular_layout(G),with_labels=True)


        nodedegrees = {}

        # for n in G.nodes():
        #     if n not in nodedegrees.keys():
        #         nodedegrees.setdefault(n, 0)
        #     nodedegrees[n] = G.degree(n)


        # 结构洞数据
        # print('constraint')
        # print(sorted((nx.constraint(G)).items(), key=lambda x: x[1]))
        #
        print('effective_size')
        print(sorted((nx.effective_size(G)).items(), key=lambda x: x[1], reverse=True)[:11])
        #
        # print('degree')
        # print(sorted(nodedegrees.items(), key=lambda x: x[1], reverse=True))

        # #展示边的权重，只考虑交叉
        edgewiths = {}
        for n in G.edges():
            if n not in edgewiths.keys():
                edgewiths.setdefault(n, 0)
            edgewiths[n] = G[n[0]][n[1]]['weight']

        print('edgewiths')
        print(sorted(edgewiths.items(), key=lambda x: x[1], reverse=True)[:11])
        plt.rcParams['figure.figsize']=(6, 4.3)
        plt.savefig("country_stage"+str(index)+".png")
        # plt.title('2012-2021')
        plt.show()
