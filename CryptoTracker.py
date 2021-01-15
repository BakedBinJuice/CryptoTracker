#!/usr/bin/env python3

from bs4 import BeautifulSoup
import requests
from forex_python.converter import CurrencyRates

print("Scraping https://coinmarketcap.com/...\n")

c = CurrencyRates()
cryptos = [
"https://coinmarketcap.com/currencies/bitcoin/",
"https://coinmarketcap.com/currencies/bitcoin-cash/",
"https://coinmarketcap.com/currencies/ethereum/",
"https://coinmarketcap.com/currencies/tether/",
"https://coinmarketcap.com/currencies/litecoin/",
"https://coinmarketcap.com/currencies/polkadot-new/",
"https://coinmarketcap.com/currencies/chainlink/"
		]

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
	print(url)
	print(finalHeading + " - $" + str(finalPrice) + "\n")


