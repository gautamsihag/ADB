------------------------------------------------------------------------------------
COMS E6111 Advanced Database Systems (Fall 2015) - Project 1
Columbia University
Information Retrieval based on User Relevance Feedback
------------------------------------------------------------------------------------
a) Abhyuday Polineni (ap3318), Surashree Kulkarni (ssk2197)	

b) List of files being submitted
proj1.py
transcript.txt

c) To run the program, type:

python proj1.py <bingKey> <precision> <query>	

E.g. python proj1.py Nd1mR2D4ERA7IeNSLzw/Sr8AcBZGI40W/AlH8XyZ5Sw 0.9 'gates'

d) Internal design of the project:

The program consists of the following methods:
i. bingSearch()
ii. getFormattedResults()
iii. printFormattedResults()
iv. indexDocuments()
v. getTopTermsOrdered()
vi. rocchioExpansion()
vii.doQueryExpansion()
viii. search()
ix. validatePrecision()
x. main()

Description:
i. The entry point is the main() method which takes as input the user query and the required precision. 

ii. It passes these values along with the  Bing Account key to the search() method which queries the Bing API and retrieves the top 10 results, and prints them in the manner shown in the reference implementation. It also takes user feedback for each query in the form of a Y/N, marking each document as relevant or non-relevant, and exiting on receiving any other input. If there are no relevant results or the total number of results is less than 10, the program exits; if the number of relevant documents is less than the required precision, the doQueryExpansion() method is called along with the query, and relevant and non-relevant documents as parameters.

iii. In the doQueryExpansion() method, the results are first passed to indexDocuments() which parses each result title and summary, removing any stop words or numeric characters, and calculating the individual token (word) frequencies, and returns a list of documents indexed as ‘relevant’ and ‘non-relevant’, and a term frequency vector (tfVector) assigned based on token frequency in the document result. 

iv. rocchioExpansion() is the main core of the program. This initializes a weight vector with the value 0.0 for every key in the inverted file. The program further computes a relevant TF weight vector and a non-relevant TF weight vector. Based on the Rocchio Algorithm formula: 

qm = alpha * q0 + beta * d(R) - gamma * d(NR)
Values of alpha = beta = gamma = 1.0 based on user testing to give most relevant results

we generate the modified query vector.

v. rocchioExpansion() returns a list of new query terms and their weight vector, which is then passed to getTopTermsOrdered() where the terms are sorted based on their weights. The top two terms *not already present in the query* are appended to the new query, and Bing is queried all over again. If there are terms which rank higher the previous iteration terms, these terms are put before the previous iteration query terms in the new ordering

e) Query modification method:

i. After receiving the first top 10 results, the terms from the titles and summary of the documents, stripping them of stop words and numeric characters. These tokens are then transformed into a term frequency vector, where each token receives a certain weight based on it’s overall term frequency. This can be called the new current ‘vocabulary’ for the query. 

ii. This term weight vector is then used in the Rocchio Algorithm, along with an original query vector, a relevant document vector and a non-relevant document vector. The formula for the algorithm is applied, with constants alpha, beta and gamma chosen. We also add a boost to the previous iteration query terms as this gives weight to what the user had chosen before. 

iii. From the new modified query vector, the top two terms not already present in the query are retrieved and appended to the original query. 

iv. The new query is passed to the Bing API and the process repeats till the precision of the results reaches the desired precision.

f) Bing Search Account Key: Nd1mR2D4ERA7IeNSLzw/Sr8AcBZGI40W/AlH8XyZ5Sw

g) Additional information: 

The other algorithms we looked to incorporate along with our current algorithm for query expansion were: 
i. Using a thesaurus which looked for synonyms and related term information for terms in the query, however, we found that this was not useful when only a few documents in the results were relevant, and sometimes led to ‘query drift’.
ii. Porter stemming to reduce the query terms into their smallest form. 
But they were removed from the final code when we found there was no improvement the search results.
iii. All the output commands are appended to the transcript.txt file created in the directory where the script is running

References:
i. https://www.youtube.com/watch?v=yPd3vHCG7N4
ii. Modern Information Retrieval: A Brief Overview Bulletin of the IEEE Computer Society Technical Committee on Data Engineering, Vol. 24, No. 4. (2001), pp. 35-42 by Amit Singhal
iii. Christopher D. Manning, Prabhakar Raghavan, and Hinrich Schütze. 2008. Introduction to Information Retrieval. Cambridge University Press, New York, NY, USA.
