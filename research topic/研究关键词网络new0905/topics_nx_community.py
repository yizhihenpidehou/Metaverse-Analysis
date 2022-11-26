#!/usr/bin/python3
# -*- coding: UTF-8 -*-
#根据文献主题分析主题之间关联度网络图
import networkx as nx
from networkx.algorithms import bipartite
import matplotlib.pylab as plt
from matplotlib import font_manager as fm
from  matplotlib import cm
import numpy as np
import json
from pywaffle import Waffle
from networkx.algorithms import community
    
fig, ax = plt.subplots(figsize=(12, 9))

with open('new_second_filtered_dataset_withtopics3.json','r') as ww:

    splist = [".","'"]
    str=ww.read()

    lst=str.split('---------------------------------\n')

    #print(lst)
    topic1 = {'social network': '203', 'social network analysis': '53', 'data mining': '41', 'human-computer interaction': '38', 'semantic web': '28', 'machine learning': '19', 'world wide web': '17', 'social networking sites': '17', 'artificial intelligence': '15', 'online social networks': '14', 'information systems': '13', 'computer science': '12', 'online social networking': '11', 'collective intelligence': '10'}
    topic2 ={'social networks': '2123', 'online social networks': '967', 'social media': '771', 'social networking sites': '392', 'social networking services': '213', 'social network analysis': '186', 'mobile social networks': '159', 'social web': '64', 'data mining': '63', 'human-computer interaction': '60', 'social media sites': '57', 'recommender systems': '54', 'social network data': '54', 'machine learning': '53', 'online social media': '51', 'location-based social networks': '50', 'social media platforms': '50', 'mobile devices': '49', 'social computing': '44', 'social media data': '43', 'world wide web': '40', 'collective intelligence': '39', 'sina weibo': '36', 'social media services': '35', 'natural language processing': '32', 'semantic web': '32', 'social networking applications': '31', 'twitter users': '27', 'community detection': '26', 'amazon mechanical turk': '25', 'computer science': '25', 'influence maximization': '25', 'social capital': '25', 'social interactions': '24', 'big data': '24'}
    topic3 = {'social networks': '2884', 'social media': '2487', 'online social networks': '1359', 'social media platforms': '346', 'machine learning': '307', 'social networking sites': '301', 'mobile social networks': '251', 'artificial intelligence': '240', 'social network analysis': '226', 'social networking services': '211', 'social media data': '178', 'big data': '158', 'online social media': '153', 'natural language processing': '153', 'human-computer interaction': '151', 'location-based social networks': '145', 'sentiment analysis': '127', 'influence maximization': '125', 'data mining': '111', 'mobile devices': '103', 'social media users': '90', 'community detection': '89', 'spatial crowdsourcing': '88', 'emotion recognition': '85', 'fake news': '84', 'recommender systems': '83', 'social internet': '69', 'social media sites': '69', 'covid-19 pandemic': '67', 'twitter users': '67', 'support vector machine': '66', 'twitter data': '60', 'deep learning': '57', 'mobile crowdsourcing': '54'}


    nodelist1 = topic3.keys()
    
    nodelist2 = []


    # 创建空的网格
    G=nx.Graph()
    # 添加节点
    G.add_nodes_from(nodelist1, bipartite=0)
    G.add_nodes_from(nodelist2, bipartite=1)
    
    for i in range(0,len(lst)-1):
        print(i)
        article =json.loads(lst[i])
        print(article['topic'])
        topic = article['topic']
        date = article['date']
        
#        if not (int(date) >=1994 and int(date) <2022):
#            print('invalid year:'+date)
#            continue
        
        if len(topic) != 0:
            cp = ['','']
            for j in topic:
                cp[0] = j
                for k in topic:
                    if k != j:
                        cp[1] = k
                        if G.has_edge(cp[0],cp[1]):
                            G[cp[0]][cp[1]]['weight']+=1
                        else:
                            G.add_edge(cp[0],cp[1],weight = 1)
 
                        print()
 
        nodedegrees = {}

        for n in G.nodes():
            if n not in nodedegrees.keys():
                nodedegrees.setdefault(n, 0)
            nodedegrees[n] = G.degree(n)
        
        print('degree')
        print(sorted(nodedegrees.items(), key=lambda x: x[1], reverse=True))



    node_label = nx.get_node_attributes(G, 'desc')



    #分成两组点，分别画图
    sizes1 = []
    sizes2 = []

