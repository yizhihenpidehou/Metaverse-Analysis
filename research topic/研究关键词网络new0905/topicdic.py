


with open('yakeRes3(完整版).txt','r') as ww:

    splist = [".","'"]
    str=ww.read()

    lst=str.split('\n')

    resdic = {}
    reslst=[]
    for i in lst:
        if(i != ''):
            print('i:'+i)
            tpc = i.split(':')[0]
            num = i.split(':')[1]
            reslst.append(tpc)
            resdic.setdefault(tpc,'')
            resdic[tpc] = num


print(resdic)
print(reslst)