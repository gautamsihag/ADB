'''
    COMS E6111 - Advanced Databases Project 1
    Team: Abhyuday Polineni (ap3318), Surashree Kulkarni (ssk2197)
'''
import urllib
import urllib2
import base64
import sys
import re
import string
import math
import xml.etree.ElementTree as elementtree
from collections import defaultdict

###Constants ###
NUM_RESULTS = 10
DESCRIPTION = "description"
URL = 'url'
TITLE = 'title'
ID = 'id'
ALPHA = 1.0
BETA = 1.0
GAMMA = 1.0
DELIMITERS = '[\s.,=?!:@<>()\"-;\'&_\\{\\}\\|\\[\\]\\\\]+'
TRANSCRIPT_PATH = 'transcript.txt'

### Bing Namespace ###
ns = {"atom": "http://www.w3.org/2005/Atom", "d": "http://schemas.microsoft.com/ado/2007/08/dataservices"}

### Stopwords ###
stopWords = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself',
                      'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they',
                      'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those',
                      'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did',
                      'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by',
                      'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above',
                      'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then',
                      'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most',
                      'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't',
                      'can', 'will', 'just', 'don', 'should', 'now', '~', '*', '|', '+', '-', '^', '%', '/', '.', '&', '$', '@', '!',
                      ';', ':', '<', '>']

### Do a Bing search on the given query ###
def bingSearch(key, query):
    
    #Formulate Query string
    getQuery = {'Query': ('\'' + " ".join(query) + '\'')}
    bingUrl = 'https://api.datamarket.azure.com/Bing/Search/Web?' + urllib.urlencode(getQuery) + '&$top=' + str(NUM_RESULTS) + '&$format=Atom'
    print "URL: " + bingUrl
    with open(TRANSCRIPT_PATH, 'a') as f: # Print to transcript
        f.write("URL: " + bingUrl + "\n")
        
    # Set Credentials
    accountKeyEnc = base64.b64encode(key + ':' + key)
    headers = {'Authorization': 'Basic ' + accountKeyEnc}
    
    # Make Request
    req = urllib2.Request(bingUrl, headers = headers)
    response = urllib2.urlopen(req)
    
    # Get response
    rawContent = response.read()
    formattedResults = getFormattedResults(rawContent) 
    return formattedResults

### Process raw response from Bing to extract urls, titles and descriptions ###
def getFormattedResults(rawResults):
    inputFeed = elementtree.fromstring(rawResults)
    formattedResults = []
    for entry in inputFeed.findall('.//atom:entry', namespaces=ns):
        url = entry.findall('.//d:Url', namespaces=ns)[0].text
        title = entry.findall('.//d:Title', namespaces=ns)[0].text
        description = entry.findall('.//d:Description', namespaces=ns)[0].text
        formattedResults.append({'url': url, 'title': title.encode('gbk', 'replace'), 'description': description.encode('gbk', 'replace')})
    
    return formattedResults

### Print Urls, Titles, and Summary in a user friendly format ###
def printFormattedResult(result, index):
    #print result
    print "Result " + str(index) + "\n["
    print " URL: " + result['url']
    print " Title: " + result['title']
    print " Summary: " + result['description']
    print " ]\n"
    with open(TRANSCRIPT_PATH, 'a') as f: # Print to transcript
        f.write("Result " + str(index) + "\n[")
        f.write(" URL: " + result['url'] + "\n")
        f.write(" Title: " + result['title'] + "\n")
        f.write(" Summary: " + result['description'] + "\n")
        f.write(" ]\n")

### Remove the stopwords and index the documents ###
def indexDocuments(results):
    indexedDocs = []
    termFreq = dict()
    invertedDoc = dict()
    for result in results:
        indexedDoc = {}
        indexedDoc['relevant'] = result['relevant']
        indexedDoc[ID] = result[ID]
        indexedDoc['tfVector'] = {}
        wSummary = re.compile(DELIMITERS).split(result['description'])
        wTitle = re.compile(DELIMITERS).split(result['title'])
        tokens = wSummary + wTitle
        
        tokensFiltered = []
        tokenIndex = 0
        for token in tokens:
            
            if token in stopWords or len(token) <= 1:
                continue;
            token = token.lower()
            
            tokensFiltered.append(token)
            
            # Compute the Un-normalized term tfVector  for each term
            if token in indexedDoc['tfVector']:
                indexedDoc['tfVector'][token] = indexedDoc['tfVector'][token] + 1
            else:
                indexedDoc['tfVector'][token] = 1
            
            # Compute the total term frequencies of each term
            if token in termFreq:
                termFreq[token] = termFreq[token] + 1;
            else:
                termFreq[token] = 1
            
            #Compute the inverted files    
            if not invertedDoc.has_key(token):
                invertedDoc[token] = { }

            if not invertedDoc[token].has_key(result[ID]):
                invertedDoc[token][result[ID]] = { }
            
            # Calculate inverted document body
            if invertedDoc[token][result[ID]].has_key("b"):
                invertedDoc[token][result[ID]]["b"].append(tokenIndex)
            else:
                invertedDoc[token][result[ID]]["b"] = [tokenIndex]

            tokenIndex = tokenIndex + 1
                
        indexedDocs.append(indexedDoc)
    
    return indexedDocs, invertedDoc