#节点大小根据effective size来调整
    for v in G.nodes():
        if v in nodelist1:
            sizes1.append(180*(nx.effective_size(G)[v]))
        elif v in nodelist2:
            sizes2.append(250*(nx.effective_size(G)[v]))

    print(sizes1)
    print(sizes2)

    pos = nx.spring_layout(G)
#    #pos = dict()
#    pos.update( (n, (1, i)) for i, n in enumerate(nodelist1) )
#    pos.update( (n, (2, i)) for i, n in enumerate(nodelist2) )

##自定义位置
#    pos = {'AI': ([-1,0.04]), 'Algorithms & Theory': ([-0.85,0.42]), 'Software & Application': ([-0.13,0.1]), 'Graph': ([-0.22,0.54]), 'Hardware': ([-0.527,0.736]), 'System & Architecture': ([-0.87,-0.33]), 'Networks': ([-0.402,-0.418]), 'Policy': ([0.3,-0.4]), 'Psychology': ([1.35,0.3]),'Social Issue': ([0.422,0.818]), 'Education': ([0.776,0.893]), 'Health': ([1.06,0.68]), 'Business': ([0.205,0.495]), 'Language & Arts': ([1.24,-0.31]), 'History & Theory': ([0.78,-0.666]), 'Religion': ([1.03,-0.5]), 'Urban & Rural development': ([0.19,0.009])}
    
    nx.draw_networkx_nodes(G,pos,nodelist=nodelist1,label=node_label.items(),node_size=sizes1,node_color = 'sandybrown',edgecolors='gray')

    nx.draw_networkx_nodes(G,pos,nodelist=nodelist2,label=node_label.items(),node_size=sizes2)

    for e in G.edges():
        ewidth = G[e[0]][e[1]]['weight']
        print(e)
        print(ewidth)
        if (e[0] in nodelist1 and e[1] in nodelist1) or (e[0] in nodelist2 and e[1] in nodelist2):
            nx.draw_networkx_edges(G,pos,edgelist=[e],width=ewidth/10,edge_color='tan')
        else:
            nx.draw_networkx_edges(G,pos,edgelist=[e],width=ewidth/15,edge_color='skyblue')
            
    nx.draw_networkx_labels(G, pos,font_size=8,font_family='sans-serif')



    for n in G.nodes():
        print((n))
        print(G.degree(n))


    nodedegrees = {}

    for n in G.nodes():
        if n not in nodedegrees.keys():
            nodedegrees.setdefault(n, 0)
        nodedegrees[n] = G.degree(n)
        

    #结构洞数据
#    print('constraint')
#    print(sorted((nx.constraint(G)).items(), key=lambda x: x[1]))
#
#    print('effective_size')
#    print(sorted((nx.effective_size(G)).items(), key=lambda x: x[1], reverse=True))


    nodedegrees = {}

#     for n in G.nodes():
#         if n not in nodedegrees.keys():
#             nodedegrees.setdefault(n, 0)
#         nodedegrees[n] = G.degree(n)
    
#     print('degree')
#     print(sorted(nodedegrees.items(), key=lambda x: x[1], reverse=True))

# #展示边的权重，只考虑交叉
#     edgewiths = {}
#     for n in G.edges():
#         if n not in edgewiths.keys():
#             edgewiths.setdefault(n, 0)
#         edgewiths[n] = G[n[0]][n[1]]['weight']

#         if G[n[0]][n[1]]['weight'] <15:
#             G.remove_edge(n[0],n[1])



#     print('edgewiths')
#     print(sorted(edgewiths.items(), key=lambda x: x[1], reverse=True))

    print('community:')
    


    communities_generator = community.girvan_newman(G)
    top_level_communities = next(communities_generator)
    next_level_communities = next(communities_generator)
    next2_level_communities = next(communities_generator)
    next3_level_communities = next(communities_generator)
    print(sorted(map(sorted, top_level_communities)))
    print(sorted(map(sorted, next_level_communities)))
    print(sorted(map(sorted, next2_level_communities)))
    print(sorted(map(sorted, next3_level_communities)))


    #nx.draw(G,pos=nx.circular_layout(G),with_labels=True)
    # plt.show()
