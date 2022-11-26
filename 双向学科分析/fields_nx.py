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

with open('second_filtered_dataset_withcountry_withfieds.json','r') as ww:

    splist = [".","'"]
    str=ww.read()

    lst=str.split('---------------------------------\n')

    #print(lst)
    fields = {

"AI" : ['artificial intelligence', 'machine learning', 'computer vision', 'natural language processing',' ai ',' nlp ',' ml '],

"Algorithms & Theory" : ['computational theory', 'algorithms','mathemat'],

"Software & Application" :['application','software',' app ' ],

"Graph":['graph'],

"Hardware" : ['hardware','electronic','robotic'],

"System & Architecture" : ['architecture','informational system','computational system','computer system','operating system' ],

"Networks" : ['computer network','internet'],

###

"Policy" : ['polic','politic','welfare','poverty'],

"Psychology" : ['psycholog'], #

"Social Issue" : ['social probem','social issue'], #

"Education" : ['education'],

"Health" : ['health','clinical','medic'],

"Business" : ['business','econom','market'],

"Language & Arts" : ['language',' art ', 'arts'],

"History & Theory" : ['history','theory' ],

"Religion" : ['religio'], #

"Urban & Rural development" : ['rural', 'urban', 'community','city','citizen','demograph']
    
}

    nodelist1 = ["AI" ,"Algorithms & Theory" , "Software & Application", "Graph" , "Hardware" , "System & Architecture" , "Networks"]

    nodelist2 = ["Policy" , "Psychology" , "Social Issue" , "Education" , "Health" , "Business" , "Language & Arts" , "History & Theory" , "Religion" , "Urban & Rural development"]


    # 创建空的网格
    G=nx.Graph()
    # 添加节点
    print (list(fields.keys()))
    G.add_nodes_from(nodelist1, bipartite=0)
    G.add_nodes_from(nodelist2, bipartite=1)
    
    for i in range(0,len(lst)-1):
        print(i)
        article =json.loads(lst[i])
        print(article['field'])
        field = article['field']
        date = article['date']
        
        if not (int(date) >=1994 and int(date) <2022):
            print('invalid year:'+date)
            continue
        
        if len(field) != 0:
            cp = ['','']
            for j in field:
                cp[0] = j
                for k in field:
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
            sizes1.append(250*(nx.effective_size(G)[v]))
        elif v in nodelist2:
            sizes2.append(250*(nx.effective_size(G)[v]))

    print(sizes1)
    print(sizes2)

#    pos = nx.shell_layout(G)
#    #pos = dict()
#    pos.update( (n, (1, i)) for i, n in enumerate(nodelist1) )
#    pos.update( (n, (2, i)) for i, n in enumerate(nodelist2) )

#自定义位置
    pos = {'AI': ([-1,0.04]), 'Algorithms & Theory': ([-0.85,0.42]), 'Software & Application': ([-0.13,0.1]), 'Graph': ([-0.22,0.54]), 'Hardware': ([-0.527,0.736]), 'System & Architecture': ([-0.87,-0.33]), 'Networks': ([-0.402,-0.418]), 'Policy': ([0.3,-0.4]), 'Psychology': ([1.35,0.3]),'Social Issue': ([0.422,0.818]), 'Education': ([0.776,0.893]), 'Health': ([1.06,0.68]), 'Business': ([0.205,0.495]), 'Language & Arts': ([1.24,-0.31]), 'History & Theory': ([0.78,-0.666]), 'Religion': ([1.03,-0.5]), 'Urban & Rural development': ([0.19,0.009])}
    
    nx.draw_networkx_nodes(G,pos,nodelist=nodelist1,label=node_label.items(),node_size=sizes1,node_color = 'slateblue')

    nx.draw_networkx_nodes(G,pos,nodelist=nodelist2,label=node_label.items(),node_size=sizes2)

    for e in G.edges():
        ewidth = G[e[0]][e[1]]['weight']
        print(e)
        print(ewidth)
        if (e[0] in nodelist1 and e[1] in nodelist1) or (e[0] in nodelist2 and e[1] in nodelist2):
            nx.draw_networkx_edges(G,pos,edgelist=[e],width=ewidth/60,edge_color='silver')
        else:
            nx.draw_networkx_edges(G,pos,edgelist=[e],width=ewidth/60,edge_color='skyblue')
            
    nx.draw_networkx_labels(G, pos,font_size=6,font_family='sans-serif')


    #生成节点位置
    pos=nx.circular_layout(G)
    print('position of all nodes:',pos)

    for n in G.nodes():
        print((n))
        print(G.degree(n))


    nodedegrees = {}

    for n in G.nodes():
        if n not in nodedegrees.keys():
            nodedegrees.setdefault(n, 0)
        nodedegrees[n] = G.degree(n)
        

    #结构洞数据
    print('constraint')
    print(sorted((nx.constraint(G)).items(), key=lambda x: x[1]))

    print('effective_size')
    print(sorted((nx.effective_size(G)).items(), key=lambda x: x[1], reverse=True))
        

    nodedegrees = {}

    for n in G.nodes():
        if n not in nodedegrees.keys():
            nodedegrees.setdefault(n, 0)
        nodedegrees[n] = G.degree(n)
    
    print('degree')
    print(sorted(nodedegrees.items(), key=lambda x: x[1], reverse=True))

#展示边的权重，只考虑交叉
    edgewiths = {}
    for n in G.edges():
        if (n[0] in nodelist1 and n[1] in nodelist2) or (n[0] in nodelist2 and n[1] in nodelist1):
            if n not in edgewiths.keys():
                edgewiths.setdefault(n, 0)
            edgewiths[n] = G[n[0]][n[1]]['weight']


    print('edgewiths')
    print(sorted(edgewiths.items(), key=lambda x: x[1], reverse=True))

    print()
    


    plt.title('1994--2021')
    #nx.draw(G,pos=nx.circular_layout(G),with_labels=True)
    plt.show()
