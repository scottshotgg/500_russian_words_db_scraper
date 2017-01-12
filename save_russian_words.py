from lxml import html
import sqlite3
import requests


english = []
russian = []
relation = []


def getWords(pn):

	page = "http://masterrussian.com/vocabulary/common_verbs.htm"
	
	if pn > 0:
		page = "http://masterrussian.com/vocabulary/common_verbs_" + str(pn) + ".htm"

	print(page)

	totalPage = requests.get(page)
	tree = html.fromstring(totalPage.content)
	tds = tree.xpath('//td')
	tdslink = tree.xpath('//td[@class="word"]//a')

	for td in range(6, len(tds)):
		realtd = td - 7

		if(realtd % 4 == 0):
			russian.append(str(tds[td].text_content()).replace(" ", ""))
		elif(realtd % 4 == 1):
			english.append(tds[td].text_content())
		elif(realtd % 4 == 2):
			relation.append(tds[td].text_content())


getWords(0)

for p in range(2, 8):
	getWords(p)

print(len(english))
print(len(russian))
print(len(relation))


# if you want the conjugation links, use the aspectual pair translit and http://masterrussian.com/verbs/govorit_skazat.htm


db = sqlite3.connect('words.db')

c = db.cursor()
c = db.execute("create table main(id integer primary key, english text, russian text, relation text)")
c = db.commit()

for x in range(0, 499):
	c = db.execute("insert into main(english, russian, relation) values(?, ?, ?)", (english[x], russian[x], relation[x]))

c = db.commit()

# c = db.execute("select * from main where id=1")
# for row in c:
# 	print(row)
# c = db.commit()

db.close()