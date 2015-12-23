
class TNode:

	classification = None 
	parent = None
	left = None
	center = None
	right = None
	data = 0

	def __init__(self, data, specificity, parent, classification):
		self.left = None
		self.center = None
		self.right = None
		self.data = data
		self.parent = parent
		self.classification = classification

class TernaryTree:
	def __init__(self):
		self.root = None

	def addNode(self, data, specificity, parent, classification):
		return TNode(data, specificity, parent, classification)

	def insertLeft(self, root, data, parent, classification):
		if root == None:
			return self.addNode(data, 1, parent, classification)
		else:
			root.left = self.insertLeft(root.left, data, root, classification)
			return root

	def insertRight(self, root, data, parent, classification):
		if root == None:
			return self.addNode(data, 1, parent, classification)
		else:
			root.right = self.insertRight(root.right, data, root, classification)
			return root


	def insertCenter(self, root, data, parent, classification):
		if root == None:
			return self.addNode(data, 1, parent, classification)
		else:
			root.center = self.insertCenter(root.center, data, root, classification)
			return root


	def maxDepth(self, root):
		if root == None:
			return 0
		else:
			ldepth = self.maxDepth(root.left)
			cdepth = self.maxDepth(root.center)
			rdepth = self.maxDepth(root.right)
			return max(ldepth, rdepth, cdepth) + 1

	def size(self, root):
		if root == None:
			return 0
		else:
			return self.size(root.left) + 1 + self.size(root.center) + self.size(root.right)

	def isLeaf(self, root):
		if root.left == None and root.right == None and root.center == None:
			return True
		else:
			return False