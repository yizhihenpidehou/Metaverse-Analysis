#!/usr/bin/python3
# -*- coding: UTF-8 -*-
#计算article期刊文献 主题，并且做主题比例分析
import matplotlib.pylab as plt
from matplotlib import font_manager as fm
from  matplotlib import cm
import numpy as np
import json


def get_keys(d, value):
    return [k for k,v in d.items() if v == value]
    
save = open ('new_second_filtered_dataset_withtopics1.json','w+')

topic1 = ['social networks',  'human-computer interaction', 'semantic web', 'machine learning', 'network analysis', 'world wide web', 'social networking sites', 'artificial intelligence', 'online social networks', 'computer science', 'knowledge discovery',  'machine learning techniques', 'collective intelligence', 'system dynamics']
topic2 =['social networks', 'social media', 'online social networks', 'social networking sites', 'social network analysis', 'social network sites', 'mobile social networks', 'social network services', 'human-computer interaction', 'social web', 'machine learning', 'recommender systems', 'social media sites', 'network sites', 'mobile devices', 'location-based social networks', 'online social media', 'social media platforms', 'social computing', 'collective intelligence',  'world wide web', 'sina weibo',  'social media services', 'semantic web', 'like facebook', 'natural language processing', 'social networking applications', 'web services', 'community detection', 'social interactions', 'influence maximization', 'social capital', 'computer science', 'collaborative filtering',  'social behavior', 'viral marketing', 'amazon mechanical turk', 'link prediction', 'decision making']
topic3 = ['social media', 'social networks', 'online social networks', 'social media platforms', 'machine learning', 'artificial intelligence', 'social network analysis', 'mobile social networks', 'online social media', 'human-computer interaction', 'natural language processing', 'location-based social networks', 'sentiment analysis', 'influence maximization', 'mobile devices', 'media platforms', 'social network services', 'recommender systems', 'community detection', 'spatial crowdsourcing', 'emotion recognition', 'fake news', 'support vector machine', 'social media sites', 'social internet', 'viral marketing', 'deep learning', 'mobile crowdsourcing', 'link prediction', 'covid-19 pandemic', 'social influence', 'like twitter', 'sina weibo', 'social media content', 'decision making', 'autism spectrum disorder', 'machine learning techniques', 'latent dirichlet allocation', 'computer science', 'convolutional neural network', 'collective intelligence', 'event detection', 'communication technologies', 'neural network', 'event-based social networks']

with open('../../dblp_final_dataset.json','r') as ww:

    splist = [".","'"]
    str=ww.read()

    lst=str.split('---------------------------------\n')

    #print(lst)
    
    topicstata = {}
    for m in topic1:
        topicstata.setdefault(m,0)
    
    
    for i in range(0,len(lst)-1):
        print(i)
        article =json.loads(lst[i])
        article.setdefault('topic',[])
        #找到摘要，判断主题，作为文章新属性
        abstract = article['abstract']
        
        for j in topic1:
            if j in abstract.lower():
                #文章主题不要重复计算
                if (j not in article['topic']):
                    article['topic'].append(j)
        #             print('主题：')
        #             print(article['topic'])
        # print(abstract)
        # print(article)
    
#得到文章时间
        try:
            if article['date'] == 'not found':
                year = 0
                
            else:
                if " " in article['date']:
                    year = article['date'].split(' ')[1]
                    year = int(year)
            
                else:
                    year = article['date']
                    year = int(year)
              
        except:
            year = 0
            pass
            
        else:
            pass
######

        if year > 1993 and year <= 2008 and len(article['topic']):
            for p in article['topic']:
                if p in topic1:
                    topicstata[p]+=1

            #一个一个文章保存
            json_r=json.dumps(article)
            #print('保存：'+json_r+str(i))
            save.write((json_r))
            save.write('\n')
            save.write('---------------------------------\n')

print(topicstata)


#统计topic画图

##########华夫饼图
#total = sum(topicstata.values())
#plt.figure(
#    FigureClass=Waffle,
#    rows = 50,   # 列数自动调整
##    columns = 20,
#
#    values = topicstata,
#    # 设置title
#    title = {
#        'label': "research topics 1994--2021 · ACM inproceedings",
#        'loc': 'left',
#        'fontdict':{
#            'fontsize': 8,
#        }
#    },
#    labels = ['{} {:.1f}%'.format(k, (v/total*100)) for k, v in topicstata.items()],
##    cmap_name = "Accent",
##    colors = []
#    # 设置标签图例的样式
#    legend = {
##        'loc': 'upper right',
#        'bbox_to_anchor': (1,2),
##        'ncol': len(dic),
#        'fontsize': 4
#    },
#    dpi=150
#)
#plt.show()
#########华夫饼图

'''
#########饼图
labels=list(sorted(topicstata.keys()))
x=[topicstata.get(labels[i]) for i in range(len(labels))]
fig, axes = plt.subplots(figsize=(15,5),ncols=2) # 设置绘图区域大小
ax, ax2 = axes.ravel()

colors = cm.rainbow(np.arange(len(x))/len(x)) # colormaps: Paired, autumn, rainbow, gray,spring,Darks

patches, texts, autotexts = ax.pie(x, labels=labels,colors = colors, autopct='%1.0f%%',shadow=False)

#plt.pie(x, labels=labels,shadow=False)

ax.axis('equal')
ax.set_title('research topics 1994--2021 · ACM inproceedings', loc='left')

# ax2 只显示图例（legend）
ax2.axis('off')
ax2.legend(patches, labels, loc='lower left')

# 重新设置字体大小
proptease = fm.FontProperties()
proptease.set_size('xx-small')

plt.setp(autotexts, fontproperties=proptease)
plt.setp(texts, fontproperties=proptease)

plt.show()

'''
