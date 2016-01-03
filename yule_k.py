import csv
import os
import glob
from collections import defaultdict

def read_results(filename):
	with open(filename,'rb') as csvin:
		reader = csv.reader(csvin, delimiter=',', quotechar='\'')
		for line in reader:
			yield line

def retrieve_tsvs(datadir):
	for root, directories, _ in os.walk(datadir):
		for directory in sorted(directories):
			for filepath in glob.glob(os.path.join(root,directory)+'/*.tsv'):
				yield filepath

def create_metadata_lookup(metadata_table):
	with open(metadata_table, 'rb') as csvin:
		reader = csv.DictReader(csvin, delimiter=',', quotechar='"')
		return {entry['htid']:entry for entry in reader}

def create_correction_lookup(correction_table):
	correction_lookup = defaultdict(dict)
	with open(correction_table, 'rb') as csvin:
		reader = csv.DictReader(csvin, delimiter=',', quotechar='"')
		for entry in reader:
			correction_lookup[entry['htid']][entry['word']] = int(entry['correction'])

	return correction_lookup


def open_summary_file(summary_file, remove_punc = True):
	summary_table = defaultdict(dict)
	with open(summary_file, 'rb') as csvin:
		reader = csv.DictReader(csvin, delimiter=',', quotechar='"')
		for line in reader:
			if not line['word'].startswith('#'): #remove the special summary tokens
				if remove_punc and filter(lambda x: x.isalnum(), line['word']): 
					summary_table[line['year']][filter(lambda x: x.isalnum, line['word'])] = int(line['termfreq'])
				else:
					print line['word']

	return summary_table

def read_tsv_file(tsv_file, correction_lookup, remove_punc=True):
	tsv_table = defaultdict(int)					
	with open(tsv_file, 'r') as texttsvin:
		htid = os.path.split(tsv_file)[1].rstrip('.tsv')
		for line in texttsvin.readlines():
			raw = line.split('\t')
			if remove_punc:
				if len(raw) >= 2 and filter(lambda x: x.isalnum(), raw[0]):
					tsv_table[filter(lambda x: x.isalnum(), raw[0])] += (int(raw[1]) if raw[0] not in correction_lookup[htid].keys() else int(raw[1])+correction_lookup[htid][raw[0]])
			else:
				if len(raw) >= 2:
					tsv_table[raw[0]] += (int(raw[1]) if raw[0] not in correction_lookup[htid].keys() else int(raw[1])+correction_lookup[htid][raw[0]]) 
		
		return  tsv_table

#Credit to magnus Nissel: https://gist.github.com/magnusnissel/d9521cb78b9ae0b2c7d6
def calculate_k(input_words):
	n = float(sum(input_words))
	n2 = sum([num ** 2 for num in input_words])
	try:
		k = 10000 * ((n2-n)/(n**2))
		return k
	except:
		return 0

def yule_k_orig(input_words):
	n = float(sum(input_words))
	mmax = max(input_words)
	right = 0
	for num in range(1,mmax+1):
		right+=input_words.count(num)*(num/n)**2
	k = 10000*((-1/n)+right)
	return k
	
