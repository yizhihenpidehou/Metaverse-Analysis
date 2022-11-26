import requests
from lxml import etree
import re
import json
from bs4 import BeautifulSoup
import time
import random
import urllib
import re
import json
#拿到acm网页中论文的：标题，摘要，

#存储的文件
finalfile = open ('acm_res1.txt','a+')
with open('11新增/11月acm.txt','r') as ww:

    s=ww.read()
    
    lst=s.split('---------------------------------\n')
    for i in range(0,len(lst)-1):
        result ={}
        # 指定 url
        #print(lst[i])
        title=lst[i].split("title:")[1].split("\n")[0]
        quote_page = lst[i].split('ee:')[1]
        date=int(lst[i].split("Year:")[1].split("\n")[0])
        journal=""
        if len(lst[i].split('journal:'))<2:
            journal = lst[i].split('booktitle:')[1].split('\n')[0]
        else:
            journal = lst[i].split('journal:')[1].split('\n')[0]
        print("quote_page:",quote_page)
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
        
        

        headers = {"User-Agent":str(random.choice(user_agents))}
        # 访问这个网站并且返回这个网站的 html 源码然后保存在 ‘page’ 中
        response = requests.get(url=quote_page, headers=headers)
        page = response.text

        #page = urllib.request.urlopen(quote_page,headers=headers)
        # 使用 beautiful soup 解析这个 html 然后保存在 ‘soup’ 变量中。
        soup = BeautifulSoup(page, 'html.parser')
        print("soup:",soup)
        print('------------------------------------------------------')
        result.setdefault('title', '')
        result.setdefault('date', '')
        result.setdefault('abstract', '')
        result.setdefault('publish', '')
        result.setdefault('author', '')
        result.setdefault('author_location', '')
        result["title"] = title
        result["link"] = quote_page
        result["date"] = date
        result["publish"]= journal
        result["keywords"]=[]
        # result.setdefault('reference', '')
        # 获取title
        # title = soup.find('span', attrs={'class':'parent-item__subtitle simple-tooltip__inline--r truncate-text-css'})
        # try:
        #     print(title)
        #     s =str(title)
        #     a = r'data-title="(.*?)"'
        #     title = re.findall(a, s)
        #     print('title:')
        #     print(title[0])
        #     result['title']=title[0]
        # except:
        #     result['title']="not found"
        #     pass
        # else:
        #     pass
        # #获取日期
        # try:
        #     date = soup.find('span', attrs={'class':'epub-section__date'})
        #     s =str(date)
        #     a = r'"epub-section__date">(.*?)</span>'
        #     date = re.findall(a, s)
        #     print('date:')
        #     print(date[0])
        #     result['date']=date[0]
        # except:
        #     result['date']="not found"
        #     pass
        # else:
        #     pass
        # #获取publish信息
        # try:
        #     publish = soup.find('a', attrs={'class':'simple-tooltip__inline--r truncate-text-css'})
        #     s =str(publish)
        #     #a = r'data-title="(.*?) href="'
        #     a = r'data-title="(.*?)"'
        #     publish = re.findall(a, s)
        #     print('publish:')
        #     print(publish[0])
        #     result['publish']=publish[0]
        # except:
        #     result['publish']="not found"
        #     pass
        # else:
        #     pass
        #获取摘要
        try:
            abstract = soup.find('div', attrs={'class':'abstractSection abstractInFull'})
            s =str(abstract)
            a = r'<p>(.*?)</p>'
            abstract = re.findall(a, s)
            print('abstract:')
            print(abstract[0])
            result['abstract']=abstract[0]
        except:
            result['abstract']="not found"
            pass
        else:
            pass
        #暂时只抓取了第一作者的信息
        try:
            print('开始爬取作者')
            author_info = soup.find_all('span', attrs={'class':'loa__author-info'})
            s =str(author_info)
            a = r'width="24"/>(.*?)</span>'
            author = re.findall(a, s)
            print('author:')
            print(author)
            result['author']=author
        except:
            result['author']="not found"
            pass
        else:
            pass
        
        try:
            s =str(author_info)
            a = r'[0-9]">(.*?)</p>'
            author_location = re.findall(a, s)
            print(author_location)
            result['author_location']=author_location
        except:
            result['author_location']="not found"
            pass
        else:
            pass
            
        #匹配reference
        # try:
        #     reference = soup.find('ol', attrs={'class':'rlist references__list references__numeric'})
        #     s =str(reference)
        #     a = r'"references__note">(.*?)<span'
        #     reference = re.findall(a, s)
        #     print('reference:')
        #     print(reference)
        #     result['reference']=reference
        # except:
        #     result['reference']="not found"
        #     pass
        # else:
        #     pass
        print(str(i) + 'finished')
        #一个一个文章保存
        json_r=json.dumps(result)
        finalfile.write((json_r))
        finalfile.write('\n')
        finalfile.write('---------------------------------\n')

finalfile.close()


