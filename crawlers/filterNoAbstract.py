import json
uncertain_file=open("11新增/ieee_res3.json", 'r')
uncertain_str=uncertain_file.read()
uncertain_lst=uncertain_str.split("---------------------------------\n")
#重爬的存起来
recrawl_file=open("11新增/11月ieee4.txt",'w')
#目前信息完整的数据
ieee_res_file=open("11新增/ieee_res3_final.json",'w')
count=0
count_uncrawl=0
for i in range(0,len(uncertain_lst)-1):
    print('第',i,"uuu:",uncertain_lst[i])
    file_json=json.loads(uncertain_lst[i])
    abstract=file_json["abstract"]
    author=file_json["author"]
    if abstract == 'not found' or len(author)==0 or author[0]=='no_name':
        count_uncrawl+=1
        # recrawl_file.write(json.dumps(file_json) + '\n')
        # recrawl_file.write("---------------------------------\n")
        # print(uncertain_lst[i])
        title = file_json["title"]
        year=file_json["date"]
        ee=file_json["link"]
        publish=file_json["publish"]
        recrawl_file.write("title:"+title+'\n')
        recrawl_file.write("Year:"+year+'\n')
        recrawl_file.write("journal:"+publish+'\n')
        recrawl_file.write("ee:"+ee+'\n')
        recrawl_file.write("---------------------------------\n")

    # else:
    else:
        count += 1
        ieee_res_file.write(json.dumps(file_json)+'\n')
        ieee_res_file.write("---------------------------------\n")
print("count:",count)
print("uncrawl_count:",count_uncrawl)
ieee_res_file.close()
recrawl_file.close()
