#!/usr/bin/python
# -*- coding: UTF-8 -*-
#将fullwork中的内容按关键词提取数据

def title_match(input_file_path,output_file_path):
    print("first filter start")
    caculate = {}
    cnt = 0
    keywords=["metaverse"]
    with open(input_file_path, 'r') as ww:

        str=ww.read()

        lst=str.split('---------------------------------\n')

        #print(lst)

        newlst=[];
        mark = 0

        for i in range(0,len(lst)):
            mark = 0
            if "title:" in lst[i]:
                title = (lst[i].split("title:"))[1]
                title = title.split("\n")[0]
                for s in keywords:
                    if s.lower() in title.lower() and mark ==0:
                        print(title)
                        newlst+=('---------------------------------\n')+lst[i]
                        mark = 1
                        if s not in caculate.keys():
                            caculate.setdefault(s,1)

                        else:
                            caculate[s]=caculate[s]+1
                        cnt = cnt +1

    print(sorted(caculate.items(), key=lambda x: x[1], reverse=True))
    print(cnt)
    with open(output_file_path, 'w+') as rr:
        rr.write(''.join(newlst))
    print("first filter close")
    return output_file_path




