#!/usr/bin/python3
# -*- coding: UTF-8 -*-
#计算article期刊文献作者国家分析
import matplotlib.pylab as plt
from matplotlib import font_manager as fm
from  matplotlib import cm
import numpy as np
import json



def get_keys(d, value):
    return [k for k,v in d.items() if v == value]
    
#cotainlst,包含则修正
#lst，相等才修正

def get_vuenues(inputpath):
    with open(inputpath,'r') as ww:

        splist = [".","'"]
        str=ww.read()
        sum=0
        lst=str.split('---------------------------------\n')

        #print(lst)

        venuestata = {}

        for i in range(0,len(lst)-1):
            # print(i)
            article =json.loads(lst[i])
            #print(article)
            if article['publish']==[]:
                continue

            publish = article['publish']
            #得到文章时间
            year = int(article['date'])
    ######

            if year > 1999 and year <= 2022:

                if publish not in venuestata.keys():
                    venuestata.setdefault(publish,1)

                else:
                    venuestata[publish]+=1

                sum+=1

    sortedcountry=sorted(venuestata.items(), key=lambda x: x[1], reverse=True)
    print((sortedcountry))

    print(sum)




    #########饼图
    labels=(sorted(venuestata.keys(),reverse=True))


    newlabels = []




    #按top20统计
    if len(sortedcountry)<20:
        num = len(sortedcountry)

    else:
        num = 20
    for i in range(0,num):
        newlabels.append(sortedcountry[i][0])


    print(newlabels)

    x=[venuestata.get(newlabels[i]) for i in range(len(newlabels))]
    fig, axes = plt.subplots(figsize=(15,5),ncols=2) # 设置绘图区域大小
    ax, ax2 = axes.ravel()

    colors = cm.rainbow(np.arange(len(x))/len(x)) # colormaps: Paired, autumn, rainbow, gray,spring,Darks

    patches, texts, autotexts = ax.pie(x, labels=newlabels,colors = colors, autopct='%1.0f%%',shadow=False)

    #plt.pie(x, labels=labels,shadow=False)

    ax.axis('equal')
    ax.set_title('venues 2000--2022', loc='left')

    # ax2 只显示图例（legend）
    ax2.axis('off')
    ax2.legend(patches, newlabels, loc='lower left',fontsize=7)

    # 重新设置字体大小
    proptease = fm.FontProperties()
    proptease.set_size('xx-small')

    plt.setp(autotexts, fontproperties=proptease)
    plt.setp(texts, fontproperties=proptease)
    plt.savefig("vuenues.png")
    plt.show()

get_vuenues("../2022-11/fourpublisher_arxiv_withsource_updatedauthor2022-11.json")
