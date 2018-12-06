from bs4 import BeautifulSoup
from csv import writer
from time import sleep
import requests

url=f"http://quotes.toscrape.com/page/1/"
response=requests.get(url)
soup=BeautifulSoup(response.text,"html.parser")

index=1

# Check if next tag exists and start scraping quotes
while soup.find_all(class_="next"):
	response=requests.get(url)
	soup=BeautifulSoup(response.text,"html.parser")
	quote_data=soup.find_all(class_="quote")

	with open("data/quotes.csv","a") as file:
		csv_writer=writer(file)
		for quote in quote_data:
			text=quote.find(class_="text").get_text()
			author=quote.find(class_="author").get_text()
			csv_writer.writerow([author,text])

	print(f"page {index} scraped")		
	index+=1
	url=f"http://quotes.toscrape.com/page/{index}/"
	sleep(5)

print("Scraping complete")	