import json
import sys
import math
import operator

def apriori(min_sup, min_conf, L1, transactions, lineCount):
	# get large 1-itemsets
	L1 = getL1Itemsets(L1, min_sup, lineCount)

	# initialise L, k
	# L is a list of dictionaries with itemsets as key, and support as value
	L = []
	L.append(L1)
	k = 1

	# Section 2.1.1 Apriori algorithm
	while (len(L[k - 1]) > 0):
		# Get Ck, a list of candidate itemsets
		# This is the list of all possible superset of the seed set L[k - 1]
		Ck = aprioriGen(L[k - 1], k)

		c = {}
		for t in transactions:
			Ct = subset(Ck, t)	# get candidates contained in t

			for item in Ct:
				itemTuple = tuple(item)
				if itemTuple not in c:
					c[itemTuple] = int(t[3])
				else:
					c[itemTuple] += int(t[3])

		Lk = getL1Itemsets(c, min_sup, lineCount)
		L.append(Lk)
		k += 1

	writeFrequentItemsets(L, lineCount, min_sup)
	writeAssociationRules(L, lineCount, min_sup, min_conf)

def getL1Itemsets(L1, min_sup, lineCount):
	for key, value in L1.items():
		support = float(value) / float(lineCount)

		# eliminate itemsets with low support
		if float(support) < float(min_sup):
			del L1[key]

	return L1

def aprioriGen(Lk_1, k):
	# input is set of all large (k - 1)-itemsets
	# output is superset of all large k-itemsets

	Ck = []
	itemsets = Lk_1.keys()
	for idx, item1 in enumerate(itemsets):
		for item2 in itemsets[idx + 1:]:
			if k == 1:
				candidate = [item1] + [item2]
				Ck.append(candidate)
			else:
				temp = [i for i in item1 if i in item2]
				candidate = set(item1 + item2)								 
				if len(temp) == (k - 1) and (candidate not in Ck):
					Ck.append(candidate)

	return Ck	

def subset(Ck, t):
	# input is superset of all large k-itemsets, and a transaction t in the database
	# output is list of all lage k-itemsets that are contained in t

	Ct = []
	for itemset in Ck:
		if set(itemset) <= set(t):	# if itemset is contained in transaction t, append to Ct
			Ct.append(itemset)	

	return Ct

def writeFrequentItemsets(L, lineCount, min_sup):
	f = open('output.txt', 'w')
	finFreqList = {}
	min_sup_percent = float(min_sup) * float(100)

	for itemset in L:
		for item in itemset:
			finFreqList[item] = itemset[item]

	# sort final frequent itemlist by support
	sorted_freqList = sorted(finFreqList.items(), key = operator.itemgetter(1), reverse = True)

	f.write("==Frequent itemsets (min_sup=" + str(min_sup_percent) + "%)\n")
	for itemset in sorted_freqList:
		item = itemset[0]
		support = (float(itemset[1]) / float(lineCount)) * 100
		output = "[" + str(item) + "], " + str(support) + "%" + "\n"
		f.write(output) 

	f.write("\n")
	f.close()

def writeAssociationRules(L, lineCount, min_sup, min_conf):
	f = open('output.txt', 'a')
	finFreqList = {}
	rules = {}
	min_conf_percent = float(min_conf) * float(100)

	for itemset in L:
		for item in itemset:
			# convert all large-1 itemsets to tuples
			if not isinstance(item, tuple):
				key = (item,)
			else:
				key = item
			finFreqList[key] = itemset[item]

	for itemset in finFreqList:
		# ignore L1 itemsets
		if len(itemset) == 1:
			continue

		for element1 in itemset:
			# Rule: antecedent (if) => consequent (then)

			consequent = (element1,)
			antecedent = tuple([item for item in itemset if item not in consequent],)
			union = itemset

			if union not in finFreqList or antecedent not in finFreqList:
				continue

			sup_R = finFreqList[union] / float(lineCount)
			conf_R = float(finFreqList[union]) / float(finFreqList[antecedent])

			# rule should satisfy confidence and support constraints
			# there should be at least one antecedent & exactly one consequent in the output
			if (float(sup_R) > float(min_sup)) and (float(conf_R) > float(min_conf)):
				key = str(list(antecedent)) + " => " + str(list(consequent)) 
				value = [float(conf_R) * float(100), float(sup_R) * float(100)]
				rules[key] = value

	# sort rules by confidence
	sorted_rules = sorted(rules.items(), key=lambda i: i[1][0], reverse = True)

	f.write("==High-confidence association rules (min_conf=" + str(min_conf_percent) + "%)\n")
	for rule in sorted_rules:
		key = rule[0]
		value = rule[1]
		f.write(key + " (Conf: " + str(value[0]) + "%, Supp: " + str(value[1]) + "%)\n")

	f.close()
