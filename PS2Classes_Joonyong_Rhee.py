from __future__ import division
import math
import operator
import time
import random
import copy
import csv
import statistics
from collections import Counter

class data_table:
    
    def __init__(self, file):
        self.file = file
        self.sort()
            
    def sort(self):
        with open (self.file) as data:
            i_val = csv.reader(data, delimiter=',', quotechar= '|')
            self.attributes = next(i_val)
            i = 0
            self.n_attributes = []
            self.instances = []
            avg = {}
            for name in self.attributes:
                if 'numerical' in name:
                    self.n_attributes.append(True)
                else:
                    self.n_attributes.append(False)
            for row in i_val:
                self.instances.append(row)
            if self.instances[-1] == [""]:
                del self.instances[-1]
            for instance in self.instances:
                for n in range(len(self.n_attributes)):
                    if instance[n] == '?':
                        if n in avg.keys():
                            instance[n] = float(statistics.mean(avg[n]))
                        else:
                            instance[n] = 0
                    if self.n_attributes[n]:
                        instance[n] = float(instance[n])
                        if n in avg.keys():
                            avg[n].append(instance[n])
                        else:
                            avg[n] = [instance[n]]
                            
class Node():
    
       def predict(self, data):
              if isinstance(self, Leaf):
                     return self.target
              else:
                     if self.n_data:
                            if data[self.attribute_val] <= self.s_val and '<=' in self.branches:
                                   return self.branches['<='].predict(data)
                            elif '>' in self.branches:
                                   return self.branches['>'].predict(data)
                            else:
                                   return '0'
                     else:
                            try:    
                                   out = self.branches[data[self.attribute]].predict(data)
                            except:
                                   return '0'
                            return out

       def disjunctive(self, path):
              if isinstance(self, Leaf):
                     if self.target == '1':
                            print ("(" + str(path) + ")")
                            print (self.target)
                            return path
                     else:
                            return False
              else:
                     for b_key, b_data in self.branches.items():
                            if self.n_data:
                                   clause = str(self.attribute_name) + " " + str(b_key) + " "+ str(self.s_val)
                            else: 
                                   clause = str(self.attribute_name) + " is " + str(b_key)
                            new = path + [clause]
                            b_data.disjunctive(new)
              return path

       def list_nodes(self, nodes):
              if isinstance(self, Leaf):
                     nodes.append(self)
                     return nodes
              nodes.append(self)
              for branch_label, branch in self.branches.items():
                     nodes = branch.list_nodes(nodes)
              return nodes

class Leaf(Node):
    
       def __init__(self, target_class):
              self.target = target_class

       def toFork(self):
              self.__class__ = Split
              self.target = None

class Split(Node):
    
       def __init__(self, attr_arr):
              self.attribute_val =  attr_arr[0]
              self.s_val =  attr_arr[1]
              self.n_data = attr_arr[2]
              self.attribute_name = attr_arr[3]
              self.mode = attr_arr[4]
              self.branches = {}

       def toLeaf(self, target):
              self.__class__ = Leaf
              self.target = target

       def add_branch(self, val, subtree, default):
              self.branches[val] = subtree
