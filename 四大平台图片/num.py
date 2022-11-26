
r = []
i = 0
for l in open('p4.txt'):
    print(l)
    print(l.split('Num:'))
    r.append(l.split('Num: ')[1].split('\n')[0])
    i = i+1

print(r)
