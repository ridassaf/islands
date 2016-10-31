import sys


if len(sys.argv) < 5:
	print 'usage: python fastSurfer.py  <frequency-threshold> <min_length> <max_length> <gap_threshold>'
	sys.exit()

threshold = float(sys.argv[1])
gap_threshold = int(sys.argv[4])
min_threshold = int(sys.argv[2])
max_threshold = int(sys.argv[3])

#Load pfam frequencies 
num_genomes_in_genus = {}
num_proteins_in_family_genus = {}
print 'Reading data...'
data = open('LocalFams_For_Rida', 'r')
for row in data:
	columns = row.strip().split('\t')
	num_genomes_in_genus[columns[1].lower()] = int(columns[2])
	if columns[1].lower() not in num_proteins_in_family_genus:
		num_proteins_in_family_genus[columns[1].lower()] = {}
	num_proteins_in_family_genus[columns[1].lower()][int(columns[0])] = int(columns[3])
data.close()
print '...done reading data'

#input = open('../allIslands.patric', 'r')
input = open('sample_genome.ids', 'r')
count = 0
done_genomes = []
SEs = {} 
islands = open('fast.islands', 'w')
for row in input:
	count += 1
	columns = row.strip().split('\t')
	genome = columns[0]
	
	prev_accn = ''
	first_accn = 1
	condition = 0
	potential_length = 0
	island = 0
	if genome not in done_genomes:
		done_genomes.append(genome)
		output = open('mnPotential-' + genome, 'w')
#		patric = open('../../data/Reference Genomes/PATRIC-cds-tab/' + genome + '.PATRIC.cds.tab', 'r')
##		patric = open('../../data/Manually_Verified/Genomes/' + genome + '.PATRIC.cds.tab', 'r')
		patric = open(genome + '.PATRIC.cds.tab', 'r')
		l = 0
		first = 1
		num_between = 0
		for line in patric:
			if l > 0:
				p_columns = line.strip().split('\t')
				p_genus = p_columns[1].split(' ')[0].lower()
				p_accn = p_columns[2]
				p_start = int(p_columns[9])
				p_end = int(p_columns[10])
				if any('integrase' in x for x in p_columns) or any('recombinase' in y for y in p_columns) or any('phage' in z for z in p_columns):
					island = 1
				if len(p_columns) > 16 and 'PLF' in p_columns[16]:
					p_pfam = p_columns[16]
					p_pfam_number = int(p_pfam.split('_')[2])

					num_genomes = num_genomes_in_genus[p_genus]
					if p_pfam_number in num_proteins_in_family_genus[p_genus]:
						num_proteins = num_proteins_in_family_genus[p_genus][p_pfam_number]
					else:
						num_proteins = 0
					protein_genome_ratio = abs(1.0 - round(float(num_proteins)/num_genomes, 2))
#					protein_genome_ratio = round(float(num_proteins)/num_genomes, 2)

					if first_accn == 1:
						prev_accn = p_accn
						first_accn = 0
					if condition == 0:
						potential_start = p_start
						condition = 1
					if p_accn == prev_accn:
						potential_end = p_end
						potential_length += 1
					else:
						if potential_length >= min_threshold and potential_length <= max_threshold and island == 1:
							#output potential island
							islands.write(genome + '\t' + prev_accn + '\t' + str(potential_start) + '\t' + str(potential_end) + '\n')
						
						prev_accn = p_accn
						potential_length = 0
						condition = 0
						island = 0

					if protein_genome_ratio >= threshold:
						if first == 0 and num_between != 0:
							output.write(str(num_between) + '\n')
						output.write(genome + '\t' + p_accn + '\t' + str(p_start) + '\t' + str(p_end) + '\t' + str(protein_genome_ratio) + '\n')
						
						num_between = 0
						first = 0
					else:
						num_between += 1
								
						if num_between > gap_threshold:
							potential_length -= num_between 
							if potential_length >= min_threshold and potential_length <= max_threshold and island == 1:
								#output potential island
								potential_end = SEs[l - num_between ][1]
								potential_start = SEs[l - (num_between + potential_length -1)][0]
								islands.write(genome + '\t' + p_accn + '\t' + str(potential_start) + '\t' + str(potential_end) + '\n')

							island = 0
							potential_length = 0

				SEs[l] = (p_start,p_end)

			l += 1
		patric.close()
		output.close()
		if potential_length >= min_threshold and potential_length <= max_threshold and island == 1:
			#output potential island
			islands.write(genome + '\t' + p_accn + '\t' + str(potential_start) + '\t' + str(potential_end) + '\n')
input.close()
islands.close()
