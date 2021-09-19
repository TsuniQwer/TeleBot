import requests
from bs4 import BeautifulSoup



#usd
urlUsd = 'https://www.banki.ru/products/currency/usd/'        # адрес мобильной версии
headers = {'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'}

r = requests.get(urlUsd, headers=headers)
soup = BeautifulSoup(r.content, 'html.parser')

usd = soup.find('div', class_='currency-table__large-text').text  # не span, как в десктопной



#eur
urlEur = 'https://www.banki.ru/products/currency/eur/'        # адрес мобильной версии
r = requests.get(urlEur, headers=headers)
soup = BeautifulSoup(r.content, 'html.parser')

eur = soup.find('div', class_='currency-table__large-text').text  # не span, как в десктопной


#bitcoin
urlbitcoin = 'https://coinmarketcap.com/ru/currencies/bitcoin/markets/'        # адрес мобильной версии
r = requests.get(urlbitcoin, headers=headers)
soup = BeautifulSoup(r.content, 'html.parser')

bitcoin = soup.find('div', class_='priceValue smallerPrice').text  # не span, как в десктопной

#Ethereum

urlEthereum = 'https://coinmarketcap.com/ru/currencies/ethereum/'        # адрес мобильной версии
r = requests.get(urlEthereum, headers=headers)
soup = BeautifulSoup(r.content, 'html.parser')

ethereum = soup.find('div', class_='priceValue smallerPrice').text  # не span, как в десктопной


#Cardano

urlCardano = 'https://coinmarketcap.com/ru/currencies/cardano/'        # адрес мобильной версии
r = requests.get(urlCardano, headers=headers)
soup = BeautifulSoup(r.content, 'html.parser')

cardano = soup.find('div', class_='priceValue').text  # не span, как в десктопной


#Binance Coin

urlBinanceCoin = 'https://coinmarketcap.com/ru/currencies/binance-coin/'        # адрес мобильной версии
r = requests.get(urlBinanceCoin , headers=headers)
soup = BeautifulSoup(r.content, 'html.parser')

BinanceCoin  = soup.find('div', class_='priceValue').text  # не span, как в десктопной


#Tether

urlTether= 'https://coinmarketcap.com/ru/currencies/tether/'        # адрес мобильной версии
r = requests.get(urlTether, headers=headers)
soup = BeautifulSoup(r.content, 'html.parser')

Tether  = soup.find('div', class_='priceValue').text  # не span, как в десктопной

#XRP

urlXRP= 'https://coinmarketcap.com/ru/currencies/xrp/'        # адрес мобильной версии
r = requests.get(urlXRP, headers=headers)
soup = BeautifulSoup(r.content, 'html.parser')

xrp  = soup.find('div', class_='priceValue').text  # не span, как в десктопной


#Solana

urlSolana= 'https://coinmarketcap.com/ru/currencies/solana/'        # адрес мобильной версии
r = requests.get(urlSolana, headers=headers)
soup = BeautifulSoup(r.content, 'html.parser')

Solana  = soup.find('div', class_='priceValue').text  # не span, как в десктопной


#Dogecoin

urlDogecoin = 'https://coinmarketcap.com/ru/currencies/dogecoin/'        # адрес мобильной версии
r = requests.get(urlDogecoin, headers=headers)
soup = BeautifulSoup(r.content, 'html.parser')

Dogecoin  = soup.find('div', class_='priceValue').text  # не span, как в десктопной


#Polkadot

urlPolkadot = 'https://coinmarketcap.com/ru/currencies/polkadot-new/'        # адрес мобильной версии
r = requests.get(urlPolkadot, headers=headers)
soup = BeautifulSoup(r.content, 'html.parser')

Polkadot = soup.find('div', class_='priceValue').text  # не span, как в десктопной


#USDCoin

urlUSDCoin = 'https://coinmarketcap.com/ru/currencies/usd-coin/'        # адрес мобильной версии
r = requests.get(urlUSDCoin, headers=headers)
soup = BeautifulSoup(r.content, 'html.parser')

USDCoin = soup.find('div', class_='priceValue').text  # не span, как в десктопной
#print(f'usd: {usd}, eur: {eur}')
#print(f'\n Bitcoin: {bitcoin}\n Ethereum: {ethereum}\n Cardano: {cardano}\n BinanceCoin: {BinanceCoin}\n Tether: {Tether}\n XRP: {xrp}\n Solana: {Solana}\n Dogecoin: {Dogecoin}\n Polkadot: {Polkadot}\n USDCoin: {USDCoin}')



  