def getTopTermsOrdered(currentTerms, weights, topX=2):
    
    i = 0
    terms = []
    augmentedTerms = []
    #Get the top 2 terms not in current query
    for term in sorted(weights, key=weights.get, reverse=True):
        terms.append(term)
        if term in currentTerms:
            continue
        augmentedTerms.append(term)
        i = i + 1
        if (i >= topX):
            break;

    #Add the remaining terms in the current query
    for term in currentTerms:
        if not term in terms:
            terms.append(term)
            
    return terms, augmentedTerms

def rocchioExpansion(prevQuery, indexedDocs, invertedDoc, numRelevant, numNonRelevant):
    queryTermWeights = {}
    for term in prevQuery:
        queryTermWeights[term] = 1.0
        
    weights = {}
    for term in invertedDoc.iterkeys():       
        weights[term] = 0.0    #initialize weight vector for each key in inverted file
    
    relevantDocsTFWeights = {}
    nonrelevantDocsTFWeights = {} 
    # Compute relevantDocsTFWeights and nonrelevantDocsTFWeights vectors
    for doc in indexedDocs:
        if doc['relevant']:
            for term in doc["tfVector"]:
                if term in relevantDocsTFWeights:
                    relevantDocsTFWeights[term] = relevantDocsTFWeights[term] + doc["tfVector"][term]
                else:
                    relevantDocsTFWeights[term] = doc["tfVector"][term]
        else:
            for term in doc["tfVector"]:
                if term in nonrelevantDocsTFWeights:
                    nonrelevantDocsTFWeights[term] = nonrelevantDocsTFWeights[term] + doc["tfVector"][term]
                else:
                    nonrelevantDocsTFWeights[term] = doc["tfVector"][term]

    # Compute Rocchio vector
    for term in invertedDoc.iterkeys():
        idf = math.log(float(len(indexedDocs)) / float(len(invertedDoc[term].keys())), NUM_RESULTS)
        
        # Terms 2 and 3 of Rocchio algorithm
        for docId in invertedDoc[term].iterkeys():
            if indexedDocs[docId]['relevant']:
                # Term 2: Relevant documents weights normalized and given BETA weight
                weights[term] = weights[term] + BETA * idf * (float(relevantDocsTFWeights[term]) / numRelevant)
            else:
                # Term 3: NonRelevant documents weights normalized and given GAMMA weight
                weights[term] = weights[term] - GAMMA * idf * (float(nonrelevantDocsTFWeights[term])/numNonRelevant)
        
        # Term 1 of Rocchio, query terms
        if term in queryTermWeights:
            queryTermWeights[term] = ALPHA * queryTermWeights[term] + weights[term]   #build new query vector of weights
        elif weights[term] > 0:
            queryTermWeights[term] = weights[term]

    return queryTermWeights

def doQueryExpansion(query, results, numRelevant, numNonRelevant):
    
    #First index the documents and calculate the inverted documents
    indexedDocs, invertedDoc = indexDocuments(results)
    
    #Apply the Rocchio Algorithm
    queryTermWeights = rocchioExpansion(query, indexedDocs, invertedDoc, numRelevant, numNonRelevant)
    
    #Get the top terms in an ordered format
    query, augmentedTerms = getTopTermsOrdered(query, queryTermWeights)
    #print query
    return query, augmentedTerms
          
