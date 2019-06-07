import csv
from random import randint

def read_Data(fname, arr):
    inputfile = csv.reader(open(fname, 'r', encoding="utf-8"))

    num =-1
    for idx, row in enumerate(inputfile):
        print(row)
        arr.append(row[0]);

def write_Data(fname, content):
    text_file = open(fname, "a", encoding="utf-8")
    text_file.write(content+"\n")
    text_file.close()

arrFirst = []

arrSecond = []

read_Data('trainFirst.txt', arrFirst)
read_Data('trainSecond.txt', arrSecond)

count = len(arrFirst)
print(count, "-", count*0.8)
while len(arrFirst)>0.2*count:
    choose = randint(0, len(arrFirst) - 1)
    write_Data('splitTrain1.txt', arrFirst[choose])
    del arrFirst[choose]
    print("Train entry:", len(arrFirst))
for i in range(0, len(arrFirst)):
    write_Data('splitValidation1.txt', arrFirst[i])
    print("Validation entry:", i)

count = len(arrSecond)
while len(arrSecond)>0.2*count:
    choose = randint(0, len(arrSecond) - 1)
    write_Data('splitTrain2.txt', arrSecond[choose])
    del arrSecond[choose]
    print("Train entry:", len(arrSecond))

for i in range(0, len(arrSecond)):
    write_Data('splitValidation2.txt', arrSecond[i])
    print("Validation entry:", i)

