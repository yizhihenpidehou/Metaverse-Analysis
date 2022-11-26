# 声明一个空字典，来保存文本文件数据
dict_temp = {}

# 打开文本文件
file = open('topic1.txt','r')

# 遍历文本文件的每一行，strip可以移除字符串头尾指定的字符（默认为空格或换行符）或字符序列
for line in file.readlines():
    line = line.strip()
    k = line.split(':')[0]
    v = line.split(':')[1]
    dict_temp[k] = v

# 依旧是关闭文件
file.close()

#  可以打印出来瞅瞅
print(dict_temp.keys())


