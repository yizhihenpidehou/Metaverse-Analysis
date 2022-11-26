import json
from collections import defaultdict
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from nltk.corpus import stopwords
second_filtered_dataset=open("../fourpublisher_arxiv_crawl_result_updateauthors_withcountry_citation.json","r")
second_filtered_dataset_str=second_filtered_dataset.read()
second_filtered_dataset_lst=second_filtered_dataset_str.split("---------------------------------\n")
print("totlen:",len(second_filtered_dataset_lst))
year_distributed=open("yearDistributed.txt","w")
stop_words = stopwords.words('english')
stop_words.extend(['from', 'use', 'present', 'play', 'can','find','used','uses','using','design','paper','time','two'
                   ,'however','also','many','well','new','based','user','users','data','method','information','propose',
                   'provide','research','approach','problem','based','proposed','result','results','need','way','show',
                   'help','different','study','process','e g','within','become','order','finally','make','related',
                   'one','number','may','demostrate','methods','set','improve'])

# minn_date 1995
minn_date=9999
num_dict={}

for i in range(2000,2023):
    num_dict[i]=0
# num_dict["2000~2022"]=0
# num_dict["2009~2017"]=0
# num_dict["2018~2022"]=0

abstract_dict=defaultdict(int)
# abstract_dict["1995~2008"]=[]
# abstract_dict["2009~2014"]=[]
# abstract_dict["2000~2008"]=[]
# abstract_dict["2009~2017"]=[]
abstract_dict["2000~2022"]=[]
for i in range(0,len(second_filtered_dataset_lst)-1):
    print("第",i,'个')
    line=json.loads(second_filtered_dataset_lst[i])
    date=int(line["date"])
    abstract=line["abstract"]
    if date < minn_date:
        minn_date=date
    if date >= 2000 and date <= 2022:
        # num_dict["2000~2022"] += 1
        abstract_dict["2000~2022"].append(abstract)
    # if date >= 2009 and date <= 2017:
    #     num_dict["2009~2017"] += 1
    #     abstract_dict["2009~2017"].append(abstract)
    # if date >= 2018 and date <= 2022:
    #     num_dict["2018~2022"] += 1
    #     abstract_dict["2018~2022"].append(abstract)
    if date in num_dict:
        num_dict[date]=num_dict[date]+1
    else:
        num_dict[date]=1
key_list=[]
value_list=[]
for key,value in num_dict.items():
    if isinstance(key,str) == False:
        key_list.append(key)
        value_list.append(value)
print("key_list:",key_list)
print("value_list:",value_list)
plt.bar(key_list,value_list,facecolor='#ff9999')
for a,b in zip(key_list,value_list):
    plt.text(a,b,'%d'%b,ha='center',va='bottom')
plt.savefig("paperNum.png")
plt.show()

for i in range(2000,2023):
    if i in num_dict.keys():
        print(i,":",num_dict[i])
        year_distributed.write(str(i)+':'+str(num_dict[i])+"\n")
#输出最早发表文章的年份
# print("minn_date:",minn_date)
print("abstract_keys:",abstract_dict.keys(),type(abstract_dict.keys()))
file_count=1
total_abstract=""
for key,value in abstract_dict.items():
    tmp_abstract=""
    tmp_abstract_file=open("tmp_abstract"+str(file_count)+".txt","w+")
    for v in value:
        tmp_abstract+=v.lower()
        tmp_abstract_file.write(v+"\n")
        tmp_abstract_file.write("---------------------------------\n")
    abstract_wordcloud = WordCloud(width=1024, height=768, background_color="white",
                                   collocation_threshold=50,max_words=80,stopwords=stop_words).generate(tmp_abstract)
    abstract_wordcloud.to_file("total_abstract"+str(file_count)+".jpg")
    tmp_abstract_file.close()
    total_abstract+=tmp_abstract+"\n"
    file_count+=1
total_abstract_wordcloud = WordCloud(width=1024, height=768, background_color="white",
                                   collocation_threshold=50,max_words=80,stopwords=stop_words).generate(total_abstract)
# 生成总云图
total_abstract_wordcloud.to_file("total_abstract.jpg")
second_filtered_dataset.close()
year_distributed.close()