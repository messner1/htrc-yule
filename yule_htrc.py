import yule_k
import os
import matplotlib.pyplot as plt
from fuzzywuzzy import fuzz
import csv
import string
import re

from collections import defaultdict


def non_fuzzy(outfile, metadata, corrections, data_path):
	with open(outfile, 'wb') as outfile:
		writer = csv.writer(outfile, delimiter=',',quotechar='\'', quoting=csv.QUOTE_MINIMAL)
		lookup = yule_k.create_metadata_lookup(metadata)
		correction_lookup = yule_k.create_correction_lookup(corrections)
		for filename in yule_k.retrieve_tsvs(data_path):
			print filename
			htid = re.sub('\.tsv', '', os.path.split(filename)[1], count=1)
			tsv_table = yule_k.read_tsv_file(filename, correction_lookup)
			k = yule_k.calculate_k([val for val in tsv_table.values()])
			writer.writerow([htid, lookup[htid]['title'],lookup[htid]['author'],lookup[htid]['date'], k])

#treat all the data as a single corpus, get yule value
def as_single_corpus(metadata, corrections, data_path):
	corpus_table = defaultdict(int)
	lookup = yule_k.create_metadata_lookup(metadata)
	correction_lookup = yule_k.create_correction_lookup(corrections)
	for filename in yule_k.retrieve_tsvs(data_path):
		print filename
		htid = re.sub('\.tsv', '', os.path.split(filename)[1], count=1)
		for item, val in yule_k.read_tsv_file(filename, correction_lookup).items():
			corpus_table[item] += val

	print yule_k.calculate_k([val for val in corpus_table.values()])

def fuzzy_restrictions(outfile, metadata, corrections, data_path, threshold=95):
	with open(outfile, 'wb') as outfile:
		writer = csv.writer(outfile, delimiter=',',quotechar='\'', quoting=csv.QUOTE_MINIMAL)
		lookup = yule_k.create_metadata_lookup(metadata)
		correction_lookup = yule_k.create_correction_lookup(corrections)

		seen_books = set()

		for filename in yule_k.retrieve_tsvs(data_path):

			htid = re.sub('\.tsv', '', os.path.split(filename)[1], count=1)
			if lookup[htid]['title'] not in seen_books:
				print filename
				fuzzy_matches = [title for title in seen_books if fuzz.token_set_ratio(title, lookup[htid]['title']) >= threshold]
				if not fuzzy_matches:
					seen_books.add(lookup[htid]['title'])
					tsv_table = yule_k.read_tsv_file(filename, correction_lookup)
					k = yule_k.calculate_k([val for val in tsv_table.values()])
					writer.writerow([htid, lookup[htid]['title'],lookup[htid]['author'],lookup[htid]['date'], k])




def main():

	as_single_corpus('metadata/poetry_metadata.csv','metadata/poetry_contextual_corrections.csv', 'data/Poetry')
	#fuzzy_restrictions('results/pruned_fiction_no_punc.csv','metadata/fiction_metadata.csv','metadata/fiction_contextual_corrections.csv', 'data/Fiction')

if __name__ == '__main__':
	main()