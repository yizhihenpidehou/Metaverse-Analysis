# -*- coding: UTF-8 -*-
#初筛数据集链接分类
def get_keys(d, value):
    return [k for k,v in d.items() if v == value]

def start_classify(input_path,res_path):
    print('classify start!')
    fourpublisher_arxiv=open(res_path,'w')
    # sp = open('springer'+str(flag)+'.txt', 'w')
    # acm = open('acm'+str(flag)+'.txt', 'w')
    # ie = open('ieee'+str(flag)+'.txt', 'w')
    # el = open('elsevier'+str(flag)+'.txt', 'w')
    # ar = open('arxiv'+str(flag)+'.txt', 'w')
    # ot = open('others'+str(flag)+'.txt', 'w')

    with open(input_path, 'r') as ww:

        sstr = ww.read()

        lst = sstr.split('---------------------------------\n')

        # print(lst)

        pubstata = {}

        for i in range(0, len(lst)):
            print(i)
            print(lst[i])
            pub = 'others'
            # 找到摘要，判断主题，作为文章新属性
            if 'ee:' in lst[i]:
                str1 = lst[i].split('ee:')[1]
                link = str1.split('\n')[0]
                print(link)
                try:
                    year = int((lst[i].split('Year:')[1]).split('\n')[0])
                except:
                    pass
                else:
                    pass
            else:
                year = 0
                link = ''

            if 'ieee' in link:
                pub = 'IEEE'

            elif 'acm' in link:
                pub = 'ACM'

            elif 'springer' in link:
                pub = 'Springer'

            elif 'elsevier' in link:
                pub = 'Elsevier'

            elif 'arxiv' in link or ('10.48550' in link):
                pub = 'arxiv'

            else:
                if 'https://doi.org' in link:
                    pub = (link.split('https://doi.org/')[1]).split('/')[0]
                    if pub == '10.1016':
                        pub = 'Elsevier'
                    elif pub == '10.1109':
                        pub = 'IEEE'
                    elif pub == '10.1145':
                        pub = 'ACM'
                    elif pub == '10.1007':
                        pub = 'Springer'
                    else:
                        pub = link.split('/')[3]

                elif 'http://doi.org' in link:
                    pub = (link.split('http://doi.org/')[1]).split('/')[0]
                    if pub == '10.1016':
                        pub = 'Elsevier'
                    elif pub == '10.1109':
                        pub = 'IEEE'
                    elif pub == '10.1145':
                        pub = 'ACM'
                    elif pub == '10.1007':
                        pub = 'Springer'
                    else:
                        pub = link.split('/')[3]

                elif 'https://' in link:
                    pub = link.split('https://')[1].split('/')[0]

                elif 'http://' in link:
                    pub = link.split('http://')[1].split('/')[0]

            if year >= 2000 and year <= 2022:
                if pub in pubstata.keys():
                    pubstata[pub] = pubstata[pub] + 1
                else:
                    pubstata.setdefault(pub, 1)

                if pub == 'Springer':
                    lst[i] += 'source:springer\n'
                    fourpublisher_arxiv.write(lst[i])

                    fourpublisher_arxiv.write('---------------------------------\n')
                elif pub == 'ACM':
                    lst[i] += 'source:acm\n'
                    fourpublisher_arxiv.write(lst[i])
                    fourpublisher_arxiv.write('---------------------------------\n')
                elif pub == 'IEEE':
                    lst[i] += 'source:ieee\n'
                    fourpublisher_arxiv.write(lst[i])
                    fourpublisher_arxiv.write('---------------------------------\n')
                elif pub == 'Elsevier':
                    lst[i] += 'source:elsevier\n'
                    fourpublisher_arxiv.write(lst[i])
                    fourpublisher_arxiv.write('---------------------------------\n')
                elif pub == 'arxiv':
                    lst[i] += 'source:arxiv\n'
                    fourpublisher_arxiv.write(lst[i])
                    fourpublisher_arxiv.write('---------------------------------\n')
                else:
                    continue
                    # fourpublisher_arxiv.write(lst[i])
                    # fourpublisher_arxiv.write('---------------------------------\n')

    print(pubstata)
    print(sorted(pubstata.items(), key=lambda x: x[1], reverse=True))

    fourpublisher_arxiv.close()
    print('classify finished!')
    return res_path
