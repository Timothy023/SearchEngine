import os
import jieba
import numpy as np
import math

dic = {}
s = {}
lst = [{}for i in range(65000)]
lenght = {}
ans = {}
q = []
cnt = int(0)
sumfile = int(0)
NumToUrl = {}

def judge(word) :
    if word == '，' or word == '；' or word == '——' or word == '。' or word == '：' or  \
       word == '（' or word == '）' or word == '/' or word == '.' or word == '！' or word == '．' or \
       word == '@' or word == '、' :
        return True
    else :
        return False

def solveFile(id) :
    global dic
    global lst
    global cnt
    global sumfile

    dicp = {}
    dicp.clear()

    path = './divided_body/' + str(id)
    if not os.path.exists(path) :
        return
    fin = open(path, 'r', encoding = 'utf-8')
    data = fin.read()
    for word in data.split() :
        if judge(word) :
            continue
        if dic.get(word, -1) == -1 :
            cnt = cnt + 1
            dic[word] = cnt
            s[cnt] = 0;
        p = dic[word]
        if dicp.get(word, -1) == -1 :
            dicp[word] = 1
            lst[p][id] = 0
            s[p] = s[p] + 1
        lst[p][id] += 1
    fin.close()
    
    path = './divided_title/' + str(id)
    if not os.path.exists(path) :
        return
    sumfile = sumfile + 1
    fin = open(path, 'r', encoding = 'utf-8')
    data = fin.read()
    for word in data.split() :
        if judge(word) :
            continue
        if dic.get(word, -1) == -1 :
            cnt = cnt + 1
            dic[word] = cnt
            s[cnt] = 0;
        p = dic[word]
        if dicp.get(word, -1) == -1 :
            dicp[word] = 1
            lst[p][id] = 0
            s[p] = s[p] + 1
        lst[p][id] += 1
    fin.close()

def makeDictionary() :
    for i in range(1, 6796) :
        solveFile(i)

def makeUrl() :
    html = open("./Reflect")
    data = html.readlines()
    for line in data : 
        list = []
        for word in line.split() :
            list.append(word)
        url = ''
        id = int(0)
        for i in range (0, list.__len__(), 1) :
            if i + 1 != list.__len__() :
                url = url + list[i]
            else :
                id = int(list[i])
        NumToUrl[id] = url
    html.close

def presolveQuery() :
    query = 'ACM'
    ans.clear()
    seg_list = jieba.cut_for_search(query)
    q.clear()
    for word in seg_list :
        q.append(word)
    for i in range(1, 6796) :
        tmp = int(0)
        for j in range(0, len(q)) :
            word = q[j]
            if dic.get(word, -1) == -1 :
                continue
            id = dic[word]
            if lst[id].get(i, -1) == -1 :
                continue
            tmp += (1 + np.log10(lst[id][i])) * np.log10(sumfile / s[id])
        if tmp != 0 :
            ans[i] = tmp

def solveQuery() :
    query = input()
    ans.clear()
    seg_list = jieba.cut_for_search(query)
    q.clear()
    for word in seg_list :
        q.append(word)
    for i in range(1, 6796) :
        tmp = int(0)
        for j in range(0, len(q)) :
            word = q[j]
            if dic.get(word, -1) == -1 :
                continue
            id = dic[word]
            if lst[id].get(i, -1) == -1 :
                continue
            tmp += (1 + np.log10(lst[id][i])) * np.log10(sumfile / s[id])
        if tmp != 0 :
            ans[i] = tmp
    sumurl = 0
    for detial in sorted(ans.items(), key = lambda kv:kv[1], reverse = True) :
        sumurl = sumurl + 1
        if (sumurl > 10) :
            break
        print(detial, '  url = ', NumToUrl[detial[0]])
        

print('Please wait...')
makeDictionary()
makeUrl()
for i in range (1, 10) :
    presolveQuery()

while 1 :
    print('Tell me what you want.')
    solveQuery()