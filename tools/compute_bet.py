import pdb

while(1):
    str = input("Enter your input: ")
    total_money = float(str.split(' ')[0])
    odd1 = float(str.split(' ')[1])
    odd2 = float(str.split(' ')[2])
    prop1 = 1/odd1
    prop2 = 1/odd2
    propotion1 = prop1/(prop1+prop2)
    propotion2 = 1 - propotion1
    print("赔率1：%s，赔率2：%s" % (total_money*propotion1, total_money*propotion2))