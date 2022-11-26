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

fig, ax = plt.subplots(figsize=(9, 7))

# topic1 = {'social network': '111', 'social network analysis': '57', 'human-computer interaction': '39', 'social networking': '32', 'semantic web': '28', 'machine learning': '23', 'network analysis': '23', 'recent years': '18', 'world wide web': '16', 'social networking sites': '16', 'artificial intelligence': '15', 'online social networks': '14', 'computer science': '13', 'online social networking': '12', 'online social': '12', 'knowledge discovery': '12', 'world wide': '12', 'machine learning techniques': '12', 'collective intelligence': '12', 'wide web': '10', 'system dynamics': '10'}
# topic2 = {'social media': '843', 'social network': '807', 'social networking': '353', 'social networking sites': '256', 'social network analysis': '192', 'online social network': '151',  'social networking services': '105', 'mobile social networks': '100', 'social network services': '83', 'network analysis': '72', 'human-computer interaction': '68', 'social web': '63', 'machine learning': '60', 'recommender systems': '58', 'social media sites': '57', 'network sites': '55', 'mobile devices': '53', 'location-based social networks': '52', 'online social media': '52', 'mobile social': '51', 'networking services': '51', 'social media platforms': '49', 'social computing': '47', 'rapid growth': '46', 'important role': '46', 'collective intelligence': '41', 'rapid development': '41', 'mobile social network': '40', 'world wide web': '40', 'sina weibo': '38', 'increasing popularity': '38', 'social networking site': '37', 'social networking service': '36', 'social media services': '36', 'semantic web': '36', 'like facebook': '36', 'location-based social': '35', 'network services': '34', 'natural language processing': '33', 'becoming increasingly': '32', 'social networking applications': '32', 'social networking websites': '32', 'world wide': '31', 'web services': '30', 'social network service': '30', 'community detection': '29', 'wide web': '29', 'united states': '28', 'social interactions': '28', 'influence maximization': '28', 'last decade': '27', 'social capital': '27', 'mobile social networking': '26', 'last years': '26', 'increasingly popular': '26', 'collaborative filtering': '25', 'social media websites': '25', 'increasingly important': '25', 'social network site': '25', 'social behavior': '25', 'computer science': '24', 'viral marketing': '23', 'on-line social networks': '23', 'social media applications': '23', 'amazon mechanical turk': '23', 'becoming increasingly popular': '23', 'link prediction': '23', 'wide range': '23', 'real world': '22', 'daily life': '22', 'networking websites': '21', 'social influence': '21', 'decision making': '21', 'media sites': '21', 'networking service': '20', 'social networking platforms': '20', 'social interaction': '20', 'delay tolerant networks': '20', 'popular social': '20'}


pair1 = [['social network', 'network analysis'], 

['machine learning', 'machine learning techniques'], 

['social network', 'online social networks'], 

['social network', 'semantic web'], 

['social network', 'computer science'], 

['social network', 'world wide web'], 

['machine learning', 'artificial intelligence'], 

['semantic web', 'machine learning'], 

['machine learning', 'knowledge discovery'],

['social network', 'artificial intelligence'], 

['human-computer interaction', 'machine learning'],

['human-computer interaction', 'artificial intelligence'],

['semantic web', 'world wide web'],

['machine learning', 'computer science'],

['artificial intelligence', 'computer science']]


pair2 = [['social media', 'social network'], 

 ['social network', 'social interaction'],

['social network', 'networking service'], 

 ['social network', 'mobile devices'], 

 ['social network', 'network sites'], 

 ['social network', 'recommender systems'],  

['social network', 'social influence'], 

['social network', 'community detection'],  

['social network', 'collaborative filtering'],

 ['social network', 'machine learning'],

 ['social network', 'social behavior'], 

['social network', 'viral marketing'], 

['social network', 'link prediction'], 

 ['social network', 'influence maximization']]


pair3 = [['social media', 'social networks'], ['social media', 'machine learning'], ['social media', 'semantic analysis'], ['social media', 'twitter data'], ['machine learning', 'deep learning'], ['machine learning', 'support vector machine'], ['social media', 'mobile social networks'], ['social networks', 'machine learning'], ['social media', 'community detection'], ['social networks', 'influence maximization'],  ['machine learning', 'artificial intelligence'], ['social media', 'deep learning'], ['social media', 'big data'], ['social networks', 'location-based social networks'], ['social media', 'natural language processing']]

topic1 = ['social networks',  'human-computer interaction', 'semantic web', 'machine learning', 'network analysis', 'world wide web', 'social networking sites', 'artificial intelligence', 'online social networks', 'computer science', 'knowledge discovery',  'machine learning techniques', 'collective intelligence', 'system dynamics']
topic2 =['social networks', 'social media', 'online social networks', 'social networking sites', 'social network analysis', 'social network sites', 'mobile social networks', 'social network services', 'human-computer interaction', 'social web', 'machine learning', 'recommender systems', 'social media sites', 'network sites', 'mobile devices', 'location-based social networks', 'online social media', 'social media platforms', 'social computing', 'collective intelligence',  'world wide web', 'sina weibo',  'social media services', 'semantic web', 'like facebook', 'natural language processing', 'social networking applications', 'web services', 'community detection', 'social interactions', 'influence maximization', 'social capital', 'computer science', 'collaborative filtering',  'social behavior', 'viral marketing', 'amazon mechanical turk', 'link prediction', 'decision making']
topic3 = ['social media', 'social networks', 'online social networks', 'social media platforms', 'machine learning', 'artificial intelligence', 'social network analysis', 'mobile social networks', 'online social media', 'human-computer interaction', 'natural language processing', 'location-based social networks', 'sentiment analysis', 'influence maximization', 'mobile devices', 'media platforms', 'social network services', 'recommender systems', 'community detection', 'spatial crowdsourcing', 'emotion recognition', 'fake news', 'support vector machine', 'social media sites', 'social internet', 'viral marketing', 'deep learning', 'mobile crowdsourcing', 'link prediction', 'covid-19 pandemic', 'social influence', 'like twitter', 'sina weibo', 'social media content', 'decision making', 'autism spectrum disorder', 'machine learning techniques', 'latent dirichlet allocation', 'computer science', 'convolutional neural network', 'collective intelligence', 'event detection', 'communication technologies', 'neural network', 'event-based social networks']


