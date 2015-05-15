from __future__ import division
import math
import operator
import time
import random
import copy
import csv
import statistics
from collections import Counter
import PS2Functions_Joonyong_Rhee
import PS2Classes_Joonyong_Rhee
import sys
    
def branches(data, n, s_val):
       n_attributes = train_data.n_attributes
       pos = 0
       neg = 0
       win_majority = '0'
       if n_attributes[n]:
              branch_dict = {'>': [], '<=': []}
              for row in data:
                        if row[-1]=='1':
                                pos += 1
                        if float(row[n]) > float(s_val):
                                branch_dict['>'].append(row)
                        elif float(row[n]) <= float(s_val):
                                branch_dict['<='].append(row)
       else:
              branch_dict = {}
              for row in data:
                     if row[-1]=='1':
                            pos += 1
                     if row[n] in branch_dict:
                            branch_dict[row[n]].append(row)
                     else:
                            branch_dict[row[n]] = [row]
       neg = len(data) - pos
       if pos > neg:
              win_majority = '1'
       else:
              win_majority = '0'
       out = {}
       out['split'] = s_val
       out['branches'] = branch_dict
       out['numerical'] = n_attributes[n]
       out ['win_majority'] = win_majority
       return out

def train(data, attributes, default, target, count):
       count += 1
       one = True
       temp = data[0][-1]
       for y in data:
              if y[-1] != temp:
                     one = False
       if count > 10:
              return PS2Classes_Joonyong_Rhee.Leaf(default)
       if not data:
              tree = PS2Classes_Joonyong_Rhee.Leaf(default)
       elif one:
              tree = PS2Classes_Joonyong_Rhee.Leaf(data[0][-1])
       else:
              n_attributes = train_data.n_attributes
              choice = PS2Functions_Joonyong_Rhee.classify(data, attributes, target, n_attributes)
              subset_data = branches(data, choice[0], choice[1])
              choice.append(subset_data['numerical'])
              choice.append(attributes[choice[0]])
              choice.append(subset_data['win_majority'])
              tree = PS2Classes_Joonyong_Rhee.Split(choice)
              for b_key, b_data in subset_data['branches'].items():
                  if not b_data:
                          break
                  subset_default = PS2Functions_Joonyong_Rhee.mode(b_data, -1)
                  next_split = train(b_data, attributes, subset_default, target, count)
                  tree.add_branch(b_key, next_split, b_data)
       return tree

def accuracy(data, tree):
       count = 0
       accurate = 0
       for row in data:
           count += 1
           p_val = tree.predict(row)
           if row[-1]==p_val:
              accurate += 1
       accuracy = 100 * (accurate/count)
       return accuracy

def prune(tree, nodes, data, p_accuracy, percentage):
       global n_accuracy
       percent = float(percentage)
       nodes = random.sample(nodes, int(percent*(len(nodes))))
       r_val = 50000
       while r_val > 0:
              pruning = []
              for node in nodes:
                     if isinstance(node, PS2Classes_Joonyong_Rhee.Leaf):
                            nodes.pop(nodes.index(node))
                            continue
                     else:
                            target = node.mode
                            node.toLeaf(target)
                            n_accuracy = accuracy(data, tree)
                            diff = n_accuracy - p_accuracy
                            pruning.append(diff)
                            node.toFork()
              if pruning:
                     maximum = pruning.index(max(pruning))
                     if isinstance(nodes[maximum], PS2Classes_Joonyong_Rhee.Split):
                            nodes[maximum].toLeaf(nodes[maximum].mode)
                     nodes.pop(maximum)
                     r_val = max(pruning)
                     p_accuracy = accuracy(data, tree)
              else:
                     r_val = 0
       return tree

def test(data, tree):
    with open ('fill_test_Joonyong_Rhee.csv', 'w', encoding='utf8',newline= '') as file:
        writer = csv.writer(file, delimiter = ',', quotechar = '|', quoting = csv.QUOTE_MINIMAL)
        writer.writerow(test_data.attributes)
        for row in data:
                row[-1] = tree.predict(row)
                writer.writerow(row)
        return data


def main():
       target = " winner"
       train_file = input("train path: ")
       validation_file = input("validate path: ")
       global test_file
       test_file = input("test path: ")
       global train_data
       global test_data
       train_data = PS2Classes_Joonyong_Rhee.data_table(train_file)
       validation_data = PS2Classes_Joonyong_Rhee.data_table(validation_file)
       test_data = PS2Classes_Joonyong_Rhee.data_table(test_file)

       types = input("Would you like to train? ")
       if types == 'yes':
           default = PS2Functions_Joonyong_Rhee.mode(train_data.instances, -1)
           train_tree = train(train_data.instances, train_data.attributes, default, target, 0)
           train_accuracy = accuracy(train_data.instances, train_tree)
           print ("Training Accuracy= " + str(train_accuracy) + "%")
           print ('Disjunctive Normal Form')
           disjunctive_form = train_tree.disjunctive([])
           nodes = train_tree.list_nodes([])
           print ("We have " + str(len(nodes)) + " nodes!")
       elif types == 'quit':
           sys.exit()
       else:
           main()
       types = input("Would you like to validate? ")
       if types == 'yes':
           validation_accuracy = accuracy(validation_data.instances, train_tree)
           print ("Validation Accuracy= " + str(validation_accuracy) + "%")
       else:
           main()
       types = input("Would you like to prune? ")
       if types == 'yes':
           percentage = input("What percent would you like to try (0 to 1)? ")
           print (percentage)
           percentage = float(percentage)
           prune_tree = prune(train_tree, nodes, validation_data.instances, validation_accuracy, percentage)
           print ('Disjunctive Normal Form')
           p_disjunctive_form = prune_tree.disjunctive([])
           p_nodes = prune_tree.list_nodes([])
           print ("Post-Pruning accuracy: " + str(n_accuracy))
           print ("We have " + str(len(p_nodes)) + " nodes!")
       else:
           main()
       types = input("Would you like a copy of the test data? ")
       if types == 'yes':
           testy = test(test_data.instances, prune_tree)
           sys.exit()

if __name__ == "__main__":
    main()
