#!/usr/bin/python
# -*- coding: UTF-8 -*-
#分析社会计算文章数据集的work--年份对应关系
import matplotlib.pylab as plt
import json


with open('acm.json','r') as ww:

    str=ww.read()

    lst=str.split('---------------------------------\n')

    #print(lst)
    
    dic = {}
    sum=0
    newdic1 = {}
    

    for i in range(2000,2023):
        dic[i]=0
    
    for i in range(0,len(lst)-1):
        #print(lst[i])
        article = json.loads(lst[i])
        year = int(article['date'])
        
        dic[year]+=1
        sum=sum+1
    for i in range(2000,2023):
        print ("Year:",i,"Work Num:",dic[i])
        newdic1[i] = dic[i]
    
    print(sum)

with open('ieee.json','r') as ww:

    str=ww.read()

    lst=str.split('---------------------------------\n')

    #print(lst)
    
    dic = {}
    sum=0
    newdic2 = {}
    

    for i in range(2000,2023):
        dic[i]=0
    
    for i in range(0,len(lst)-1):
        #print(lst[i])
        article = json.loads(lst[i])
        year = int(article['date'])
        
        dic[year]+=1
        sum=sum+1
    for i in range(2000,2023):
        print ("Year:",i,"Work Num:",dic[i])
        newdic2[i] = dic[i]
    
    print(sum)
    
with open('elsevier.json','r') as ww:

    str=ww.read()

    lst=str.split('---------------------------------\n')

    #print(lst)
    
    dic = {}
    sum=0
    newdic3 = {}
    

    for i in range(2000,2023):
        dic[i]=0
    
    for i in range(0,len(lst)-1):
        #print(lst[i])
        article = json.loads(lst[i])
        year = int(article['date'])
        
        dic[year]+=1
        sum=sum+1
    for i in range(2000,2023):
        print ("Year:",i,"Work Num:",dic[i])
        newdic3[i] = dic[i]
    
    print(sum)

with open('springer.json','r') as ww:

    str=ww.read()

    lst=str.split('---------------------------------\n')

    #print(lst)
    
    dic = {}
    sum=0
    newdic4 = {}
    

    for i in range(2000,2023):
        dic[i]=0
    
    for i in range(0,len(lst)-1):
        #print(lst[i])
        article = json.loads(lst[i])
        year = int(article['date'])
        
        dic[year]+=1
        sum=sum+1
    for i in range(2000,2023):
        print ("Year:",i,"Work Num:",dic[i])
        newdic4[i] = dic[i]
    
    print(sum)

#with open('arxiv.json','r') as ww:
#
#    str=ww.read()
#
#    lst=str.split('---------------------------------\n')
#
#    #print(lst)
#
#    dic = {}
#    sum=0
#    newdic5 = {}
#
#
#    for i in range(1994,2023):
#        dic[i]=0
#
#    for i in range(1,len(lst)-1):
#        print(lst[i])
#        article = json.loads(lst[i])
#        year = int(article['date'])
#
#        dic[year]+=1
#        sum=sum+1
#    for i in range(1994,2022):
#        print ("Year:",i,"Work Num:",dic[i])
#        newdic5[i] = dic[i]
#
#    print(sum)
    
myList1 = newdic1.items()
myList1 = sorted(myList1)
x, y1 = zip(*myList1)

myList2 = newdic2.items()
myList2 = sorted(myList2)
x, y2 = zip(*myList2)

myList3 = newdic3.items()
myList3 = sorted(myList3)
x, y3 = zip(*myList3)

myList4 = newdic4.items()
myList4 = sorted(myList4)
x, y4 = zip(*myList4)

#myList5 = newdic5.items()
#myList5 = sorted(myList5)
#x, y5 = zip(*myList5)



l1,=plt.plot(x, y1)
l2,=plt.plot(x, y2)
l3,=plt.plot(x, y3)
l4,=plt.plot(x, y4)
#l5,=plt.plot(x, y5)


plt.legend(handles=[l1,l2,l3,l4], labels=[ 'acm','ieee','elsevier','springer'],loc='upper left')

plt.xlabel('Year')
plt.ylabel('Work Number')

plt.savefig("Publisher.png")

plt.show()