with open('new_second_filtered_dataset_withtopics3.json','r') as ww:

    splist = [".","'"]
    str=ww.read()

    lst=str.split('---------------------------------\n')

    nodelistnew = []

    for tp in topic3:
        # for v in tp:
        nodelistnew.append(tp)

    # 创建空的网格
    G=nx.Graph()
    # 添加节点
    G.add_nodes_from(nodelistnew)

    print(nodelistnew)


    for i in range(0,len(lst)-1):
        article =json.loads(lst[i])
        topic = article['topic']
        date = article['date']
        
#        if not (int(date) >=1994 and int(date) <2022):
#            print('invalid year:'+date)
#            continue
        tmp_lst=[]
        if len(topic) != 0:
            cp = ['','']
            for j in topic:
                if j in nodelistnew:
                    cp[0] = j
                    for k in topic:
                        if k in nodelistnew:
                            if k != j:
                                cp[1] = k
                                if G.has_edge(cp[0],cp[1]) and (cp[0],cp[1]) not in tmp_lst:
                                    G[cp[0]][cp[1]]['weight']+=1
                                    tmp_lst.append((cp[0],cp[1]))
                                    tmp_lst.append((cp[1], cp[0]))
                                elif G.has_edge(cp[0],cp[1])==False:
                                    G.add_edge(cp[0],cp[1],weight = 1)
                                    tmp_lst.append((cp[0], cp[1]))
                                    tmp_lst.append((cp[1], cp[0]))
 
        nodedegrees = {}

        # for n in G.nodes():
        #     if n not in nodedegrees.keys():
        #         nodedegrees.setdefault(n, 0)
        #     nodedegrees[n] = G.degree(n)
        
        # print('degree')
        # print(sorted(nodedegrees.items(), key=lambda x: x[1], reverse=True]


    #分成两组点，分别画图
    sizes1 = []
    sizes2 = []

#节点大小根据effective size来调整
    # for v in G.nodes():

    for tp in topic3:
        sizes1.append(180*(nx.effective_size(G)[tp]))


    pos = nx.spring_layout(G)
    # print("size1:",len(sizes1))
    # print("pos1:", len(pos))
    # print("nodelist",len(nodelistnew))
#    #pos = dict()
#    pos.update( (n, (1, i] for i, n in enumerate(nodelist1) )
#    pos.update( (n, (2, i] for i, n in enumerate(nodelist2) )

##自定义位置
#    pos = {'AI': ([-1,0.04]), 'Algorithms & Theory': ([-0.85,0.42]), 'Software & Application': ([-0.13,0.1]), 'Graph': ([-0.22,0.54]), 'Hardware': ([-0.527,0.736]), 'System & Architecture': ([-0.87,-0.33]), 'Networks': ([-0.402,-0.418]), 'Policy': ([0.3,-0.4]), 'Psychology': ([1.35,0.3]),'Social Issue': ([0.422,0.818]), 'Education': ([0.776,0.893]), 'Health': ([1.06,0.68]), 'Business': ([0.205,0.495]), 'Language & Arts': ([1.24,-0.31]), 'History & Theory': ([0.78,-0.666]), 'Religion': ([1.03,-0.5]), 'Urban & Rural development': ([0.19,0.009])}
    
    nx.draw_networkx_nodes(G,pos,nodelist=nodelistnew,node_size=sizes1,node_color = 'sandybrown')


    for e in G.edges():
        ewidth = G[e[0]][e[1]]['weight']
        # for tp in topic1:
        if (e[0] in topic3 and e[1] in topic3):
            nx.draw_networkx_edges(G,pos,edgelist=[e],width=ewidth/20,edge_color='tan')
            
    nx.draw_networkx_labels(G, pos, font_size=8,font_family='sans-serif')



    # for n in G.nodes():
    #     print[n]
    #     print(G.degree(n]


    # nodedegrees = {}

    # for n in G.nodes():
    #     if n not in nodedegrees.keys():
    #         nodedegrees.setdefault(n, 0)
    #     nodedegrees[n] = G.degree(n)
        
    
    #结构洞数据
    # print('constraint')
    # print(sorted[nx.constraint(G].items(), key=lambda x: x[1]]

    print('effective_size')
    print(sorted(nx.effective_size(G).items(), key=lambda x: x[1], reverse=True))


    # nodedegrees = {}

    # for n in G.nodes():
    #     if n not in nodedegrees.keys():
    #         nodedegrees.setdefault(n, 0)
    #     nodedegrees[n] = G.degree(n)
    
    # print('degree')
    # print(sorted(nodedegrees.items(), key=lambda x: x[1], reverse=True]

    #展示边的权重，只考虑交叉
    edgewiths = {}
    for n in G.edges():
        if n not in edgewiths.keys():
            edgewiths.setdefault(n, 0)
        edgewiths[n] = G[n[0]][n[1]]['weight']


    print('edgewiths')
    print(sorted(edgewiths.items(), key=lambda x: x[1], reverse=True)[0:100])

    # print()


    plt.axis('off')
    axis = plt.gca()
    axis.set_xlim([1.2*x for x in axis.get_xlim()])
    axis.set_ylim([1.2*y for y in axis.get_ylim()])
    plt.show()
