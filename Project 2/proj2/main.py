
import json
import sys
import constants
import math
import ternaryTree
import classify

def createTernaryTree():
	tTree = ternaryTree.TernaryTree()

	root = tTree.addNode(0, 1, None, "Root")

	# populate 3-way tree with categories and their subcategories
	tTree.insertLeft(root, constants.QP_ROOT['Computers'], root, 'Computers')
	tTree.insertCenter(root, constants.QP_ROOT['Sports'], root, 'Sports')
	tTree.insertRight(root, constants.QP_ROOT['Health'], root, 'Health')

	Computers = root.left
	tTree.insertLeft(Computers, constants.QP_COMPUTERS['Hardware'], Computers, 'Hardware')
	tTree.insertRight(Computers, constants.QP_COMPUTERS['Programming'], Computers, 'Programming')

	Sports = root.center
	tTree.insertLeft(Sports, constants.QP_SPORTS['Soccer'], Sports, 'Soccer')
	tTree.insertRight(Sports, constants.QP_SPORTS['Basketball'], Sports, 'Basketball')

	Health = root.right
	tTree.insertLeft(Health, constants.QP_HEALTH['Fitness'], Health, 'Fitness')
	tTree.insertRight(Health, constants.QP_HEALTH['Diseases'], Health, 'Diseases')

	return root, tTree

# key = xdx+w3OKQOk3GQY5DdI01EKAfjmU6uP1Q99yY6H+ECU
# main.py <BING_ACCOUNT_KEY> <t_es> <t_ec> <host>
if __name__ == "__main__":
	print "hello"
	arglist = sys.argv 
	if len(arglist) < 4:
		print "Usage: main.py <BING_ACCOUNT_KEY> <t_es> <t_ec> <host>"
		sys.exit(1)

	# validate arguments t_es, t_ec are in range
	if (float(arglist[2]) > 1 or float(arglist[2]) < 0):
		print "specificity invalid {}".format(arglist[2])
		sys.exit(1)

	if int(arglist[3]) < 1:
		print "coverage invalid"
		sys.exit(1)

	bing_account_key = arglist[1]
	t_es = float(arglist[2])
	t_ec = int(arglist[3])
	host = arglist[4]

	# create category tree
	# categoryTree = {'root': [constants.QP_ROOT, [constants.QP_COMPUTERS, constants.QP_HEALTH, constants.QP_SPORTS]]}
	expCoverage = {"Root": 0}
	expSpecificity = {"Root" : 1}
	sample = {}
	index = {}

	root, tTree = createTernaryTree()

	# classify database
	result = set(classify.classifyDatabase(bing_account_key, host, tTree, root, t_ec, t_es, expSpecificity, expCoverage, sample, index))

	print "*****************************************"
	print "** Done with Database Classification **"
	print ""
	print "Categories found:"
	print "	=> Root*"
	for x in result:
		print "	=> %s (%d, %f) " % (x, expCoverage[x], expSpecificity[x])

	print ""
	print "Dumping Content Summaries"

	for category in index:
		print "Dumping Summary for Category %s " % category

	# write content summaries to file
		f = open("./%s-%s.txt" % (category, host), 'w')
		for word in sorted(index[category].iterkeys()):
			f.write("%s#%d\n" % (word, len(index[category][word])))
		f.close()








