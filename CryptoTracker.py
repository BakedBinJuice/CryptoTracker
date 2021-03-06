#!/usr/bin/env python3

from bs4 import BeautifulSoup
import requests
from forex_python.converter import CurrencyRates
import smtplib, ssl

c = CurrencyRates()

cryptos = [
"https://coinmarketcap.com/currencies/bitcoin/",
"https://coinmarketcap.com/currencies/bitcoin-cash/",
"https://coinmarketcap.com/currencies/ethereum/",
"https://coinmarketcap.com/currencies/tether/",
"https://coinmarketcap.com/currencies/litecoin/",
"https://coinmarketcap.com/currencies/polkadot-new/",
"https://coinmarketcap.com/currencies/chainlink/",
"https://coinmarketcap.com/currencies/neo/"
]

emails = [
]

prices = []

for url in cryptos:
	r = requests.get(url)
	soup = BeautifulSoup(r.content, 'html.parser')
	data = soup.find_all('div', {"class": "priceValue___11gHJ"})
	newData = str(data)
	dataName = soup.find_all('h1', {"class": "priceHeading___2GB9O"})
	dataHeading = str(dataName)
	checker = ''
	heading = ''
	price = ''

	for i, v in enumerate(newData):
		if v == '>':
			checker = v
		elif v == '/':
			checker = ""
			break
		elif checker == '>':
			price+=v

	checker = ''

	for i, v in enumerate(dataHeading):
		if v == '>':
			checker = v
		elif v == '/':
			checker = ""
			break
		elif checker == '>':
			heading+=v


	finalHeading = heading.replace('<', "")
	price = price.replace('<', "")
	newPrice = price.replace('$', "")
	newerPrice = newPrice.replace(',', "")
	finalPrice = newerPrice
	finalPrice = c.convert('USD', 'AUD', float(finalPrice))
	finalPrice = round(finalPrice, 2)
	fullDisplay = finalHeading + " - $" + str(finalPrice) + " (AUD)\n"
	prices.append(fullDisplay)

port = 587
password = "emailPassword"
context = ssl.create_default_context()
sender = "Sender Email"
finalDisplay = '''\
Subject: Crypto Update.

All data has been scraped from (https://coinmarketcap.com/).

'''

for price in prices:
	finalDisplay+="\n" + price

print(finalDisplay)

with smtplib.SMTP("smtp.gmail.com", port) as server:
	server.ehlo()
	server.starttls(context=context)
	server.ehlo()
	server.login(sender, password)
	for email in emails:
		server.sendmail(sender, email, finalDisplay)
		print("Successfully sent email to " + email)