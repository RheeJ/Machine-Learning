from __future__ import division
import math
import operator
import time
import random
import copy
import statistics
from collections import Counter

def entropy(data, attributes, target):

       dataEntropy = 0.0
       frequencies = {}
       a = attributes.index(target)
       for row in data:
              if row[a] in frequencies:
                     frequencies[row[a]] += 1 
              else:
                     frequencies[row[a]] = 1
       for freq in frequencies.values():
              dataEntropy += (-freq/len(data)) * math.log(freq/len(data), 2) 
       return dataEntropy


def gain(data, attributes, n, target, n_attributes):
    if 'numerical' in n:
        info_gain = numerical(data, attributes, n, target, n_attributes)
    else:
        info_gain = nominal(data, attributes, n, target)
    return info_gain

def numerical(data, attributes, n, target, n_attributes):
       t_entropy = entropy(data, attributes, target)
       i = attributes.index(n)
       bestcase = 0
       sort_list = sorted(data, key=operator.itemgetter(i))
       s_entropy = t_entropy
       for x in range(len(sort_list)):
               if x==0 or x == (len(sort_list)-1):
                   continue
               b_entropy = 0.0
               sets = [sort_list[0:x], sort_list[x+1:]]
               for temp in sets:
                   prob = len(temp)/len(sort_list)
                   b_entropy += prob*entropy(temp, attributes, target)
               if b_entropy < s_entropy:
                   bestcase = sort_list[x][i]
                   s_entropy = b_entropy
       return [(t_entropy - s_entropy),bestcase]

def nominal(data, attributes, n, target):
    t_entropy = entropy(data, attributes, target)
    s_entropy = 0.0
    i = attributes.index(n)
    bestcase = 0
    frequency = {}
    a = attributes.index(target)
    for row in data:
        if row[a] in frequency:
                frequency[row[a]] += 1 
        else:
                frequency[row[a]] = 1

        for val, freq in frequency.items():
                prob =  freq / sum(frequency.values())
                sets     = [entry for entry in data if entry[i] == val]
                s_entropy += prob * entropy(sets, attributes, target)
    return [(t_entropy - s_entropy),bestcase]

def classify(data, attributes, target, n_attributes):
       best = False
       bestCut = None
       maxGain = 0
       for a in attributes[:-1]:
              newGain, cut_at = gain(data, attributes, a, target, n_attributes) 
              if newGain>maxGain:
                     maxGain = newGain
                     best = attributes.index(a)
                     bestCut = cut_at
       return [best, bestCut]

def mode(data, index):  
       L = [e[index] for e in data]
       return Counter(L).most_common()[0][0]
