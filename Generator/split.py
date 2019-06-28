import csv
from random import randint

memeCount = 15

likeValues = []
maxValues = []
avgValues = []
faktorValues =[]


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

def goThroughAll(fname):

    inputfile = csv.reader(open(fname, 'r', encoding="utf-8"))

    for idx, row in enumerate(inputfile):
        if idx % 2 == 0 :
            print("Reading ", idx, " = ", row)
            if row[0] == 'ONE_DOES_NOT_SIMPLY':
                likeValues[0].append(int(row[3]))
            if row[0] == 'MOST_INTERESTING_MAN':
                likeValues[1].append(int(row[3]))
            if row[0] == 'SUCCESS_KID':
                likeValues[2].append(int(row[3]))
            if row[0] == 'BAD_LUCK_BRIAN':
                likeValues[3].append(int(row[3]))
            if row[0] == 'GOOD_GUY_GREG':
                likeValues[4].append(int(row[3]))
            if row[0] == 'FOREVER_ALONE':
                likeValues[5].append(int(row[3]))
            if row[0] == 'ALL_THE_THINGS':
                likeValues[6].append(int(row[3]))
            if row[0] == 'YO_DAWG':
                likeValues[7].append(int(row[3]))
            if row[0] == 'CONSPIRACY_KEANU':
                likeValues[8].append(int(row[3]))
            if row[0] == 'WILLY_WONKA':
                likeValues[9].append(int(row[3]))
            if row[0] == 'WINTER_IS_COMING':
                likeValues[10].append(int(row[3]))
            if row[0] == 'FUTURAMA_FRY':
                likeValues[11].append(int(row[3]))
            if row[0] == 'Y_U_NO':
                likeValues[12].append(int(row[3]))
            if row[0] == 'KERMIT_THE_FROG':
                likeValues[14].append(int(row[3]))
            if row[0] == 'WHAT_IF_I_TELL_YOU':
                likeValues[14].append(int(row[3]))

def grupByType(fname):

    inputfile = csv.reader(open(fname, 'r', encoding="utf-8"))

    for idx, row in enumerate(inputfile):
        if idx % 2 == 0 :
            print("Reading ", idx, " = ", row)
            if row[0] == 'ONE_DOES_NOT_SIMPLY':
                list_OneDoes.append(row[1])
            if row[0] == 'MOST_INTERESTING_MAN':
                list_MostInterest.append(row[1])
            if row[0] == 'SUCCESS_KID':
                list_Success_KID.append(row[1])
            if row[0] == 'BAD_LUCK_BRIAN':
                list_BadLuck.append(row[1])
            if row[0] == 'GOOD_GUY_GREG':
                list_GoodGuy.append(row[1])
            if row[0] == 'FOREVER_ALONE':
                list_ForeverAlone.append(row[1])
            if row[0] == 'ALL_THE_THINGS':
                list_AllTheThings.append(row[1])
            if row[0] == 'YO_DAWG':
                list_YoDawg.append(row[1])
            if row[0] == 'CONSPIRACY_KEANU':
                list_Keanau.append(row[1])
            if row[0] == 'WILLY_WONKA':
                list_Willy.append(row[1])
            if row[0] == 'WINTER_IS_COMING':
                list_Winter.append(row[1])
            if row[0] == 'FUTURAMA_FRY':
                list_Futurama.append(row[1])
            if row[0] == 'Y_U_NO':
                list_YUN.append(row[1])
            if row[0] == 'KERMIT_THE_FROG':
                list_Kermit.append(row[1])
            if row[0] == 'WHAT_IF_I_TELL_YOU':
                list_WhatIF.append(row[1])

def splitMeme(listMeme, fname1, fname2):
    for i in range(len(listMeme)):
        if i < 0.8*len(listMeme):
            write_Data(fname1, listMeme[i])
        else:
            write_Data(fname2, listMeme[i])



numberOfMemes= []

for i in range(0, memeCount):
    likeValues.append(0)
    likeValues[i] = []

def findAvgAndMax():
    for i in range(0, memeCount):
        avgValues.append(int(sum(likeValues[i])/len(likeValues[i])))
        maxValues.append(max(i for  i in likeValues[i]))
        faktorValues.append(int(maxValues[i]/avgValues[i]))
        numberOfMemes.append(len(likeValues[i]))



list_OneDoes = []
list_MostInterest = []
list_Success_KID = []
list_BadLuck = []
list_GoodGuy = []
list_ForeverAlone = []
list_AllTheThings = []
list_YoDawg = []
list_Keanau = []
list_Willy = []
list_Winter = []
list_Futurama = []
list_YUN = []
list_Kermit = []
list_WhatIF = []

arrSecond = []

grupByType('trainSecond.csv')


splitMeme(list_OneDoes, 'splitTrain2.txt', 'splitValidaton2.txt')
splitMeme(list_MostInterest, 'splitTrain2.txt', 'splitValidaton2.txt')
splitMeme(list_Success_KID, 'splitTrain2.txt', 'splitValidaton2.txt')
splitMeme(list_BadLuck, 'splitTrain2.txt', 'splitValidaton2.txt')
splitMeme(list_GoodGuy, 'splitTrain2.txt', 'splitValidaton2.txt')
splitMeme(list_ForeverAlone, 'splitTrain2.txt', 'splitValidaton2.txt')
splitMeme(list_AllTheThings, 'splitTrain2.txt', 'splitValidaton2.txt')
splitMeme(list_YoDawg, 'splitTrain2.txt', 'splitValidaton2.txt')
splitMeme(list_Keanau, 'splitTrain2.txt', 'splitValidaton2.txt')
splitMeme(list_Willy, 'splitTrain2.txt', 'splitValidaton2.txt')
splitMeme(list_Winter, 'splitTrain2.txt', 'splitValidaton2.txt')
splitMeme(list_Futurama, 'splitTrain2.txt', 'splitValidaton2.txt')
splitMeme(list_YUN, 'splitTrain2.txt', 'splitValidaton2.txt')
splitMeme(list_Kermit, 'splitTrain2.txt', 'splitValidaton2.txt')
splitMeme(list_WhatIF, 'splitTrain2.txt', 'splitValidaton2.txt')




