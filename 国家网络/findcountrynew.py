#!/usr/bin/python3
# -*- coding: UTF-8 -*-
#计算article期刊文献作者国家分析
import matplotlib.pylab as plt
from matplotlib import font_manager as fm
from  matplotlib import cm
import numpy as np
import json
from pywaffle import Waffle

def get_keys(d, value):
    return [k for k,v in d.items() if v == value]
year_lst=[(2000,2022)]
errorlst = ['n','c','not found','']

with open('../2022-11/fourpublisher_arxiv_withsource_updatedauthor_citation2022-11_final.json','r') as ww:

    splist = [".","'"]
    str=ww.read()
    sum=0
    lst=str.split('---------------------------------\n')

    #print(lst)
    

    for year_tuple in year_lst:
        countrystata = {}

        for i in range(0,len(lst)-1):
            print(i)
            try:
                article =json.loads(lst[i])
                print("article:",article)
                author_country = (article['country'][0]).upper()
            except:
                # print(article)
                pass

            else:
                pass
    #得到文章时间
            year = int(article['date'])
    ######

            if year > year_tuple[0] and year <= year_tuple[1] and (author_country not in errorlst):
                if ('ctmighterror' not in article) or (article['ctmighterror']==[]):
                    if author_country not in countrystata.keys():
                        countrystata.setdefault(author_country,1)

                    else:
                        countrystata[author_country]+=1

                    sum+=1

        sortedcountry=sorted(countrystata.items(), key=lambda x: x[1], reverse=True)[:10]
        print((sortedcountry))

        print(sum)

        #统计theme画图

        ##########华夫饼图
        #total = sum(countrystata.values())
        #plt.figure(
        #    FigureClass=Waffle,
        #    rows = 50,   # 列数自动调整
        ##    columns = 20,
        #
        #    values = countrystata,
        #    # 设置title
        #    title = {
        #        'label': "research themes 1994--2021 · ACM inproceedings",
        #        'loc': 'left',
        #        'fontdict':{
        #            'fontsize': 8,
        #        }
        #    },
        #    labels = ['{} {:.1f}%'.format(k, (v/total*100)) for k, v in countrystata.items()],
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
        labels=(sorted(countrystata.keys(),reverse=True))

        #暂时只保留文章数量比较多的
        #print('labels')
        #print(labels)
        newlabels = []

        #for i in labels:
        #    #print(countrystata[i])
        #    if countrystata[i] >= 50:
        #        newlabels.append(i)
        if len(sortedcountry)<10:
            num = len(sortedcountry)

        else:
            num = 10

        for i in range(0,num):
            newlabels.append(sortedcountry[i][0])
        #for i in range(6,10):
        #    newlabels.append(sortedcountry[i][0])

        # print(newlabels)
        #
        # x=[countrystata.get(newlabels[i]) for i in range(len(newlabels))]
        # fig, axes = plt.subplots(figsize=(15,5),ncols=2) # 设置绘图区域大小
        # ax, ax2 = axes.ravel()

        # colors = cm.rainbow(np.arange(len(x))/len(x)) # colormaps: Paired, autumn, rainbow, gray,spring,Darks

        # patches, texts, autotexts = ax.pie(x, labels=newlabels,colors = colors, autopct='%1.0f%%',shadow=False)

        # #plt.pie(x, labels=labels,shadow=False)

        # ax.axis('equal')
        # ax.set_title('author countries and Regions 2017--2021', loc='left')

        # # ax2 只显示图例（legend）
        # ax2.axis('off')
        # ax2.legend(patches, newlabels, loc='lower left')

        # # 重新设置字体大小
        # proptease = fm.FontProperties()
        # proptease.set_size('xx-small')

        # plt.setp(autotexts, fontproperties=proptease)
        # plt.setp(texts, fontproperties=proptease)

        # plt.show()


