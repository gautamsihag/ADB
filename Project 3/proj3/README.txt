Project 3- Apriori Algorithm

a. 
Surashree Kulkarni (ssk2197)
Abhyuday Poleini (ap3318)

b. 
main.py
apriori.py
INTEGRATED-DATASET.csv
example-run.txt

c. 
(a) NYC Open Data dataset used: 
https://data.cityofnewyork.us/Health/New-York-City-Leading-Causes-of-Death/jb7j-dtam

The leading causes of death by sex and ethnicity in New York City in since 2007. Fields included are:
Year, Ethnicity, Sex, Cause of Death, Count, Percent

(b) 
There was no mapping done. This entire dataset was used as is.

(c)
This dataset gives causes of death over the years 2007-2011 for different ethnicities and gender. From this, we can derive a. top reasons for death in New York b. given a cause of death, what is your ethnicity/gender? The rules formed show us that for a given community, what comprises their leading cause of death. For example, one of the rules derived were that given a death due to assault/homicide, the victim is highly likely to be a non-hispanic black male.

(d)
As mentioned before, there has been no preprocessing done, so to recreate the INTEGRATED-DATASET file, simply download it from the website in a .csv format.

d.
To run the program, type:
python main.py INTEGRATED-DATASET.csv <min_sup> <min_conf>
Note that min_sup and min_conf values lie between 0 and 1

e.
i. In main.py, INTEGRATED-DATASET.csv is preprocessed as follows:
	- Eliminate 'Year' from dataset, we are treating all transactions as during a single period
	- Eliminate 'Percent'- we were not sure how to use this attribute
	- There are some fields under 'Cause of death' which start and end with "", these were parsed separately to remove the leading and trailing ""
	- The inital count of each item in each transaction was set to the 'Count' of that transaction. Count here basically is the number of cases,
		so we can safely assume that each transaction in the database occurred x number of times, where x = 'Count'
ii. This dictionary of transaction and support is passed to apriori.py. 
iii. getL1Itemsets() prunes the dictionary of transactions that have low support.
iv. The algorithm in Section 2.1.2 is then implemented. 
v. For a given large-L[k - 1]-itemset, its candidate supersets L[k] are computed.
vi. For each transaction, suitable subsets are generated along with their support (the 'count' field in transactions)
vii. getL1Itemsets() is called again to prune low support subsets.
viii. Frequent itemsets and association rules are computed, sorted by support and confidence, and written to output.txt.	

f.
Interesting run:
python main.py INTEGRATED-DATASET.csv 0.005 0.7

This run is interesting because it gives us some good- and VERIFIABLE- facts about cause of deaths among men and women. 
For example, one of the rules derived is,
['ALZHEIMERS DISEASE'] => ['FEMALE'] (Conf: 71.6538789429%, Supp: 0.705451829097%) 

Indeed, it is true that about 2/3 of the victims of Alzheimer's are female. And even though the support for this rule is low (~0.7%), this rule has been scientifically proven. Also, the low support can be attributed to the fact that the dataset is only 5 years of data for the state of New York. If we expand to America, or the entire world, this rule will have greater support. 

Another rule derived was:
['INTENTIONAL SELF-HARM (SUICIDE)'] => ['MALE'] (Conf: 74.6739587716%, Supp: 0.744900057494%)
Again, it has been proven that the incidence of suicides is 5 times higher than that in women.

Another example in the frequent itemset list is: 
The support for [('NON-HISPANIC WHITE', 'MALIGNANT NEOPLASMS')] is greater than for [('NON-HISPANIC BLACK', 'MALIGNANT NEOPLASMS')]. This, again, is verifiable from sources on the internet, incidence of malignant tumours is higher among non-hispanic white males, followed by non-hispanic white females.

Thus, we see that the rules derived are reflective of the what medical studies have proven.

g.
Additional information:
Even though the rules obtained have high confidence but low support, the rules are all verifiable facts. More data (say for all over America, instead of NY) might have fixed the low support problem.
