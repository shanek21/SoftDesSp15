from pattern.web import *
f = Facebook(license='CAAE...S9o8bFK8ZAOTD4')
me = f.profile()
	my_friends = f.search(me[0], type=FRIENDS, count=10000)
for friend in my_friends:
    friend_news = f.search(friend.id, type=NEWS, count=10000)
    for news in friend_news:
        print news.text
        print news.author