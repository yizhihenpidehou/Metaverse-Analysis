target_ff=open("11月first_keywords_filter.txt", 'r')
target_ff_str=target_ff.read()
target_ff_lst=target_ff_str.split("---------------------------------\n")

old_ff=open("first_filtered_all.txt",'r')
old_ff_str=old_ff.read()
old_ff_lst=old_ff_str.split("---------------------------------\n")
old_ff_title_lst=[]
for i in range(0,len(old_ff_lst)):
    title = old_ff_lst[i].split("title:")[1].split("\n")[0]
    old_ff_title_lst.append(title)

sr_ff=open("11月新增爬取数据.txt",'w')
count=0
for i in range(0,len(target_ff_lst)):
    title=target_ff_lst[i].split("title:")[1].split("\n")[0]
    if title not in old_ff_title_lst:
        sr_ff.write(target_ff_lst[i])
        sr_ff.write("---------------------------------\n")
        old_ff_title_lst.append(title)
        count+=1
print("count:",count)
target_ff.close()
old_ff.close()
sr_ff.close()

# article_ff=open("article_extracted.txt",'r')
# inproceedings_ff=open("inproceedings_extracted.txt", 'r')
# article_ff_str=article_ff.read()
# article_ff_lst=article_ff_str.split("---------------------------------\n")
# inproceedings_ff_str=inproceedings_ff.read()
# inproceedings_ff_lst=inproceedings_ff_str.split("---------------------------------\n")
# title_lst=[]
# for i in range(0,len(article_ff_lst)):
#     title = (article_ff_lst[i].split("title:"))[1]
#     title = title.split("\n")[0]
#     if title not in title_lst:
#         title_lst.append(title)
# for i in range(0,len(inproceedings_ff_lst)):
#     title = (inproceedings_ff_lst[i].split("title:"))[1]
#     title = title.split("\n")[0]
#     if title not in title_lst:
#         title_lst.append(title)
# print("total num:",len(title_lst))
# article_ff.close()
# inproceedings_ff.close()