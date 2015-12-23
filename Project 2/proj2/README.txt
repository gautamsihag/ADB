
Project 2: Database Classification & Content Summarization

a. Surashree Kulkarni- ssk2197, Abhyuday Polineni- ap3318

b. Files: 

main.py - main method
classify.py - performs classification and summarization
constants.py - categories/sub-categories list
ternaryTree.py - data structure to hold category information

c. How to run the program:

i. Unzip ssk2197-proj2 and switch to that folder
ii. Run the following command:
python main.py  <BING_KEY> <t_es> <t_ec> <host>

where, 
<BING_KEY> = xdx+w3OKQOk3GQY5DdI01EKAfjmU6uP1Q99yY6H+ECU
<t_es> = value between 0 and 1 (specificity)
<t_ec> = integer greater than 1 (coverage)
<host> = URL (eg. diabetes.org)

d. Internal design:

i. The program takes as input the user’s BING_ACCOUNT_KEY, required specificity, required coverage and the URL of the database to classify.
ii. The program first calls createTernaryTree(); this method creates an instance of class ternaryTree consisting of a tree data structure with a parent node, and three nodes- left, right, center- as children. This instance is used to hold the categories, with “Root” as the root node, “Computers”, “Sports”, “Health” as its children and the children of these nodes are sub-categories as specified in the homework.	
iii. This category tree structure is then sent along with the input parameters to classify()
iv. The classify() method works recursively by walking down the category tree until it reaches the leaf node. 
v. The method first retrieves the left, center and right child of a node (if they exists), and continues to call probeDatabase() with data contained in each of these nodes (the categories we initialized the tree with in step ii.) 
vi. probeDatabase() is the method that actually makes the queries to BING API by calling bingSearch() method, which issues the query and returns its content to probeDatabase(). 
vii. probeDatabase() fetches the list of documents returned by Bing and iterates through each of them for processing. Binary documents that are pdfs or ppts are skipped. For the rest, the method uses “lynx —dump” to extract the text on that page. The content is then cleaned, indexed (performIndexing()) and returned.
viii. While performing v., the method also keeps a track of the number of query hits it receives and updates the count for each of the left, right and center probe values. The ‘coverage vector’ is computed, which is a dictionary of values for the number of hits for each child on the left, right and center. The coverageSum is computed by adding all these three values. The specificity dictionary is then computed for each node, which is equal to the (coverage of current node * specificity of parent node)/ coverageSum. 
ix. The method then calls itself (recursively) with the computed specificity and coverage in the previous call, appends it to the result object, and returns result. The content summaries are then dumped into a file.

e. Bing account key: xdx+w3OKQOk3GQY5DdI01EKAfjmU6uP1Q99yY6H+ECU

f. Additional information:

i) Our program also follows the following rule in the paper for better accuracy:

“As defined above, the computation of ECoverage might count documents more than once, since the same document might match multiple query probes. To address this issue, we could issue query probes in order, augmenting each query probe with the negation of all earlier query probes.”

This is performed in probeDatabase() where the query built first negates all the previous queries performed. 

ii) We decided to NOT include multiple-word entries in our content summaries.  

References:

http://www.cs.columbia.edu/~gravano/Papers/2003/tois03.pdf
http://www.cs.columbia.edu/~gravano/Papers/2008/tois08.pdf

