from bs4 import BeautifulSoup
from random import choice
from csv import reader
from pyfiglet import print_figlet
import requests

with open("data/quotes.csv") as file:
	quotes=list(reader(file))

def play_game():
	available_guess=4
	random_quote=choice(quotes)
	author=random_quote[0]
	print(f"Here's a quote:\n{random_quote[1]}")
	hints=get_bio(format_author(author))
	msg="y"
	while available_guess>0 and msg!="n":
		user_guess=input(f"Who said this? Guesses remaining: {available_guess}.")
		if user_guess.lower()==author.lower():
			print("You guessed correctly! Congratulations!")
			msg=play_again()
		else:
			get_hint(available_guess,hints)
			available_guess-=1

	print(f"The author was {author}")
	if available_guess==0:		
		print("You lost")
	if msg!="n":	
		msg=play_again()		

def play_again():
	msg=input("Would you like to play again(y/n)?")
	if msg.lower()=='y':
		play_game()
	else:
		print("Ok! See you next time!")
		return msg

def get_hint(guess,hints):
	if guess==4:
		print(f"The author was born in {hints[2]} {hints[3]}")	
	elif guess==3:
		print(f"The author's first name starts with {hints[0]}")
	elif guess==2:
		print(f"The author's last name starts with {hints[1]}")								

def format_author(author):
	if author.count("."):
		return "-".join([item.strip() for item in author.split(".")])
	return author.replace(" ","-")	

def get_bio(author):
	url=f"http://quotes.toscrape.com/author/{author}/"
	response=requests.get(url)	
	soup=BeautifulSoup(response.text,"html.parser")
	birth_date=soup.find(class_="author-born-date").get_text()
	birth_location=soup.find(class_="author-born-location").get_text()
	return [author[0],author.split("-")[len(author.split("-"))-1][0],birth_date,birth_location]	

print_figlet("Welcome to Quote Guesser",font="standard",colors="magenta".upper())
play_game()
