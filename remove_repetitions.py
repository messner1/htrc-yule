
from collections import OrderedDict
import csv
from fuzzywuzzy import fuzz

from itertools import takewhile

from timeit import default_timer as timer

from yule_k import create_metadata_lookup

def load_metadata_table(metadata_table):
	with open(metadata_table, 'rb') as csvin:
		reader = csv.DictReader(csvin, delimiter=',', quotechar='"')
		return sorted([htid_object(item['htid'], float(item['K']), item['title'], item['author'], item['enumcron'], item['imprint'], item['totalpages']) for item in reader], key=lambda x: x.K)

def generate_clumps(entries, k_threshold):
	index = 0
	while index < len(entries):
		sublist = [entry for entry in takewhile(lambda x: abs(float(x.K) - float(entries[index].K)) <= k_threshold , entries[index:])]
		index += len(sublist)
		yield sublist






class htid_object():
	def __init__(self, htid, K, title, author, enumcron, imprint, totalpages):
		self.htid = htid
		self.K = K
		self.title = title
		self.author = author
		self.enumcron = ''.join(enumcron.split()).lower().strip().replace('.','')
		self.imprint = imprint
		self.totalpages = totalpages

	def _title_similarity(self, other_title):
		if self.title and other_title:
			if fuzz.token_set_ratio(self.title, other_title) > 95:
				return True
			else:
				return False
		return 'NAN'

	def _author_similarity(self, other_author):
		if self.author and other_author:
			if fuzz.token_set_ratio(self.author, other_author) > 95:
				return True
			else: 
				return False
		return 'NAN'

	def _enumcron_similarity(self, other_enumcron):
		if self.enumcron and other_enumcron:
			if self.enumcron == other_enumcron:
				return True
			else:
				return False
		return True
		
	def test_similarity(self, other):
		title_similarity = self._title_similarity(other.title)
		author_similarity = self._author_similarity(other.author)
		enumcron_similarity = self._enumcron_similarity(other.enumcron)
		if title_similarity and author_similarity and enumcron_similarity:
			return True
		elif ((title_similarity == 'NAN' and author_similarity) or (author_similarity == 'NAN' and title_similarity)) and enumcron_similarity:
			return True

		return False



def main():

	start = timer()

	count = 0

	table = load_metadata_table('metadata/fiction_metadata.csv')
	with open('results/fictiondedup.csv', 'w') as outfile:
		for grouping in generate_clumps(table, 0.7):
			while len(grouping) > 0:
				compare_element = grouping.pop(0)
				count += 1
				print count
				text_group = []
				for i in xrange(len(grouping)-1, -1, -1):
				    if compare_element.test_similarity(grouping[i]):
				    	count += 1
				    	print count
				    	text_group.append(grouping[i])
				        del grouping[i]
				if len(text_group) > 0:
					outfile.write("\'"+compare_element.htid+"\',\'"+compare_element.title+"\',\'"+compare_element.author+"\',\'"+str(compare_element.K)+"\',\'"+compare_element.imprint+"\',\'"+compare_element.enumcron+"\',\'"+str(compare_element.totalpages)+"\'\n")
					for found in text_group:
						outfile.write("\'"+found.htid+"\',\'"+found.title+"\',\'"+found.author+"\',\'"+str(found.K)+"\',\'"+found.imprint+"\',\'"+found.enumcron+"\',\'"+str(found.totalpages)+"\'\n")
					outfile.write("\n")


	end = timer()
	print end - start


if __name__ == '__main__':
	main()