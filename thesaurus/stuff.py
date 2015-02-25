from pattern.web import*
import string
import random

word = 'vehicle'

#is the word capitalized?
capital = word[0].isupper()
ending = ''

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
url = 'http://www.thesaurus.com/browse/' + word + '?s=t'
retry = True
while retry:
	try:
		html = URL (url).download()
		retry = False
	except:
		print [word+ending]
html = html.split('antonyms')
if len(html) < 3:
	print [word+ending]
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
	print [word + ending]
html = html.split('@')

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
print synonyms