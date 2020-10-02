from bs4 import BeautifulSoup
from random import choice, shuffle
import requests
import csv

version = "v1.0"

class VocabGame:
	GAME_MODES = {"1": "Standard"}
	GROUPING_CHOICES = {"1":"All", "2":"Nouns Only", "3":"Verbs Only", "4":"Adjectives Only"}
	USER_CHOICES_1 = {"start", "options", "update"}

	def __init__(self, mode="Standard", grouping="All"):
		self.vocab = self._get_vocabs()
		self.mode = mode
		self.grouping = grouping
		self.streak = 0

		print(f"Welcome to the SAT Vocabulary Study Tool {version} created by Howard Sun.")
		print("This program will allow you to efficiently review and learn quintessential SAT words needed for success.")
		self._menu()

	def _menu(self):
		print("Type 'start' to start the tool with current settings.")
		print("Otherwise, type 'options' if you want to change the settings.")
		choice_1 = input("Enter the your choice: ").lower()
		while choice_1 not in VocabGame.USER_CHOICES_1:
			choice_1 = input("You must enter 'start' or 'options': ")
		if choice_1 == "start":
			self._game_start()
		elif choice_1 == "options":
			self._options()
		elif choice_1 == "update":
			self._update_vocabs()
			print("Update complete!")
			self._menu()
		

	def _options(self):
		print(f"Which of the following modes would you like to start with? Currently selected: '{self.mode}'")
		print("1 - Multiple Choice (Default)")
		choice_2 = input("Enter the number corresponding the choice: ")
		if choice_2 not in VocabGame.GAME_MODES.keys():
			print(f"Sorry, '{choice_2}' is not a valid input. '{self.mode}' has been selected.")
		else:
			self.mode = VocabGame.GAME_MODES[choice_2]
			print(f"'{self.mode}'' has been selected.")
		print(f"Which of the following groupings would you like to select? Currently selected: '{self.grouping}'")
		print("1 - All (Default)")
		choice_3 = input("Enter the number corresponding the choice: ")
		if choice_3 not in VocabGame.GROUPING_CHOICES.keys():
			print(f"Sorry, '{choice_3}' is not a valid input. '{self.grouping}'' has been selected.")
		else:
			self.grouping = VocabGame.GROUPING_CHOICES[choice_3]
			print(f"'{self.grouping}' has been selected.")
		self._menu()


	def _vocab_reset(self):
		self.vocab = self._get_vocabs()

	def _game_start(self):
		if self.mode == "Standard":
			if self.grouping == "All":
				temp_list = []
				temp_request = choice(list(self.vocab.keys()))
				temp_list.append(self.vocab[temp_request][0])

				while len(temp_list) < 4:
					appending = self.vocab[choice(list(self.vocab.keys()))][0]
					if appending not in temp_list:
						temp_list.append(appending)
				shuffle(temp_list)
				choices = dict(enumerate(temp_list,1))
				
				print(f"Which of the following is the definition of {temp_request}?")
				for i, value in choices.items():
					print(f"{i} - {value}")
				response = input("Pick the number corresponding to your choice: ")
				while response not in {'1','2','3','4'}:
					response = input("You must enter a number out of the 4 corresponding options: ")
				response = int(response)

				if choices[response] == self.vocab[temp_request][0]:
					self.streak += 1
					print(f"You are correct!")
					if self.streak > 2:
						print(f"You are on a streak of {self.streak}. Amazing!")
				else:
					self.streak = 0
					print(f"Incorrect! The correction definition for {temp_request} is: {self.vocab[temp_request][0]}.")

				temp_list.clear()

				again = input("Would you like to continue? (Y/N)")
				if not again:
					again = "y"
				while again[0].lower() not in {"y","n"}:
					again = input("Would you like to continue? (Y/N)")

				if again[0].lower() == "y":
					self._game_start()
				elif again[0].lower() == "n":
					self._menu()
		else:
			pass

	def _get_vocabs(self):
		with open("vocabs.csv") as file:
			reader = csv.DictReader(file, fieldnames=["Index","Word", "Definition", "Grouping"], delimiter="|")
			return {row["Word"]:[row["Definition"],row["Grouping"],row["Index"]] for row in reader}

	def _update_vocabs(self):
		with open("vocabs.csv", "w", encoding="utf-8") as file:
			writer = csv.DictWriter(file, fieldnames=["Index","Word", "Definition", "Grouping"], delimiter="|")

			writer.writeheader()
			response = requests.get("https://satvocabulary.us/INDEX.ASP?CATEGORY=6000LIST")
			soup = BeautifulSoup(response.text, "html.parser")
			wordlist = soup.find_all("tr")

			wordlist[0].decompose()
			wordlist[1].decompose()

			for tag in wordlist:

				if not tag.contents:
					continue

				index = tag.contents[1].get_text()
				vocab =  tag.contents[3].get_text().title().strip()
				definition = tag.contents[5].get_text().title().strip()
				grouping = tag.contents[7].get_text().title()

				writer.writerow({"Index":index,"Word":vocab, "Definition":definition, "Grouping":grouping})

VocabGame()



tqwpoepqwojep