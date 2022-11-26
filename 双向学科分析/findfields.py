#!/usr/bin/python3
# -*- coding: UTF-8 -*-
#计算article期刊文献 主题，并且做主题比例分析
import matplotlib.pylab as plt
from matplotlib import font_manager as fm
from  matplotlib import cm
import numpy as np
import json
from pywaffle import Waffle

def get_keys(d, value):
    return [k for k,v in d.items() if v == value]
    
save = open ('second_filtered_dataset_withcountry_withfieds.json','w+')

fields = {

##Computer Science

"AI" : ['artificial intelligence', 'machine learning', 'computer vision', 'natural language processing',' ai ',' nlp ',' ml '],

"Algorithms & Theory" : ['computational theory', 'algorithms','mathemat'],

"Software & Application" :['application','software',' app ' ],

"Graph":['graph'],

"Hardware" : ['hardware','electronic','robotic'],

"System & Architecture" : ['architecture','informational system','computational system','computer system','operating system' ],

"Networks" : ['computer network','internet'],

###Social Science

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



with open('second_filtered_dataset_withcountry.json','r') as ww:

    splist = [".","'"]
    str=ww.read()

    lst=str.split('---------------------------------\n')

    #print(lst)
    
    fieldstata = {}
    for m in fields.keys():
        fieldstata.setdefault(m,0)
    
    
    for i in range(0,len(lst)-1):
        print(i)
        article =json.loads(lst[i])
        article.setdefault('field',[])
        #找到摘要，判断主题，作为文章新属性
        abstract = article['abstract']
        
        for j in fields.values():
            for k in j:
                if k in abstract.lower():
                    #文章主题不要重复计算
                    if (get_keys(fields, j)[0] not in article['field']):
                        article['field'].append(get_keys(fields, j)[0])
                        print('主题：')
                        print(article['field'])
        print(abstract)
        print(article)
    
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

        if year > 1994 and year <= 2021 and len(article['field']):
            for p in article['field']:
                fieldstata[p]+=1

        #一个一个文章保存
        json_r=json.dumps(article)
        #print('保存：'+json_r+str(i))
        save.write((json_r))
        save.write('\n')
        save.write('---------------------------------\n')

print(fieldstata)


#统计field画图

##########华夫饼图
#total = sum(fieldstata.values())
#plt.figure(
#    FigureClass=Waffle,
#    rows = 50,   # 列数自动调整
##    columns = 20,
#
#    values = fieldstata,
#    # 设置title
#    title = {
#        'label': "research fields 1994--2021 · ACM inproceedings",
#        'loc': 'left',
#        'fontdict':{
#            'fontsize': 8,
#        }
#    },
#    labels = ['{} {:.1f}%'.format(k, (v/total*100)) for k, v in fieldstata.items()],
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


#########饼图
labels=list(sorted(fieldstata.keys()))
x=[fieldstata.get(labels[i]) for i in range(len(labels))]
fig, axes = plt.subplots(figsize=(15,5),ncols=2) # 设置绘图区域大小
ax, ax2 = axes.ravel()

colors = cm.rainbow(np.arange(len(x))/len(x)) # colormaps: Paired, autumn, rainbow, gray,spring,Darks

patches, texts, autotexts = ax.pie(x, labels=labels,colors = colors, autopct='%1.0f%%',shadow=False)

#plt.pie(x, labels=labels,shadow=False)

ax.axis('equal')
ax.set_title('research fields 1994--2021 · ACM inproceedings', loc='left')

# ax2 只显示图例（legend）
ax2.axis('off')
ax2.legend(patches, labels, loc='lower left')

# 重新设置字体大小
proptease = fm.FontProperties()
proptease.set_size('xx-small')

plt.setp(autotexts, fontproperties=proptease)
plt.setp(texts, fontproperties=proptease)

plt.show()


