#!/usr/bin/python
# -*- coding: UTF-8 -*-
#分析社会计算文章数据集的work--年份对应关系
import matplotlib.pylab as plt
import json

sp=open('springer.json','a+')
acm=open('acm.json','a+')
ie=open('ieee.json','a+')
el=open('elsevier.json','a+')

with open('../fourpublisher_crawl_citation_res.json','r') as ww:

    str=ww.read()

    lst=str.split('---------------------------------\n')
    for i in range(0,len(lst)-1):
    #print(lst[i])
        try:
            article = json.loads(lst[i])
            source = article['source']
            print(source)
            if 'acm' in source:
                acm.write(lst[i])
                acm.write('---------------------------------\n')
                
            if 'ieee' in source:
                ie.write(lst[i])
                ie.write('---------------------------------\n')
                
            if 'springer' in source:
                sp.write(lst[i])
                sp.write('---------------------------------\n')

            if 'elsevier' in source:
                el.write(lst[i])
                el.write('---------------------------------\n')
        except Exception as e:
            print(e)
            print(article)
        
        else:
            pass
sp.close()
el.close()
ie.close()
acm.close()
