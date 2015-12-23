import json
import sys
import math
import csv
import apriori
import time

if __name__ == "__main__":
	start_time = time.time()
        print "hello"

        arglist = sys.argv
        if len(arglist) < 3:
                print "Usage: main.py </path/to/INTEGRATED-DATASET.csv> minimum_support minimum_confidence"
                sys.exit(1)

        # validate arguments min_supp and min_conf are between 0 and 1
        if (float(arglist[2]) > 1 or float(arglist[2]) < 0):
                print "Minimum support invalid. Must be between 0 and 1."
                sys.exit(1)

	if (float(arglist[3]) > 1 or float(arglist[3]) < 0):
                print "Minumum coverage invalid. Must be between 0 and 1."
                sys.exit(1)

	# fetch parameters
	dataset = arglist[1]
	min_sup = arglist[2]
	min_conf = arglist[3]
	transactions = []
	L1 = {}
	lineCount = 0

	try:

		# read file
		with open(dataset, 'rb') as csvfile:
			reader = csv.reader(csvfile, delimiter = ' ', quotechar = '|')
			next(reader)
			for row in reader:
				market_basket = ' '.join(row)
				itemset = market_basket.split(",")
	
				count1 = itemset[4]
				count2 = itemset[5]
	
				# remove first element of itemset ('year'=> ignore value)
				itemset.pop(0)

				# remove 'percent' and 'count' from itemset, count appended later
				itemset.pop()
				itemset.pop()

				# some preprocessing
				# there are some diseases in quotes ("") in the csv,
				# these have to be treated specially
				if itemset[2][0] == '\"':
					count = count2
					itemset[2] = itemset[2] + " " + itemset[3]
					itemset[2] = str(itemset[2][1:-1])
					itemset.pop()
				else:
					count = count1

				lineCount += int(count)
	
				# keep track of no. of cases
				itemset.append(count)

				transactions.append(itemset)
			
				# calculate support
				for item in itemset[:-1]:
					if item not in L1:
						L1[item] = int(count)
					else:
						L1[item] += int(count)


		csvfile.close()

    	except IOError:
        	print "Invalid file path. Cannot open: " + dataset

	apriori.apriori(min_sup, min_conf, L1, transactions, lineCount)	
	print("--- %s seconds ---" % (time.time() - start_time))


