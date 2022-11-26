import json
import sys

import requests
import random
import time
import re

def start_crawl_citation(inputpath,respath):
    base_url = "https://scholar.google.com/scholar?q="
    res_file=open(respath,"a+")
    ff=open(inputpath,"r")
    ff_str = ff.read()
    lst = ff_str.split("---------------------------------\n")
    for i in range(2, len(lst) - 1):
        print("第", i, "个")
        res_dic = {}
        random_sleep = random.choice(range(10, 12))
        print("sleep for:", random_sleep)
        sstr = json.loads(lst[i])
        title = sstr["title"]
        quote_page = sstr["link"]
        title_split = title.split(" ")
        target_url = base_url
        for j in range(0, len(title_split)):
            if j < len(title_split) - 1:
                target_url = target_url + title_split[j] + "+"
            else:
                target_url = target_url + title_split[j]
        sstr["title"] = title
        sstr["citation"] = 0
        user_agents = [
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"]

        headers = {"User-Agent": str(random.choice(user_agents))}
        # 访问这个网站并且返回这个网站的 html 源码然后保存在 ‘page’ 中
        print("target_url:", target_url)
        response = requests.get(url=target_url, headers=headers)
        page = response.text
        print("page:", page)
        print("cited by:", re.findall("Cited by", page))
        if len(page.split("Cited by")) > 1:
            print("citation:", int((page.split("Cited by")[1].split("</a>")[0]).strip()))
            citation = int((page.split("Cited by")[1].split("</a>")[0]).strip())
            sstr["citation"] = citation
        elif len(page.split("This page appears when Google automatically detects requests coming from your computer network which appear to be in violation of the"))>1 or len(page.split("Sorry, some features may not work in this version of Internet Explorer."))>1:
            print("detected!")
            sys.exit()
        else:
            sstr["citation"] = 0

        res_file.write(json.dumps(sstr) + "\n")
        res_file.write("---------------------------------\n")
        time.sleep(random_sleep)

    ff.close()
    res_file.close()
    return respath

def initial_citation_crawler():
    #将每个文章的title按空格分开并用+号连起来，前缀是：https://scholar.google.com/scholar?q=
    res_file=open("11月_arxiv_crawl_result_updateauthors_citation_final.json","a+")
    ff=open("../11月_arxiv_crawl_result_updateauthors_final.json","r")
    ff_str=ff.read()
    lst=ff_str.split("---------------------------------\n")
    base_url="https://scholar.google.com/scholar?q="
    for i in range(0,len(lst)-1):
        print("第",i,"个")
        res_dic={}
        random_sleep=random.choice(range(20,30))
        print("sleep for:",random_sleep)
        sstr=json.loads(lst[i])
        title=sstr["title"]
        quote_page=sstr["link"]
        title_split=title.split(" ")
        target_url=base_url
        for j in range(0,len(title_split)):
            if j< len(title_split)-1:
                target_url=target_url+title_split[j]+"+"
            else:
                target_url = target_url + title_split[j]
        sstr["title"]=title
        sstr["citation"]=0
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
        print("target_url:",target_url)
        response = requests.get(url=target_url, headers=headers)
        page = response.text
        print("page:", page)
        print("cited by:",re.findall("Cited by",page))
        if len(page.split("Cited by"))>1:
            print("citation:",int((page.split("Cited by")[1].split("</a>")[0]).strip()))
            citation=int((page.split("Cited by")[1].split("</a>")[0]).strip())
            sstr["citation"] = citation
        elif len(page.split("This page appears when Google automatically detects requests coming from your computer network which appear to be in violation of the"))>1:
            sys.exit()
        else:
            sstr["citation"]=0

        res_file.write(json.dumps(sstr) + "\n")
        res_file.write("---------------------------------\n")
        time.sleep(random_sleep)

    ff.close()
    res_file.close()

# start_crawl_citation(inputpath="fourpublisher_arxiv_withsource_updatedauthor2022-02.json",respath="fourpublisher_arxiv_withsource_updatedauthor_citation2022-02.json")