import sys
import math
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier
#from sklearn.neural_network import MLPClassifier
import random
import numpy as np

if len(sys.argv) < 2:
    print 'Usage: python py.py <input-file>'
    exit(0)

labels = [1] * 122 + [0] * 122
data=[[0 for j in range(22)] for i in range(244)]
input = open(sys.argv[1],'r')
count = 0
for row in input:
	columns = row.strip().split('\t')
	for j in range(2, len(columns)):
		data[count][j-2] = float(columns[j])
	count += 1
input.close()
input = open(sys.argv[2],'r')
count = 122
for row in input:
	columns = row.strip().split('\t')
	for j in range(2, len(columns)):
		data[count][j-2] = float(columns[j])
	count += 1
input.close()

input = open(sys.argv[3], 'r')
count = 0
test_data=[[0 for j in range(22)] for i in range(7969)]
for row in input:
	columns = row.strip().split('\t')
	for j in range(2, len(columns)):
		test_data[count][j-2] = float(columns[j])
	count += 1
input.close()

lines = int(sys.argv[5])
input = open(sys.argv[4], 'r')
count = 0
real_test_data=[[0 for j in range(22)] for i in range(lines)]
for row in input:
	columns = row.strip().split('\t')
	for j in range(2, len(columns)):
		real_test_data[count][j-2] = float(columns[j])
	count += 1
input.close()


output = open('predictions', 'w')

S = range(0,122)
S2 = range(0,lines)
minp = 1000
maxp = 0
average = 0
positives = {}

test_labels = [0 for i in range(7969)]
test_labels[3724] = 1
test_labels[3560] = 1
test_labels[4420] = 1

for j in range(0, 100):
#    s1 = random.sample(range(0,122), 40)
#    s2 = random.sample(range(122, 244), 40)
#    subset = s1 + s2
#    subset= random.sample(range(1139), 122)
#    subset= random.sample(range(303), 122)
    subset= random.sample(range(122), 80)
#    if 130 in subset:
#	print 'NOOOOOOO'
#    clf = svm.SVC(kernel='linear')
#    clf.fit([data[i] for i in subset] + [test_data[i] for i in subset], [labels[i] for i in subset] + [0 for i in range(40)])
    rfc = RandomForestClassifier(n_estimators=100, oob_score=True)
    rfc.fit([data[i] for i in subset] + [data[122+i] for i in subset], [labels[i] for i in subset] + [0 for i in range(80)])
#    rfc.fit([test_data[i] for i in range(7969)], [test_labels[i] for i in range(7969)])
#    mpl = MLPClassifier(algorithm='l-bfgs', alpha=1e-5, hidden_layer_sizes=(5, 2), random_state=1)
#    mpl.fit([data[i] for i in S] + [test_data[i] for i in subset], [labels[i] for i in S] + [0 for i in range(122)])
    
    remaining = set(S) - set(subset)
#    remaining = range(lines)
#    predictions = clf.predict([data[i] for i in remaining])
    predictions = rfc.predict([data[i] for i in remaining] + [data[122+i] for i in remaining])
#    predictions = rfc.predict([real_test_data[i] for i in range(lines)])
#    predictions = mpl.predict([test_data[i] for i in remaining])
#    print rfc.feature_importances_
    match = 0
    count = 0
    index = 0
    for i in remaining:
        if predictions[index] == labels[i]:
#        if predictions[index] == 1:
	    if (i+1) not in positives:
		positives[i+1] = 0
	    positives[i+1] += 1
#	    output.write(str(i+1) + '\t' + str(test_data[i]) + '\n')
            match += 1
#	if predictions[index] == 0:
#		match += 1
        count += 1
        index += 1
    for i in remaining:
        if predictions[index] == labels[122+i]:
            match += 1
        count += 1
        index += 1
    
    p = round(float(match)/count * 100,2)
    if p > maxp:
        maxp = p
    if p < minp:
        minp = p
    average += p

for i in positives:
	if positives[i] == 100:
	    output.write(str(i) + '\t' + str(real_test_data[i-1]) + '\n')
output.close()
#print positives
print count
print str(p) + '% matched'
print str(minp) + '% minimum'
print str(maxp) + '% maximum'
print str(round(average/100,2)) + '% average'

