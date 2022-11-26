import os,sys
from pathlib import Path
from crawlers import citation_crawler
from xml2txt import xml2txt_article,xml2txt_inproceedings,xml2txt_all
from firstFilter import first_keywords_filter
from publisher_divide import classify
from convert import get_author
from author_cooperation import author_nx
from citation import cal_citation
from gender import local_assortativity,gender_diversity
from venueAnalysis import findvenue
abs_file_path=os.path.abspath(sys.argv[0])
print("当前pipleline绝对路径:",abs_file_path)
print(Path(os.path.abspath('.')))
dblp_file_dir=Path(os.path.abspath('.'))/"xml2txt"
dblp_file_lst=sorted(list(str(x) for x in dblp_file_dir.glob("dblp-2022-*.xml")))
print("dblp_file_lst:",dblp_file_lst)
baseurl='/Users/yizhihenpidehou/Desktop/fdu/Metaverse-Analysis/'
def merge_txt(f1,f2,res_file_path):
    ff1=open(f1,'r')
    ff2=open(f2,'r')
    ff1_str=ff1.read()
    ff2_str=ff2.read()
    ff1_lst=ff1_str.split('---------------------------------\n')
    ff2_lst=ff2_str.split('---------------------------------\n')
    res_file=open(res_file_path,'w')
    for i in range(1,2):
        if len(ff1_lst[i]) == 0 or len(ff1_lst[i].split('ee:'))<2:
            continue
        res_file.write(ff1_lst[i])
        res_file.write('---------------------------------\n')
    for i in range(0,len(ff2_lst)):
        if len(ff2_lst[i]) == 0 or len(ff2_lst[i].split('ee:'))<2:
            continue
        res_file.write(ff2_lst[i])
        res_file.write('---------------------------------\n')
    ff1.close()
    ff2.close()
    res_file.close()
    return res_file_path
# merge_txt(baseurl+'firstFilter/article.txt',baseurl+'firstFilter/inproceedings.txt',baseurl+'firstFilter/test.txt')

def start_pipleline():
    for i in range(10,len(dblp_file_lst)):
        dblp_path=dblp_file_lst[i]
        mouth=dblp_path.split("dblp-")[1].split('.xml')[0]
        local_path=Path(baseurl+mouth)
        if local_path.is_dir() == False:
            os.mkdir(local_path)
        local_path=str(local_path)+'/'
        #
        xml_dblp_res_path=local_path+"dblp_all"+mouth+".txt"
        # xml_dblp_res_path=xml2txt_all.start(dblp_path,xml_dblp_res_path)
        firstfilter_all_output_path = local_path + "dblp_extracted" + mouth + ".txt"
        # firstfilter_all_output_path = first_keywords_filter.title_match(xml_dblp_res_path,firstfilter_all_output_path)

        # '''
        # article_res_path=baseurl+"xml2txt/article"+mouth+".txt"
        # inproceedings_res_path=baseurl+"xml2txt/inproceedings"+mouth+".txt"
        # #从dblp.xml中拉取article、inproceedings数据
        # xml_article_res_path=xml2txt_article.start(dblp_path,article_res_path)
        # xml_inproceedings_res_path=xml2txt_inproceedings.start(dblp_path,inproceedings_res_path)
        #
        # # 按照文章标题对dblp.xml拉下的数据进行初筛
        # firstfilter_article_output_path=local_path+"firstFilter/article_extracted"+mouth+".txt"
        # firstfilter_inproceedings_output_path = local_path+"firstFilter/inproceedings_extracted"+mouth+".txt"
        # firstfilter_article_output_path=first_keywords_filter.title_match(xml_article_res_path,firstfilter_article_output_path)
        # firstfilter_inproceedings_output_path=first_keywords_filter.title_match(xml_inproceedings_res_path,firstfilter_inproceedings_output_path)
        #
        # #将article和inproceedings文件进行合并
        # first_filter_all_path=local_path+'first_filtered_all'+mouth+'.txt'
        # first_filter_all_path=merge_txt(firstfilter_article_output_path,firstfilter_inproceedings_output_path,first_filter_all_path)
        # '''
        # # 将初筛数据按照出版商进行分类，并且标上source
        fourpublisher_arxiv_withsource_path=local_path+'fourpublisher_arxiv_updatedauthor'+mouth+'.txt'
        # fourpublisher_arxiv_withsource_path=classify.start_classify(firstfilter_all_output_path,fourpublisher_arxiv_withsource_path)

        # 将dblp拉下来分散的作者格式转变为作者列表
        fourpublisher_arxiv_withsource_updatedauthor_path=local_path+'fourpublisher_arxiv_withsource_updatedauthor'+mouth+'.json'
        # fourpublisher_arxiv_withsource_updatedauthor_path=get_author.authors2list(fourpublisher_arxiv_withsource_path,fourpublisher_arxiv_withsource_updatedauthor_path)

        # 启动爬虫,爬取文章的citation
        fourpublisher_arxiv_withsource_updatedauthor_citation_path=local_path+'fourpublisher_arxiv_withsource_updatedauthor_citation'+mouth+'_final.json'
        # fourpublisher_arxiv_withsource_updatedauthor_citation_path=citation_crawler.start_crawl_citation(fourpublisher_arxiv_withsource_updatedauthor_path,fourpublisher_arxiv_withsource_updatedauthor_citation_path)
        # 对爬下来的作者信息做指标分析
        res_dict=author_nx.author_analysis_pipeline(inputpath=fourpublisher_arxiv_withsource_updatedauthor_citation_path,graphpath=local_path+'fourpublisher_arxiv_collaboration')
        # print("author_nx HIS:",res_dict["HIS"])
        # 对爬下来的citation做指标分析
        # cal_citation.citation_analysis_pipeline(inputpath=fourpublisher_arxiv_withsource_updatedauthor_citation_path,graphpath=local_path+'fourpublisher_arxiv_citation_distribution')

        # 对性别做分析
        # gender_analysis.gender_pipeline(inputpath=fourpublisher_arxiv_withsource_updatedauthor_citation_path)
        # local_assortativity.local_assortativity_pipleline(inputpath=fourpublisher_arxiv_withsource_updatedauthor_citation_path,respath=local_path+"local_assortativity"+mouth+'.png')
        gender_diversity.gender_diversity_pipleline()

        # 统计vuenue
        findvenue.get_vuenues(inputpath=fourpublisher_arxiv_withsource_updatedauthor_path)
start_pipleline()

