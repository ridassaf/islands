import sys

def getComplement(seq):
	return seq[::-1]

def getReverse(seq):
	comp = getComplement(seq)
	comp = comp.replace('a', 'i')
	comp = comp.replace('t', 'a')
	comp = comp.replace('i', 't')
	comp = comp.replace('c', 'i')
	comp = comp.replace('g', 'c')
	comp = comp.replace('i', 'g')
	return comp

def numPalindromes(seq, j):
	num_palindromes = 0
	current_seq = ''
	for i in range(len(seq)):
		if i < j:
			current_seq += seq[i]
		else:
			comp_seq = getComplement(current_seq)
			if comp_seq == seq[i:i+j] or comp_seq == seq[i+1:i+j+1]:
				num_palindromes += 1
			current_seq = current_seq[1:] + seq[i]
	return num_palindromes

def maxPalindrome(seq):
	max_palindrome = 0
	for j in range(3, len(seq)/2):
		if numPalindromes(seq, j) > 0:
			max_palindrome = j
	return max_palindrome

def numReverseLocal(seq, j):
	num_reverse = 0
	current_seq = ''
	for i in range(len(seq)/2):
		if i < j:
			current_seq += seq[i]
		else:
			rev_seq = getReverse(current_seq)
			if rev_seq in seq[i:]:
				num_reverse += 1
				return num_reverse 
			current_seq = current_seq[1:] + seq[i]
	return num_reverse 

def maxReverseLocal(seq):
	max_reverse_local = 0
	for j in range(7, len(seq)):
		if numReverseLocal(seq, j) > 0:
			max_reverse_local = j
	return max_reverse_local

def numReverseAcross(seq, seq2, j):
	num_reverse = 0
	current_seq = ''
	for i in range(len(seq)):
		if i < j:
			current_seq += seq[i]
		else:
			rev_seq = getReverse(current_seq)
			if rev_seq in seq2:
				num_reverse += 1
				return num_reverse 
			current_seq = current_seq[1:] + seq[i]
	return num_reverse 

def maxReverseAcross(seq, seq2):
	max_reverse_across = 0
	for j in range(7, len(seq)):
		if numReverseAcross(seq, seq2,  j) > 0:
			max_reverse_across = j
	return max_reverse_across

def numDirectLocal(seq, j):
	num_direct = 0
	current_seq = ''
	for i in range(len(seq)/2):
		if i < j:
			current_seq += seq[i]
		else:
			if current_seq in seq[i:]:
				num_direct += 1
				return num_direct
			current_seq = current_seq[1:] + seq[i]
	return num_direct

def maxDirectLocal(seq):
	max_direct_local = 0
	for j in range(7, len(seq)):
		if numDirectLocal(seq, j) > 0:
			max_direct_local = j
	return max_direct_local

def numDirectAcross(seq, seq2,  j):
	num_direct = 0
	current_seq = ''
	for i in range(len(seq)):
		if i < j:
			current_seq += seq[i]
		else:
			if current_seq in seq2:
				num_direct += 1
				return num_direct
			current_seq = current_seq[1:] + seq[i]
	return num_direct

def maxDirectAcross(seq, seq2):
	max_direct_across = 0
	for j in range(7, len(seq)):
		if numDirectAcross(seq, seq2,  j) > 0:
			max_direct_across = j
	return max_direct_across

def AT(seq):
	num_a = seq.count('a')
	num_t = seq.count('t')
	a_t = (num_a + num_t)/15.0
	return a_t

def distToIntegrase(start, end, accn, file_name):
	mini = 10000000
	dist = 0
	gff = open(file_name + '.RefSeq.gff', 'r')
	for row in gff:
		col = row.strip().split('\t')
		if col[0] == accn:
			if 'integrase' in col[8] or 'recombinase' in col[8]:
				if int(col[3]) > start and int(col[3]) < end:
					dist1 = abs(start - int(col[3]))
					dist2 = abs(end - int(col[4]))
					if dist1 < dist2:
						dist = dist1
					else:
						dist = dist2
					if dist < mini:
						mini = dist
	gff.close()
	return mini

input = open(sys.argv[1], 'r')
output = open('features', 'w')
prev_fna = ''
dna_seq = {}
for row in input:
	columns = row.strip().split('\t')
	if columns[0] != prev_fna:
		fna = open(columns[0] + '.fna', 'r')
		### Read Frags and DNA seqs
		current_accn = '<'
		current_dna_seq = ''
		dna_seq = {}
		for r in fna:
			r = r.strip()
			if len(r) > 0 and r[0] == '>':
				dna_seq[current_accn] = current_dna_seq
				current_accn = r.split()[0][1:]
				current_dna_seq = ''
			else:
				current_dna_seq += r
		dna_seq[current_accn] = current_dna_seq
		### Finish reading frags and DNA Seqs ###
		fna.close()
	prev_fna = columns[0]

	accn = columns[1]
	start = int(columns[2])
	end = int(columns[3])

	start_seq = dna_seq[accn][start - 100: start + 115]
	end_seq = dna_seq[accn][end - 100: end + 115]
  
	a_t = round(AT(start_seq), 2)
	num_palindromes_L = numPalindromes(start_seq, 3)			
	num_palindromes_R = numPalindromes(end_seq, 3)

	max_palindromes_L = maxPalindrome(start_seq)
	max_palindromes_R = maxPalindrome(end_seq)

	num_direct_local_L = numDirectLocal(start_seq, 7)
	num_direct_local_R = numDirectLocal(end_seq, 7)

	num_direct_across_L = numDirectAcross(start_seq, end_seq, 7)
	num_direct_across_R = numDirectAcross(end_seq, start_seq, 7)

	num_reverse_local_L = numReverseLocal(start_seq, 7)
	num_reverse_local_R = numReverseLocal(end_seq, 7)

	num_reverse_across_L = numReverseAcross(start_seq, end_seq, 7)
	num_reverse_across_R = numReverseAcross(end_seq, start_seq, 7)

	max_direct_local_L = 0#maxDirectLocal(start_seq)
	max_direct_local_R = maxDirectLocal(end_seq)

	max_reverse_local_L = 0#maxReverseLocal(start_seq)
	max_reverse_local_R = maxReverseLocal(end_seq)

	max_direct_across_L = 0#maxDirectAcross(start_seq, end_seq)
	max_direct_across_R = maxDirectAcross(end_seq, start_seq)

	max_reverse_across_L = 0#maxReverseAcross(start_seq, end_seq)
	max_reverse_across_R = maxReverseAcross(end_seq, start_seq)

	dist_to_integrase = distToIntegrase(start, end, accn, columns[0])
	output.write(str(start) + '\t' + str(end) + '\t' + str(a_t) + '\t' + str(num_palindromes_L) + '\t' + str(num_palindromes_R) + '\t' + str(max_palindromes_L) + '\t' + str(max_palindromes_R) + '\t')
	output.write(str(num_direct_local_L) + '\t' + str(num_direct_local_R) + '\t' + str(num_direct_across_L) + '\t' + str(num_direct_across_R) + '\t')
	output.write(str(num_reverse_local_L) + '\t' + str(num_reverse_local_R) + '\t' + str(num_reverse_across_L) + '\t' + str(num_reverse_across_R) + '\t')
	output.write(str(max_direct_local_R) + '\t' + str(max_reverse_local_R) + '\t')
	output.write(str(max_direct_across_R) + '\t' + str(max_reverse_across_R) + '\t' + str(dist_to_integrase) + '\n')

output.close()	
input.close()