def search(key, precision, query):
    
    iterationNumber = 0
    while True:
        
        print 'Parameters'
        print '%-20s= %s' % ("Client key", key)
        print '%-20s= %s' % ("Query", " ".join(query))
        print '%-20s= %s' % ("Target Precision", precision)
        with open(TRANSCRIPT_PATH, 'a') as f: # Print to transcript
            f.write("Parameters\n")
            f.write('%-20s= %s\n' % ("Client key", key))
            f.write('%-20s= %s\n' % ("Query", " ".join(query)))
            f.write('%-20s= %s\n' % ("Target Precision", precision))
            
        results = bingSearch(key, query)
        if (len(results) < NUM_RESULTS):
            print "Error: Total number of results = %d, exiting.." % len(results)
            with open(TRANSCRIPT_PATH, 'a') as f: # Print to transcript
                f.write("Error: Total number of results = %d, exiting..\n" % len(results))
            break
        print "Total number of results = %d\n" % len(results)
        with open(TRANSCRIPT_PATH, 'a') as f: # Print to transcript
            f.write("Total number of results = %d\n" % len(results))
        numItems = 0
        numRelevant = 0
        numNonRelevant = 0
        
        print "======================"
        print "Iteration: " + str(iterationNumber)
        print "Bing Search Results:"
        print "Y/y = relevant, N/n = not relevant, <any other> = quit"
        print "======================"
        with open(TRANSCRIPT_PATH, 'a') as f: # Print to transcript
            f.write("======================\n")
            f.write("Iteration: " + str(iterationNumber) + "\n")
            f.write("Bing Search Results:\n")
            f.write("Y/y = relevant, N/n = not relevant, <any other> = quit\n")
            f.write("======================\n")    
        
        # Get the relevance of the document from the user feedback
        for result in results:
            result[ID] = numItems
            numItems += 1
            printFormattedResult(result, numItems)
            relevant = raw_input("Relevant (Y/N)?")
            with open(TRANSCRIPT_PATH, 'a') as f: # Print to transcript
                f.write("Relevant (Y/N)?" + relevant + "\n")
            if relevant == 'Y' or relevant == 'y':
                result['relevant'] = True
                numRelevant += 1
            elif relevant == 'N' or relevant == 'n':
                result['relevant'] = False
                numNonRelevant += 1
            else:
                print "Invalid input, exiting...\n!"
                with open(TRANSCRIPT_PATH, 'a') as f: # Print to transcript
                    f.write("Invalid input, exiting...\n!")
                return
        print '======================'
        print 'FEEDBACK SUMMARY'
        with open(TRANSCRIPT_PATH, 'a') as f: # Print to transcript
            f.write("FEEDBACK SUMMARY\n")
        # if no relevant results exit
        if (numRelevant <= 0):
            print "Error: No relevant results from user feedback, exiting...\n"
            with open(TRANSCRIPT_PATH, 'a') as f: # Print to transcript
                f.write("Error: No relevant results from user feedback, exiting...\n")
            return
    
        print "Precision " + str(float(numRelevant)/NUM_RESULTS)
        with open(TRANSCRIPT_PATH, 'a') as f: # Print to transcript
            f.write("Precision " + str(float(numRelevant)/NUM_RESULTS) + "\n")
        # if precision of results is less than target precision do query expansion
        if float(numRelevant)/NUM_RESULTS < precision:
            print "Still below the desired precision of  " + str(precision)
            with open(TRANSCRIPT_PATH, 'a') as f: # Print to transcript
                f.write("Still below the desired precision of  " + str(precision) + "\n")
            query, augmentedTerms = doQueryExpansion(query, results, numRelevant, numNonRelevant)
            print "Augmenting by: " + str(augmentedTerms)
            with open(TRANSCRIPT_PATH, 'a') as f: # Print to transcript
                f.write("Augmenting by: " + str(augmentedTerms) + "\n")
        else:
            print "Precision reached, exiting"
            with open(TRANSCRIPT_PATH, 'a') as f: # Print to transcript
                f.write("Precision reached, exiting\n")
            return
        iterationNumber = iterationNumber + 1
        
def validatePrecision(s):
    # Validate whether the precision@10 is a float between 0 and 1
    try:
        f = float(s)
        if (0 <= f and f <= 1):
            return True
        else:
            return False
    except ValueError:
        return False
    
if __name__ == "__main__":
    # Entry point, does some initial parameter checking
    if len(sys.argv) != 4:
        print "Usage: python main.py <bingKey> <precision> <query>"
        sys.exit(1)
    bingAccountKey = sys.argv[1]
    precision = float(sys.argv[2])
    query = sys.argv[3]

    if not validatePrecision(precision):
        print "Precision must be between 0 and 1"
        sys.exit(1)
    
    ### TEST dummy command line data ###
    '''
    bingAccountKey = 'Nd1mR2D4ERA7IeNSLzw/Sr8AcBZGI40W/AlH8XyZ5Sw'
    precision = 0.9
    query = ['gates']
    '''
    queryArray = query.split();
    #Start the search and query expansion routine
    search(bingAccountKey, precision, queryArray)

