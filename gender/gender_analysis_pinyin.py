import json
# ngender只能检测中文名
import ngender as ng
# 可以检测中文拼音
from Pinyin2Hanzi import DefaultDagParams
from Pinyin2Hanzi import dag

import gender_guesser.detector as gender
#!/usr/bin/python
# Author : wkong
# Crack

def clearChar(chars):
    reStr = ['\n','\r','\t',' ']

    for reS in reStr:
        chars = chars.replace(reS, '')

    return chars


def sm(strs):
    smlist = 'bpmfdtnlgkhjqxrzcsyw'
    nosm = ['eR','aN','eN','iN','uN','vN','nG','NG']
    rep = {'ZH':'Zh','CH':'Ch','SH':'Sh'}

    for s in smlist:
        strs = strs.replace(s,s.upper())

    for s in nosm:
        strs = strs.replace(s,s.lower())

    for s in rep.keys():
        strs = strs.replace(s,rep[s])

    for s in nosm:
        tmp_num = 0
        isOk = False
        while (tmp_num < len(strs)) and (isOk==False):
            try:
                tmp_num = strs.index(s.lower(),tmp_num)
            except:
                isOk = True
            else:
                tmp_num = tmp_num + len(s)
                if strs[tmp_num:tmp_num+1].lower() not in smlist:
                    strs = strs[:tmp_num-1]+strs[tmp_num-1:tmp_num].upper()+strs[tmp_num:]

    return strs






def pinyin_to_hanzi(pinyin,Topk=5):
    '''
    拼音转化为汉字
    汉字存在多意性，所以这里没有一一对应的关系，只能选出概率最高的topk
    '''
    translator=DefaultDagParams()
    result=dag(translator,pinyin,path_num=Topk,log=True)
    # print("pinyin:",pinyin)
    for item in result:
        socre=item.score # 得分
        res=item.path # 转换结果
        print('pinyin:',res)
def onep(strs):
    restr = ''
    strs = sm(strs)
    for s in strs:
        if 'A' <= s and s <= 'Z':
            restr = restr + ' ' + s
        else:
            restr = restr + s

    restr = restr[1:]
    restr = restr.lower()
    return restr.split(' ')


def team_gender_diversity(lst):
    res=[]
    for i in range(0,len(lst)-1):
        item_json=json.loads(lst[i])


def gender_pipeline(inputpath,respath):
    male=0
    female=0
    target_file=open(inputpath,'r')
    res_file=open(respath,'w')
    d = gender.Detector()
    with  target_file as tf:
        tf_str=tf.read()
        lst=tf_str.split("---------------------------------\n")
        for i in range(0,len(lst)-1):
            tf_json=json.loads(lst[i])
            author=tf_json["author"]
            gender_res_lst=[]
            # print("author:",author)
            for a in author:
                a_=a.split(" ")
                gender_res="unknown"
                for p in a_:
                    gender_res = d.get_gender(p)
                    if gender_res !='unknown' and gender_res !='andy':
                        break
                print("gender_res:",gender_res)
                if gender_res == 'male':
                    male+=1
                    gender_res_lst.append(1)
                elif gender_res == 'female':
                    female+=1
                    gender_res_lst.append(0)
            tf_json["gender"]=gender_res_lst
            res_file.write(json.dumps(tf_json)+'\n')
            res_file.write("---------------------------------\n")
    res_file.close()
        # print("male:",male)
        # print("female:",female)
gender_pipeline("../2022-01/fourpublisher_arxiv_withsource_updatedauthor_citation2022-01.json",
                "fourpublisher_arxiv_withsource_updatedauthor_citation2022-01_withgender.json")