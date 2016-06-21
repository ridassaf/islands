import sys
import random

input = open(sys.argv[1], 'r')
output = open('negatives.headers', 'w')
prev_fna = ''
for row in input:
	columns = row.strip().split('\t')
	if columns[0] != prev_fna:
		left = 0
	prev_fna = columns[0]

	accn = columns[1]
	start = int(columns[2])
	end = int(columns[3])
	
	if left > start:
		left = 0
	r = random.randint(left, start)
	r2 = random.randint(r, start)

	output.write(prev_fna + '\t' + accn + '\t' + str(r) + '\t' + str(r2) + '\n')

	left = end	 

output.close()	
input.close()
