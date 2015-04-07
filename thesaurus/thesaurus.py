from pattern.web import*
import string
import random
import pickle

"""
Overall, it seems like you had some very useful insights about making runtime shorter with 
caching/memoizing, and prioritizing searches. However, though this is good on a high level,

I really suggest you work on splitting your functions a whole lot more, and thinking on making
your code readable and intuitive, not just fast.

I have some specific comments on some really repetitive chunks of code, and how you can reduce them down.
I also have some comments on the many if statements you have, and a comment on how I would personally
structure that differently.

Basically, you're on the right track with code efficiency, but get thinking on readability,
elegance, and structure! Which are just as important. 

+Functionality: 5/5
+Documentation: 4/5 (Comments aren't everything here, make the structure cleaner)
+Style: 4/5 (Split your functions more, aim for elegance and little repetition)
+CheckIn: yes
+Total: 4/5

"""

def if_x_in_y(charList, word):
	"""Take a list of characters and a word and returns true if any of the characters are in the word, false if not"""
	for char in charList:
		if char in word:
			return True
	return False

def find_synonyms(word):
	"""Takes in a word and returns a list of synonyms."""
	#is the word capitalized?
	capital = word[0].isupper()
	ending = ''

	#if the word ends with a weird symbol, take it away and save it as variable 'ending' to add back later
	if word[-1] not in set(string.ascii_letters):
		ending = word[-1]
		word = word[:-1]
		#if the second to last letter of the word is a weird symbol, take it away and save it as a variable 'ending' to add back later
		if len(word) > 1:
			if word[-2] not in set(string.ascii_letters):
				ending = word[-1]
				word = word[:-1]

	#navigate to the thesaurus page of the word and parse the html for the synonyms of the word
	
	#Oh dear. this part looks extremely grimy....check if there's any libraries that can deal with 
	# some of this for you...I used one before that "prettified" an html file
	# and only returned the text I needed, for example, and that was just one function call.
	# Anyway, at least put this in in a seperate file and function that can parse an html file,
	# and just call it here

	url = 'http://www.thesaurus.com/browse/' + word + '?s=t'
	retry = True
	while retry:
		try:
			html = URL (url).download()
			retry = False
		except:
			return [word + ending]
	html = html.split('antonyms')
	if len(html) < 3:
		return [word+ending]
	html = html[2]
	html = html.split('<span class="text">')
	html = ''.join(html)
	html = html.split('</span>')
	html = ''.join(html)
	html = html.split('\n')
	finalHtml = []
	for item in html:
		if len(item) > 0:
			if item[0] in set(string.ascii_letters):
				finalHtml.append(item)
	html = '@'.join(finalHtml)
	html = html.split('</h2>')
	if len(html) > 1:
		html = html[1]
	else:
		return [word + ending]
	html = html.split('@')

	"""
	Holy crap, OK. I do like how you tried to comment this and make it somewhat readable. 

	However, a bunch of if statements like this is not the best way to structure this. 

	My suggestion would be to actually make each filtering process it's own seperate function. 

	Then, create a list of these functions in the order
	that you want(Yup, you can do that, lists can hold funcitons).

	Finally, make another funciton "is_synonym_needed" that loops through the list, calls the funciton
	on every loop, and breaks/returns false if the function returns false. If it makes it through them all,
	it returns true.
	
	"""
	#make sure all of the synonyms are more than white space
	finalHtml = []
	for item in html:
		if len(item) > 0:
			finalHtml.append(item)

	#if </a> is at the end of a synonym, remove it
	for x in xrange(len(finalHtml)):
		if finalHtml[x][-4:] == '</a>':
			finalHtml[x] = finalHtml[x][:-4]

	#if a synonym is longer than 25 characters, remove it
	html = []
	for item in finalHtml:
		if len(item) <= 25:
			html.append(item)
		else:
			break
	finalHtml = []
	for item in html:
		if 'synonyms' not in item.lower():
			finalHtml.append(item)

	#if the synonym starts with a ' ', then remove it
	for x in xrange(len(finalHtml)):
		if finalHtml[x][0] == ' ':
			finalHtml[x] = finalHtml[x][1:]

	#if the synonym ends with a ' ', then remove it
	for x in xrange(len(finalHtml)):
		if finalHtml[x][-1] == ' ':
			finalHtml[x] = finalHtml[x][:-1]

	#if the word was capital, make the synonyms capital
	synonyms = []
	for item in finalHtml:
		thing = item.split(' ')
		if capital:
			for index, newItem in enumerate(thing):
				if index == 0:
					thing[index] = thing[index].title()
			item = ' '.join(thing)
			synonyms.append(item + ending)
		else:
			synonyms.append(item + ending)
	return 

