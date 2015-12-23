import json
import math
import logging
import os
import re
import urllib
import urllib2
import base64
import sys
import probe

DELIMITERS = '[^A-Za-z]+'
BING_URL = 'https://api.datamarket.azure.com/Data.ashx/Bing/SearchWeb/v1/Composite?$top=10&$format=JSON&'

# issue query to Bing API and return top ten results
def bingSearch(bing_key, URL, query):

    url_query = 'Query=' + '%27site' + '%3a' + URL + '%20' + query.replace(' ', '%20') + '%27'

    accountKeyEnc = base64.b64encode(bing_key + ':' + bing_key)
    headers = {'Authorization': 'Basic ' + accountKeyEnc}
    full_query = BING_URL + url_query

    print '%-20s= %s' % ("URL", full_query)

    req = urllib2.Request(full_query, headers = headers)

    # query Bing
    try:
        response = urllib2.urlopen(req)
        content = response.read()
    except urllib2.HTTPError, error:
        content = error.read()

    # return reponse documents from Bing API.
    return content

def performIndexing(index, category, documentURL, content):
    if not category.classification in index:
        index[category.classification] = {}

    # update index to hold document url
    tokens = re.compile(DELIMITERS).split(content)
    for token in tokens:
        token = token.lower()
        if token.strip() == '':
            continue
        if token not in index[category.classification]:
            index[category.classification][token] = set([])

        index[category.classification][token].add(documentURL)

# Probe database and build a classification set based on input specificity and coverage
def classifyDatabase(bing_account_key, URL, root, parent, tc, ts, expSpecificity, expCoverage, sample, index):
    result = []
    if root.isLeaf(parent) == 1:
        return [parent.classification]

    # populate query probes for children in tree that exist
    # fetch class names
    parentClass = parent.classification

    # store number of query hits found for children
    # Query Bing for each child with query and count hits
    # Perform this recursively till we reach leaf nodes
    leftProbes = []
    lQueryHits = 0
    if parent.left is not None:
        leftProbes = parent.left.data
        lClass = parent.left.classification

    for y in range(len(leftProbes)):
        lQueryHits = lQueryHits +  probe.probeDatabase(bing_account_key, parent, URL, leftProbes, y, sample, index)

    rightProbes = []
    rQueryHits = 0
    if parent.right is not None:
        rightProbes = parent.right.data
        rClass = parent.right.classification

    for y in range(len(rightProbes)):
        rQueryHits = rQueryHits +  probe.probeDatabase(bing_account_key, parent, URL, rightProbes, y, sample, index)

    centerProbes = []
    cQueryHits = 0
    if parent.center is not None:
        centerProbes = parent.center.data
        cClass = parent.center.classification

    for y in range(len(centerProbes)):
        cQueryHits = cQueryHits + probe.probeDatabase(bing_account_key, parent, URL, centerProbes, y, sample, index)

    # compute coverage vector for each node
    if parent.left is not None:
        expCoverage[lClass] = lQueryHits
    if parent.center is not None:
        expCoverage[cClass] = cQueryHits
    if parent.right is not None:
        expCoverage[rClass] = rQueryHits

    expCoverageSum = lQueryHits + rQueryHits + cQueryHits + 1
    print "Coverage Sum: {}".format(expCoverageSum)

    if parent.left is not None:
        espec =  round(float((expCoverage[lClass] * expSpecificity[parentClass])) / expCoverageSum, 4)
        expSpecificity[lClass] = espec

    if parent.center is not None:
        espec =  round(float((expCoverage[cClass] * expSpecificity[parentClass])) / expCoverageSum, 4)
        expSpecificity[cClass] = espec

    if parent.right is not None:
        espec =  round(float((expCoverage[rClass] * expSpecificity[parentClass])) / expCoverageSum, 4)
        expSpecificity[rClass] = espec

    # recursively travel category tree and compute final result
    if parent.left is not None and expSpecificity[lClass] >= ts and expCoverage[lClass] >= tc:
        result.append(lClass)
        result = result + classifyDatabase(bing_account_key, URL, root, parent.left, tc, ts, expSpecificity, expCoverage, sample, index)

    if parent.center is not None and expSpecificity[cClass] >= ts and expCoverage[cClass] >= tc:
        result.append(cClass)
        result = result + classifyDatabase(bing_account_key, URL, root, parent.center, tc, ts, expSpecificity, expCoverage, sample, index)

    if parent.right is not None and expSpecificity[rClass] >= ts and expCoverage[rClass] >= tc:
        result.append(rClass)
        result = result + classifyDatabase(bing_account_key, URL, root, parent.right, tc, ts, expSpecificity, expCoverage, sample, index)

    if len(result) == 0:
        return [parent.classification]
    else:
        return result
