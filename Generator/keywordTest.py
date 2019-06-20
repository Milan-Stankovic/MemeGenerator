import gensim
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import STOPWORDS
import numpy as np
from gensim import corpora, models
from pprint import pprint
from itertools import chain
from gensim.summarization import keywords
import random
import csv
import nltk
from random import randint

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

def read_Data(fname, arr):
    inputfile = csv.reader(open(fname, 'r', encoding="utf-8"))

    num =-1
    for idx, row in enumerate(inputfile):
        if idx %2 ==0:
            num =num+1
            arr.append(row);

def write_Data(fname, content):
    text_file = open(fname, "a", encoding="utf-8")
    text_file.write(content+"\n")
    text_file.close()


def write_CSV(savefile, txt):

    with open(savefile, 'a', encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(txt)
        '''for i in range(0,2):
            print("Row{", i, "] = ", txt[i])
            writer.writerow(txt[i])'''

def extractType(tokens, type, mode):
    retVal = []
    for idx in range(0, len(tokens)):
        if (tokens[idx][1][0] == type) == mode:
            temp = []
            temp.append(idx)
            temp.append(tokens[idx][0])
            retVal.append(temp)

    return retVal

def extractNonPunctuaction(tokens):
    retVal = []
    for idx in range(0, len(tokens)):
        if tokens[idx][1] != "''" and tokens[idx][1][0] != 'N' and tokens[idx][1][0] != 'V' and tokens[idx][1][0] != '.' and tokens[idx][1][0] != ':' and tokens[idx][1] != '``' and tokens[idx][1][0] != ',':
            temp = []
            temp.append(idx)
            temp.append(tokens[idx][0])
            retVal.append(temp)

    return retVal

def splitEntry(entry, label, splits, firstWordsIgnore):
    retVal = []
    frontSet = []
    backSet = []
    tempR = 0
    tokens = nltk.word_tokenize(text)
    posTokens = nltk.pos_tag(tokens)

    verbs = extractType(posTokens, 'V', True);
    nouns = extractType(posTokens, 'N', True);
    nonPunctuation = extractNonPunctuaction(posTokens);

    #print("--------------------------------------------------------------------------------------------------------------")
    #print("POS: ", posTokens)
    #print(entry)
    #print("Tokens: ", tokens)
    #print("Verbs: ", verbs)
    #print("Nouns: ", nouns)
    #print("NonP: ", nonPunctuation)


    while splits>0 and (len(verbs)>0 or len(nouns)>0 or len(nonPunctuation)>0):
        #print("Splits: ", splits, "LENS: v - ", len(verbs), " n - ", len(nouns), " nP - ", len(nonPunctuation))
        splitStr = ""
        if len(verbs)>0:
            choose = randint(0, len(verbs)-1)
            #print("BIRAM VERB: ", choose)
            if verbs[choose][0] >= firstWordsIgnore and verbs[choose][0] < len(posTokens)-1 and len(verbs[choose][1]) > 3:
                splitStr = verbs[choose]
                splits = splits - 1
            else:
                print("")#print("FALSE Split str", verbs[choose])
            del verbs[choose]
        elif len(nouns)>0:
            choose = randint(0, len(nouns)-1)
            #print("BIRAM NOUN: ", choose)
            if nouns[choose][0] >= firstWordsIgnore and nouns[choose][0]<len(posTokens)-1 and len(nouns[choose][1]) > 3:
                splitStr = nouns[choose]
                splits = splits - 1
            else:
                print("")#print("FALSE Split str", nouns[choose])
            del nouns[choose]
        elif len(nonPunctuation)>0:
            choose = randint(0, len(nonPunctuation)-1)
            #print("BIRAM NONPUN: ", choose)
            if nonPunctuation[choose][0] >= firstWordsIgnore and nonPunctuation[choose][0]<len(posTokens)-1 and len(nonPunctuation[choose][1]) > 3:
                splitStr = nonPunctuation[choose]
                splits = splits - 1
            else:
                print("")#print("FALSE Split str", nonPunctuation[choose])
            del nonPunctuation[choose]
        #print("Split str", splitStr)
        if splitStr:
            temp = entry.split(splitStr[1], 1)
            #print(temp)
            write_CSV("trainFirst.csv", [label, entry])
            write_CSV("trainSecond.csv", [label, (splitStr[1] + temp[1])[::-1]])
            write_CSV("splitSet.csv", [label, splitStr[1]])

    #print("LENS: v - ", len(verbs), " n - ", len(nouns), " nP - ", len(nonPunctuation))

    #print("Verbs: ", verbs)
    #print("Nouns: ", nouns)
    #print("NonP: ", nonPunctuation)
    print("--------------------------------------------------------------------------------------------------------------")
    if splits > 0:
        tempR+=1
    #print("TEMP: ", tempR)
    return tempR

noNoThreeSplits = 0

arr1=[]
read_Data('testData.csv', arr1)

nlCount = 0

for i in range(len(arr1)):
    print(arr1[i])
    text = arr1[i][1]
    label = arr1[i][0]
    text = text.replace('\n', '')
    noNoThreeSplits += int(splitEntry(text, label, 3, 2))

arr1=[]
read_Data('trainData.csv', arr1)

for i in range(0, len(arr1)):
    print(arr1[i])
    text = arr1[i][1]
    label = arr1[i][0]
    text = text.replace('\n', '')
    noNoThreeSplits += int(splitEntry(text, label, 4, 2))

print("NONO3SPLITS: ", noNoThreeSplits)


