
import json
from wordcloud import WordCloud
from nltk.corpus import stopwords
second_filtered_dataset=open("../crawl_result_merge.json","r")
second_filtered_dataset_str=second_filtered_dataset.read()
second_filtered_dataset_lst=second_filtered_dataset_str.split("---------------------------------\n")
total_abstract=open("total_abstract.txt","w")

#拼接每个阶段的摘要
for i in range(0,len(second_filtered_dataset_lst)-1):#len(merge_lst)
    line=json.loads(second_filtered_dataset_lst[i])
    abstract=line["abstract"]
    total_abstract.write(abstract+"\n")
    print("abstract",abstract)
total_abstract.close()
total_abstract=open("total_abstract.txt","r")

stop_words = stopwords.words('english')
stop_words.extend(['from', 'use', 'present', 'play', 'can','find','used','uses','using','design','paper','time','two'
                   ,'however','also','many','well','new','based','user','users','data','method','information','propose',
                   'provide','research','approach','problem','based','proposed','result','results','need','way','show',
                   'help','different','study','process','e g','within','become','order','finally','make','related',
                   'one','number','may','demostrate','methods','set','improve'])

abstract_wordcloud=WordCloud(width=1024,height=768,background_color="white",stopwords=stop_words,max_words=80).generate(total_abstract.read().lower()
                                                                                       )
abstract_wordcloud.to_file("total_abstract.jpg")
second_filtered_dataset.close()
total_abstract.close()