#Oh dear. Please split your functions. These functions are way too long. Good job on commenting, but
# that isn't the only way of making code readable. Think about if there's a better way to structure
# things in the first place, as I mentioned in my comment on the if statements above.

def improve_text(text):
	"""Takes in any size text and returns the text with each word processed through a thesaurus and translated"""
	#define the list of words that should not be translated
	skippedWords = ['i', 'a', 'the', 'it', 'he', 'she', 'you', 'are', 'is', 'in', 'for']
	for x in xrange(len(skippedWords)):
		#This is a giant repetive chunk of code here. Whenever you see repetition like this,
		# a red flag should go off in your head on how you can make it just one or two lines. 
		skippedWords.append(skippedWords[x]+',')
		skippedWords.append(skippedWords[x]+':')
		skippedWords.append(skippedWords[x]+';')
		skippedWords.append(skippedWords[x]+'.')
		skippedWords.append(skippedWords[x]+'?')
		skippedWords.append(skippedWords[x]+'!')
	#take the text, and replace '\n' with a recognizable marker, '!@#', which I will later recognize as a place to put new lines
	text = text.replace('\n', ' !@# ')
	text = text.replace('  ', ' ')
	improvedText = []
	synonyms = []
	knownSynonyms = dict()
	text = text.split()
	#process the words into synonyms
	wordCount = 0
	lineCount = 0
	wordsSkippedCount = 0
	dictionaryUseCount = 0
	synonymsFoundCount = 0
	for index, word in enumerate(text):
		#if one of the words in the input is on the skippedWords list, or has '-' in it, or has a number in it, then simply put it back into the new sentence
		if word.lower() in skippedWords or '-' in word or if_x_in_y(list(string.digits), word):
			improvedText.append(word)
			wordsSkippedCount += 1
		#if one of the words is the marker '!@#', then add '\n'
		elif word == '!@#':
			improvedText.append('\n')
			lineCount += 1
		#if we have already found the synonyms list of this word before, then just reference the list of synonyms again (without accessing the internet) and randomly choose one
		elif word in knownSynonyms:
			improvedText.append(random.choice(knownSynonyms[word]))
			dictionaryUseCount += 1
		#else look up the synonyms list and randomly choose one
		else:
			synonyms = find_synonyms(word)
			improvedText.append(random.choice(synonyms))
			knownSynonyms[word] = synonyms
			synonymsFoundCount += 1
		wordCount += 1

		#Again, all these print statements are super repetitive. Consider something cleaner like:

		# fields = ['Word Count', 'Line Number', 'Words skipped', 'Dict Uses', 'Syns Found']
		# counts = [wordCount, lineCount, wordsSkippedCount, dictionaryUseCount, synonymsFoundCount]
		# for field, count in zip(fields, counts):
		# 	print field, ': ', wordCount, '\n'

		print '   Word count: ', wordCount, '\n'
		print '  Line number: ', lineCount, '\n'
		print 'Words skipped: ', wordsSkippedCount, '\n'
		print '    Dict uses: ', dictionaryUseCount, '\n'
		print '   Syns found: ', synonymsFoundCount, '\n', '\n'

	#join the synonyms together back into the text
	return ' '.join(improvedText)

#This is what is translated
file = open('thesaurus_explaination.txt','r')
input_file = file.read()
file.close()

#This is the file that the translation is saved to
f = open('coolStuff.txt', 'w')

#Execute the translation and write the new file
f.write(improve_text(input_file))