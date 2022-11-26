import json
import random
import re
import sys

import requests
from bs4 import BeautifulSoup

# 这是爬article和inproceedings的
ieeeresult = open('11新增/ieee_res_test.json', 'w')
with open('11新增/11月ieee3.txt', 'r') as ww:
    s = ww.read()

    lst = s.split('\n---------------------------------\n')
    print(len(lst))
    for i in range(0, len(lst) - 1):
        print(len(lst))
        result = {}
        # 指定 url
        title = lst[i].split('title:')[1].split('\n')[0]
        year = lst[i].split('Year:')[1].split('\n')[0]
        if len(lst[i].split('journal:'))<2:
            journal = lst[i].split('booktitle:')[1].split('\n')[0]
        else:
            journal = lst[i].split('journal:')[1].split('\n')[0]
        print(title)
        print(journal)
        quote_page = lst[i].split('ee:')[1].split('\n')[0]
        print(quote_page)

        user_agents = [
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60",
            "Opera/8.0 (Windows NT 5.1; U; en)",
            "Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50",
            "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50",
            "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0",
            "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2 ",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
            "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
            "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0) ",
            "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
            "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
            "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
            "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
            "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
            "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
            "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
            "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
            "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20"]

        headers = {"User-Agent": str(random.choice(user_agents))}
        # 访问这个网站并且返回这个网站的 html 源码然后保存在 ‘page’ 中
        # headers = headers
        response = requests.get(url=quote_page, headers=headers)
        page = response.text

        # page = urllib.request.urlopen(quote_page,headers=headers)
        # 使用 beautiful soup 解析这个 html 然后保存在 ‘soup’ 变量中。
        soup = BeautifulSoup(page, 'html.parser')
        print('------------------------------------------------------')
        result.setdefault('title', title)
        result.setdefault('date', year)
        result.setdefault('link', quote_page)
        result.setdefault('abstract', '')
        result.setdefault('publish', journal)
        result.setdefault('author', [])
        result.setdefault('author_location', [])
        #        # 获取title
        #        try:
        ##            title = soup.find('title')
        #            title = soup.find('meta', attrs={'property':'twitter:title'})
        #            print(title)
        #            print(type(title))
        ##            s =str(title)
        ##            a = r'<title>(.*?)|'
        ##            title = re.findall(a, s)
        ##            result['title']=title
        ##            print(title[0])
        ##            result['title']=title[0]
        #        except:
        #        #    result['title']="not found"
        #            result['title']="not found"
        #            pass
        #        else:
        #            pass

        # 获取metadata
        pubre = re.compile("metadata={.*?};")
        metadata = soup.find(text=pubre)

        a = r'metadata=(.*?);'
        metadata = re.findall(a, str(metadata))
        metadata = str(metadata)
        print("metadata:", metadata)
        if metadata == "[]":
            pass

        # title
        #        try:
        #            a = r'"title":"(.*?)",'
        #            title = re.findall(a, metadata)
        #            print(title[0])
        #            result['title']=title[0]
        #        except:
        #            result['title']="not found"
        #            pass
        #        else:
        #            pass
        #
        #        #日期
        #        try:
        #            a = r'"publicationDate":"(.*?)",'
        #            date = re.findall(a, metadata)
        #            print(date[0])
        #            result['date']=date[0]
        #        except:
        #            result['date']="not found"
        #            pass
        #        else:
        #            pass

        # 摘要
        try:
            a = r',"abstract":"(.*?)",'
            abstract = re.findall(a, metadata)
            if len(abstract) > 0:
                result['abstract'] = abstract[0]
            else:
                b = r'content=\'([^\']*)\"'
                abstract2 = soup.find(attrs={'property': 'twitter:description'})
                if len(abstract2) == None:
                    abstract2 = soup.find(name="meta", attrs={'name': 'description'})
                if len(re.findall(b, str(abstract2).strip())) == 0:
                    b = r'content="(.*)"'
                abstract_final = re.findall(b, str(abstract2).strip())[0]
                result['abstract'] = re.findall(b, str(abstract2).strip())[0].split(" property=")[0]
        except:

            result['abstract'] = "not found"
            pass

        # publish信息
        #        try:
        #            a = r'"publicationTitle":"(.*?)"'
        #            publish = re.findall(a, metadata)
        #            print(publish[0])
        #            result['publish']=publish[0]
        #        except:
        #            result['publish']="not found"
        #            pass
        #        else:
        #            pass

        # 作者信息(第一作者)
        try:
            # a = r'"authors":\[(.*?)\],"issn"'
            a = r'"authors":\[(.*?)\],"issn"'
            authors = re.findall(a, metadata)
            print("authorss:", authors)
            authors_str=""
            if len(authors) == 0:
                a = r'"authors":\[(.*?)\],"isbn"'
                # a = r'"authors":\[(.*?)\]'
                authors = re.findall(a, metadata)

                if len(authors)==0:
                    a = r'"authors":\[(.*?)\]'
                    authors = re.findall(a, metadata)

                authors_str = authors[0]

            else:
                authors_str = authors[0]
                # authors_str = '['+(authors[0].split(',"isbn":[{')[0])
                # if authors_str[len(authors_str)-1] != ']':
                #     authors_str+=']'
                # print("author——str:",authors_str)
            newauthors = eval(authors_str)
            print("type:",type(newauthors))
            print("newauthors:",newauthors)
            # 多个作者
            if type(newauthors) == type(list()):
                print('多个作者')
                for na in (newauthors):
                    print(na)
                    if ("name") in na:
                        print(na["name"])
                        result['author'].append(na["name"])
                    if ("name") not in na:
                        result['author'].append("no_name")
                    if ("affiliation") in na:
                        print(na["affiliation"])
                        result['author_location'].append(na["affiliation"])
                    if ("affiliation") not in na:
                        result['author_location'].append("no_location")
            elif type(newauthors) == type(tuple()):
                    print('多个作者')
                    for na in (newauthors):
                        print(na)
                        if ("name") in na:
                            print(na["name"])
                            result['author'].append(na["name"])
                        if ("name") not in na:
                            result['author'].append("no_name")
                        if ("affiliation") in na:
                            print(na["affiliation"])
                            result['author_location'].append(na["affiliation"])
                        if ("affiliation") not in na:
                            result['author_location'].append("no_location")
            # 一个作者
            else:
                print('一个作者')
                if ('name') in newauthors:
                    print(newauthors['name'])
                    result['author'].append(newauthors['name'])
                if ("name") not in newauthors:
                    result['author'].append("no_name")

                if ('affiliation') in newauthors:
                    print(newauthors['affiliation'])
                    result['author_location'].append(newauthors['affiliation'])
                if ("affiliation") not in newauthors:
                    result['author_location'].append("no_location")


        except Exception as e:
            print('author str(e):\t\t', str(e))
            pass
        else:
            pass
        print(str(i) + 'finished')
        # 检查一下作者和地点是不是对称
        if len(result['author']) != len(result['author_location']):
            print('作者和作者地点长度不一样！')
            print(result)
            sys.exit()
        # 一个一个文章保存
        json_r = json.dumps(result)
        ieeeresult.write((json_r))
        ieeeresult.write('\n')
        ieeeresult.write('---------------------------------\n')

ieeeresult.close()


