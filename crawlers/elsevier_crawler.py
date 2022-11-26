#coding=utf-8


import urllib.request
import json
from lxml import etree
crawl_file=open("elsevier.txt",'r')
# 输出文件中所有内容
# print(crawl_file.read())
total_content=crawl_file.read()
results=[]
list=total_content.split('---------------------------------\n')

print(len(list))
total_len=len(list)
print("len:",total_len)
#存储结果的文件
finalfile = open ('elsevier_crawl_results.json','a+')
#未能爬到的数据
#errorfile=open('new_2021_elsevier_err.json',"a+")

print("len:",len(list))
for i in range(0,len(list)-1):
    # try:
        print("start:",i)
        str1 = list[i].split('ee:')[1]

        url = str1.split('\n')[0]

        str2 = list[i].split('title:')[1]
        title = str2.split('\n')[0]

        str3 = list[i].split('Year:')[1]
        year = str3.split('\n')[0]

        str4=""
        if len(list[i].split('journal:'))!=2:
            str4 = list[i].split('booktitle:')[1]
        else:
            str4 = list[i].split('journal:')[1]
        journal=str4.split('\n')[0]
        # print('ee:',url)
        # print('title:',title)
        # print('year:',year)
        # print('journal:',journal)
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
        headers = {
                  # "Cookie":"dk_ezNNjLPu_ICblKgC44YJn98ytqweX_IBeN3ZTYVM-1650073344-0-AcIogCMwSDB3zzmi1qWaNAikKbO/YovFT01um0gxlnxDosZbx7MEfW2xdiW6nn7lSxLS9bajzXub6J1q3b3JL12KF3ilDIyNwenI03AC4jXu",
                  "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36",
                  # "cookie":"EUID=b9a7cc4e-0e8c-478e-99d2-405422273d1c; mboxes={}; utt=40b433e9c8d008180f01a955ec9981761cdbf5c; ANONRA_COOKIE=141A830716A5EE0641BD796EDC520AA4AA826FFB466A31C132C8E723A8AFEFBE9EB0CAF6E01972F55A40E54674BA775157F12FD9E428BCC4; id_ab=IDP; cf_clearance=XOvp53A6VX0CmkgVVEZSt04LcfvK4owqtRlQ4Z6QnQw-1650035267-0-250; sd_session_id=ee75c6f032693541eb6b33d6dab0357be935gxrqb; has_multiple_organizations=false; fingerPrintToken=68048a68a656037ddc21e3ccf50abbd6; AMCVS_4D6368F454EC41940A4C98A6@AdobeOrg=1; AMCV_4D6368F454EC41940A4C98A6@AdobeOrg=-2121179033|MCIDTS|19099|MCMID|32878644913999694462843260481025795088|MCAAMLH-1650801945|11|MCAAMB-1650801945|RKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y|MCOPTOUT-1650204345s|NONE|MCAID|NONE|MCCIDH|-1574561161|vVersion|5.3.0; cra-ch-clearance=6fd507e13bdb1985:36306431363061343166306365393031393564653362626232396333373665303530613330626665656532386132353439623239633433653634393135363361316635613633323961643564333466653965646436373a313430623935346161613861343235353538623632383633; __cf_bm=JRRwfngC70Gos6FA9fBCwsMMJ80EA6MqhCLXllLH9xs-1650203659-0-AV4o+YbAqEsI+lEGWbQdz1ha2NwdybHk4ifT+Vu+eIWXiAhql6KoQa3IIjiHeKgjoHO2xZedVZ+hVMPF8CYCczOy2k8tkGXeJNRLwsm3vMhL; sd_access=eyJlbmMiOiJBMTI4Q0JDLUhTMjU2IiwiYWxnIjoiZGlyIn0..5IkaU1QL9mnhMMcR1LojBQ.Ahvhv4_6mQsz2UtE8_LJvPrcDBbsk_HSpaG0z6qU5FPKyex82raJxNbKc83WnGIlT-JhjdAOeZhEv5qmeLnE68NMnh4tiqQwIeVnTwPOTqZR6BKfTHenTfR2MWm5yIyMhs-JpeRf5hiJ24mNFFiUqw.sfe2mG-Emr8Cjxc1Ng7ktQ; MIAMISESSION=194e106d-1a17-4a6f-8124-1829c6d60422:3827656754; SD_REMOTEACCESS=eyJhY2NvdW50SWQiOiI2MTE0NyIsInRpbWVzdGFtcCI6MTY1MDIwMzk1NDY4OX0=; mbox=session#5abc3c003cf341249e26571a6e07d866#1650205815|PC#6d76aa97a54f4d00886a02058d55f239.34_0#1713448755; s_pers= c19=sd%3Aproduct%3Ajournal%3Aarticle|1650205759400; v68=1650203954708|1650205759464; v8=1650203959484|1744811959484; v8_s=Less%20than%201%20day|1650205759484;; s_sess= s_cpc=0; s_sq=; s_ppvl=sd%253Aproduct%253Ajournal%253Aarticle%2C1%2C1%2C150%2C1440%2C150%2C1440%2C900%2C1%2CP; e41=1; s_cc=true; s_ppv=sd%253Aproduct%253Ajournal%253Aarticle%2C4%2C2%2C1042%2C1440%2C150%2C1440%2C900%2C1%2CP;",
                  # "accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
    }


        req=urllib.request.Request(url,headers=headers)
        redirect_url=urllib.request.urlopen(req).geturl()
        # print("redirectt_url:",redirect_url)
        redirect_url_split=redirect_url.split("https://linkinghub.elsevier.com/retrieve/")
        # print("split:",redirect_url_split)
        now_url="https://www.sciencedirect.com/science/article/"+redirect_url_split[1]
        #now_url="https://www.sciencedirect.com/science/article/pii/S187705091830231X"
        print("now_url:",now_url)
        redirect=urllib.request.Request(now_url,headers=headers)
        redirect_res=urllib.request.urlopen(redirect)


        html = redirect_res.read().decode("utf-8", "ignore")
        # print("html:",html)
        #存放文章信息字典
        paper_info_dict={}
        selector = etree.HTML(html)
        # abss0002
        script=selector.xpath("//script[@type='application/json' and @data-iso-key='_0']/text()")
        citation_publication_date=selector.xpath("//meta[@name='citation_publication_date']/@content")
        citation_article_type=selector.xpath("//meta[@name='citation_article_type']/@content")
        citation_type=selector.xpath("//meta[@name='citation_type']/@content")
        citation_journal_title=selector.xpath("//meta[@name='citation_journal_title']/@content")
        paper_info_dict["title"] = title
        paper_info_dict["journal"] = journal
        paper_info_dict["url"] = now_url
        paper_info_dict["Year"] = year
        # paper_info_dict["citation_publication_date"]=citation_publication_date[0]
        # paper_info_dict["citation_article_type"]=citation_article_type[0]
        # paper_info_dict["citation_type"]=citation_type[0]
        # paper_info_dict["citation_journal_title"]=citation_journal_title[0]
        paper_info_dict["keywords"] = []
        paper_info_dict["abstract"] = ""
        paper_info_dict["author"] = []
        paper_info_dict["author_location"] = []


        # print("citation_publication_date:", citation_publication_date)
        # print("citation_article_type",citation_article_type)
        # print("citation_type:",citation_type)
        # print("citation_journal_title:",citation_journal_title)
        json_page = json.loads(script[0])
        print("script:",script)
        # finalfile.write("script:",script)
        # finalfile.write('\n')
    #-------------------获取作者与其所属机构----------------------------------
        print("json_author_aff:", json_page['authors']['content'][0]['$$'])
        author_list=[]
        aff_list=[]
        for item in json_page['authors']['content'][0]['$$']:
            # print("item:", item)
            if item["#name"] == "author":
                tmp_name = ""
                # print("item[$$]:",item["$$"])
                for name in item["$$"]:
                    if "#name" in name.keys() and name["#name"].find("name")!=-1 and "_" in name.keys():
                        tmp_name+=name["_"]
                        # print("name:",name["_"])
                # print("tmp_name:",tmp_name)
                author_list.append(tmp_name)
            if item["#name"] =="affiliation":
                for aff in item["$$"]:
                    # print("aff:", aff)
                    if "#name" in aff.keys() and "_" in aff.keys() and aff['#name'] == 'textfn':
                        # print("aff:",aff["_"])
                        aff_list.append(aff['_'])
                    elif '$$' in aff.keys() and aff['$$'][0]['#name']=='__text__':
                        print("aff_loc:", aff['$$'][0]['_'])
                        aff_list.append(aff['$$'][0]['_'])

        print("author_list:",author_list)
        print("author_location:", aff_list)
        paper_info_dict["author"]=author_list
        paper_info_dict["author_location"] = aff_list
        #-------------获取摘要----------------------------
        # print("json_abstract:", json_page['abstracts']["content"])
        abstract = ""
        if "content" not in json_page['abstracts'].keys():
            continue
        for item in json_page['abstracts']["content"]:
            # print("abstract_item:",item)
            for item2 in item["$$"]:
                # print("item2:",type(item2),item2)
                if "#name" in item2.keys() and item2["#name"] == "abstract-sec":
                    if (isinstance(item2["$$"][0], dict)) and "$$" not in item2["$$"][0].keys():
                        # print("normal:",item2["$$"][0]["_"])
                        abstract = item2["$$"][0]["_"]
                    else:
                        # print(item2["$$"][0]["$$"])
                        special_abs = ""
                        for text in item2["$$"][0]["$$"]:
                            if "#name" in text.keys() and text["#name"] == "__text__":
                                special_abs += text["_"]
                        # print("special:",special_abs)
                        abstract = special_abs
        print("abstravt:", abstract)
        paper_info_dict["abstract"] = abstract
    # -------------获取关键词----------------------------
        keywords_list = []
        if "content" in json_page["combinedContentItems"]:

            # print("keywords:",json_page["combinedContentItems"]["content"],type(json_page["combinedContentItems"]["content"]))
            for item in json_page["combinedContentItems"]["content"]:
                if "#name" in item.keys() and item["#name"] == "keywords":
                    # print("$$:",len(item["$$"]))
                    keywords_dict = item["$$"][0]["$$"]
                    for item2 in keywords_dict:
                        if "$$" in item2.keys() and "_" in item2["$$"][0].keys():
                            # print("item2:", item2["$$"][0]["_"])
                            keywords_list.append(item2["$$"][0]["_"])
                        # if item2["#name"] == "keyword":
            print("keywords_list:", keywords_list)
            paper_info_dict["keywords"] = keywords_list

    #------- 写入文件---------
        print("paper_info:",paper_info_dict)
        paper_json=json.dumps(paper_info_dict)
        finalfile.write(paper_json+"\n")
        finalfile.write('---------------------------------\n')
        print("success")
        # finalfile.write()
    # except:
    #     print("error occur")
    #     str1 = list[i].split('ee:')[1]
    #
    #     url = str1.split('\n')[0]
    #
    #     str2 = list[i].split('title:')[1]
    #     title = str2.split('\n')[0]
    #
    #     str3 = list[i].split('Year:')[1]
    #     year = str3.split('\n')[0]
    #
    #     str4 = list[i].split('journal:')[1]
    #     journal = str4.split('\n')[0]
    #
    #     errorfile.write("ee:" + url + "\n")
    #     errorfile.write("title:"+title+"\n")
    #     errorfile.write("Year:"+year+"\n")
    #     errorfile.write("journal:"+journal+"\n")
    #     errorfile.write('---------------------------------\n')
finalfile.close()
# errorfile.close()




