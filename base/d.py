def min_num(a):

    b=a[0]
    for i in range(len(a)):

        if  b >  a[i]:
            b=a[i]


    return b    
c=[-6,54,2,-34,-44]   
m=[]
while c:
    a=min_num(c)
    b=c.index(a)
    m.append(a)
    c.pop(b)
    
    
print(m)