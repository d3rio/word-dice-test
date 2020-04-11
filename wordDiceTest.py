# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 14:29:31 2020

@author: d3rio
"""
from urllib import request
from nltk import word_tokenize
import numpy as np
from scipy.stats import chi2
from tabulate import tabulate
import matplotlib.pyplot as plt

# get book from Project Gutenberg
#url = "http://www.gutenberg.org/files/2554/2554-0.txt" # Crime and Punishment
#title = "Crime and Punishment"
#url = "https://www.gutenberg.org/files/1342/1342-0.txt" # Pride and Prejudice
#title = "Pride and Predudice"
#url = "https://www.gutenberg.org/files/84/84-0.txt" # Frankenstein
#title = "Frankenstein"
#url = "https://www.gutenberg.org/files/98/98-0.txt" # A Tale of Two Cities
#title = "A Tale of Two Cities"
url = "https://www.gutenberg.org/files/4300/4300-0.txt"
title = "Ulysses"

response = request.urlopen(url)
raw = response.read().decode('utf-8-sig')
tokens = word_tokenize(raw)

# filter out non-alpha characters and make all lowercase
filt_words = [w.lower() for w in tokens if w.isalpha()]
# filter out all words length 2 or less
filt_words = [w for w in filt_words if len(w)>2]
# filter out all repeats of the same word
uniq_words = []
[uniq_words.append(w) for w in filt_words if w not in uniq_words]
    
mod9List = []
mod6List = []

for I in range(len(uniq_words)):
#for I in range(1000):
    word = uniq_words[I]
    sum = 0
    for J in range(len(word)):
        sum = sum + ord(word[J])-96
    
    if np.mod(sum,9)<6: # only keep 0-5
        mod9List.append(np.mod(sum,9))
    
    mod6List.append(np.mod(sum,6))

# convert to np arrays
mod9List = np.array(mod9List)
mod6List = np.array(mod6List)

## calculate chi-squared for each list
# total number of numbers in each list
N9 = len(mod9List)
N6 = len(mod6List)

# make similar array using numpy.random.randit
randArray = np.random.randint(0,6,N6)

# expected number of rolls for each number if perfectly fair and random
expect9 = N9/6
expect6 = N6/6

# count actual number of times each number appears
mod9Num = np.zeros(6)
mod6Num = np.zeros(6)
randNum = np.zeros(6)
for I in range(6):
    mod9Num[I] = np.count_nonzero(mod9List==I)
    mod6Num[I] = np.count_nonzero(mod6List==I)
    randNum[I] = np.count_nonzero(randArray==I)

# sum of squares of [difference between actual and ideal] divided by ideal
SSE6 = np.sum(np.square(mod6Num-expect6)/expect6)
SSE9 = np.sum(np.square(mod9Num-expect9)/expect9)
SSErand = np.sum(np.square(randNum-expect6)/expect6)
SSE = [SSE6,SSE9,SSErand]
methodName = ['mod(N,6) method','mod(N,9) method','rand function']

# calculate confidence critical value
confLim = np.array([0.5,0.9,0.99,0.999,0.9999])
confVal = chi2.ppf(confLim,5)

# print results to screen in bar plot
n_groups = 6
fig, ax = plt.subplots()
index = np.arange(n_groups)
bar_width = 0.25
opacity = 0.5
rects1 = plt.bar(index, mod6Num, bar_width, alpha=opacity, color='b', label='mod(N,6)')
rects2 = plt.bar(index+bar_width, mod9Num, bar_width, alpha=opacity, color='g', label='mod(N,9)')
rects3 = plt.bar(index+2*bar_width, randNum, bar_width, alpha=opacity, color='r', label='rand()')
plt.xlabel('number rolled')
plt.ylabel('number of times rolled')
plt.title('Words in {}'.format(title))
plt.xticks(index+bar_width, ('1','2','3','4','5','6'))
plt.legend(loc='lower right')
plt.tight_layout()
plt.show()

# print results to screen as table
arr1 = [methodName[0]]
arr1.extend(mod6Num.tolist())
arr2 = [methodName[1]]
arr2.extend(mod9Num.tolist())
arr3 = [methodName[2]]
arr3.extend(randNum.tolist())
tableDat = [arr1,arr2,arr3]
print('{} has {:d} unique words'.format(title,len(uniq_words)))
print('')
print(tabulate(tableDat, headers = ['method',1,2,3,4,5,6]))
print('')
for I in range(len(SSE)):
    print('Normalized sum of squared error (SSE) for {} = {:5g}'.format(methodName[I],SSE[I]))
print('')

for J in range(len(confLim)):
    print('Critical value of chi-squared distribution for {:5g}% confidence level = {:5g}'.format(100*confLim[J],confVal[J]))
    for I in range(len(SSE)):
        if SSE[I]>confVal[J]:
            printstr = '{} SSE is greater than critical value, {:5g}% confidence level that numbers are not distributed randomly'
            print(printstr.format(methodName[I],100*confLim[J]))
        
