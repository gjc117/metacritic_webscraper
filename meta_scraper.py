from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup

url = 'https://www.metacritic.com/browse/games/score/metascore/90day/all/filtered?sort=desc'

#Request url and close connection
req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
web_byte = urlopen(req).read()
webpage = web_byte.decode('utf-8')
urlopen(req).close()

#parse html into bs4
page_soup = soup(webpage, "html.parser")

#finc all results on page (first and last have slightly different claases. Called separately)
prod_f = page_soup.findAll("div", {"class":"product_row game first"})
prods = page_soup.findAll("div", {"class":"product_row game"})
prod_l = page_soup.findAll("div", {"class":"product_row game last"})

#Combine all three sets of results
prod_f.extend(prods)
prod_f.extend(prod_l)

#Create csv file to write to
filename = "games.csv"
f = open(filename, "w")
headers = "rank, title, score, release_date\n"
f.write(headers)

#Loop through all results. Print and write rank, title, score and release dates to csv file
for prod in prod_f:

	rank = prod.select('div')[0].get_text(strip=True)
	title = prod.select('div')[3].get_text(strip=True).replace('\n',' ')

	score = prod.select('div')[2].get_text(strip=True)

	release = prod.select('div')[5].get_text(strip=True)

	print("rank: " + rank)
	print("title: " + title)
	print("score: " + score)
	print("release: " + release +"\n\n")

	f.write(rank + "," + title + "," + score + "," + release.replace(",","|") + "\n")

f.close()