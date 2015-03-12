""" Analyzes the word frequencies in a book downloaded from
	Project Gutenberg """

import string

def get_word_list(file_name):
	""" Reads the specified project Gutenberg book.  Header comments,
		punctuation, and whitespace are stripped away.  The function
		returns a list of the words used in the book as a list.
		All words are converted to lower case.
	"""
	f = open(file_name,'r')
	lines = f.readlines()
	curr_line = 0
	while lines[curr_line].find('START OF THIS PROJECT GUTENBERG EBOOK') == -1:
	    curr_line += 1
	lines = lines[curr_line+1:]
	text = ''.join(lines)
	text = text.replace('\n', ' ')
	words = text.split()
	for x in xrange(len(words)):
		words[x] = words[x].lower()
	return words

def get_top_n_words(word_list, n):
	""" Takes a list of words as input and returns a list of the n most frequently
		occurring words ordered from most to least frequently occurring.

		word_list: a list of words (assumed to all be in lower case with no
					punctuation
		n: the number of words to return
		returns: a list of n most frequently occurring words ordered from most
				 frequently to least frequentlyoccurring
	"""

	#Create a dictionary in the format 'word':'number of times word appears'
	word_counts = dict()
	for word in word_list:
		if word not in word_counts:
			word_counts[word] = 1
		else:
			word_counts[word] += 1

	#Sort the dictionary by number of times word appears
	ordered_by_frequency = sorted(word_counts, key=word_counts.get, reverse=True)

	return ordered_by_frequency[:n]

print get_top_n_words(get_word_list('MobyDick.txt'), 100)