# start_classify("first_filtered_all.txt",'first_filtered_all_withsource.txt')
def initial_classify():
    
    sp=open('springer.txt','w')
    acm=open('acm.txt','w')
    ie=open('ieee.txt','w')
    el=open('elsevier.txt','w')
    ar=open('arxiv.txt','w')
    ot=open('others.txt','w')

    with open('../firstFilter/11月新增+first_filtered_all.txt', 'r') as ww:

        splist = [".","'"]
        str=ww.read()

        lst=str.split('---------------------------------\n')

        #print(lst)

        pubstata = {}

        for i in range(0,len(lst)):
            print(i)
            print(lst[i])
            pub = 'others'
            #找到摘要，判断主题，作为文章新属性
            if 'ee:' in lst[i]:
                str1=lst[i].split('ee:')[1]
                link = str1.split('\n')[0]
                print(link)
                try:
                    year = int((lst[i].split('Year:')[1]).split('\n')[0])
                except:
                    pass
                else:
                    pass
            else:
                year=0
                link = ''

            if 'ieee' in link:
                pub = 'IEEE'

            elif 'acm' in link:
                pub = 'ACM'

            elif 'springer' in link:
                pub = 'Springer'

            elif 'elsevier' in link:
                pub = 'Elsevier'

            elif 'arxiv' in link or ('10.48550' in link):
                pub = 'arxiv'

            else:
                if 'https://doi.org' in link:
                    pub = (link.split('https://doi.org/')[1]).split('/')[0]
                    if pub == '10.1016':
                        pub ='Elsevier'
                    elif pub == '10.1109':
                        pub = 'IEEE'
                    elif pub == '10.1145':
                        pub = 'ACM'
                    elif pub == '10.1007':
                        pub = 'Springer'
                    else:
                        pub = link.split('/')[3]

                elif'http://doi.org' in link:
                    pub = (link.split('http://doi.org/')[1]).split('/')[0]
                    if pub == '10.1016':
                        pub ='Elsevier'
                    elif pub == '10.1109':
                        pub = 'IEEE'
                    elif pub == '10.1145':
                        pub = 'ACM'
                    elif pub == '10.1007':
                        pub = 'Springer'
                    else:
                        pub = link.split('/')[3]

                elif'https://' in link:
                    pub = link.split('https://')[1].split('/')[0]

                elif'http://' in link:
                    pub = link.split('http://')[1].split('/')[0]

            if year >= 2000 and year <= 2022:
                if pub in pubstata.keys():
                    pubstata[pub] = pubstata[pub]+1
                else:
                    pubstata.setdefault(pub, 1)

                if pub == 'Springer':
                   sp.write(lst[i])
                   sp.write('---------------------------------\n')
                elif pub == 'ACM':
                   acm.write(lst[i])
                   acm.write('---------------------------------\n')
                elif pub == 'IEEE':
                   ie.write(lst[i])
                   ie.write('---------------------------------\n')
                elif pub == 'Elsevier':
                   el.write(lst[i])
                   el.write('---------------------------------\n')
                elif pub == 'arxiv':
                   ar.write(lst[i])
                   ar.write('---------------------------------\n')
                else:
                   ot.write(lst[i])
                   ot.write('---------------------------------\n')

    print(pubstata)

    print(sorted(pubstata.items(),key = lambda x:x[1],reverse = True))

    sp.close()
    ot.close()
    el.close()
    ie.close()
    acm.close()
    ar.close()
