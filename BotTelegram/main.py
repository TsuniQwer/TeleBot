from telebot import types
import telebot
import config
import random
import pyowm


import schedule
from threading import Thread
from time import sleep

import requests
from bs4 import BeautifulSoup

from datetime import datetime  # date
import bus
import timetable


# -------------------------------------------------------------

owm = pyowm.OWM("f71c23329ecc0fff8824830092b7b9a8")

current_datetime = datetime.now()

bot = telebot.TeleBot(config.API_KEY)

sity = ["Пушкино", "Москва", "Казань", "Сочи","Нижний Новгород","Калининград","Калининград",
        "Ярославль", "Екатеринбург", "Анапа", "Владимир", "Тула", "Краснодар", "Воронеж",
        "Суздаль", "Новосибирск", "Кострома","Самара","Волгоград","Геленджик","Тверь","Саратов",
        "Красноярск", "Великий Новгород", "Псков", "Выборг", "Переславль-Залесский", "Рязань",
        "Коломна","Сергиев Посад", "Уфа", "Кисловодск", "Ростов-На-Дону", "Смоленск", "Челябинск",
        "Пятигорск", "Иваново","Калуга", "Пермь", "Тюмень", "Омск", "Йошкар-Ола", "Новороссийск",
        "Владивосток", "Углич", "Петрозаводск", "Вологда", "Муром", "Астрахань", "Ростов Великий",
        "Плёс", "Плес", "Звенигород", "Чебоксары", "Ивантеевка", "Клязьма", "Тарасовка", "Черкизово",
        "Заветы Ильича", "Королёв", "Мытищи", "Щёлково", "Фрязино","USA", "Хатанга", "Тура",
        "Иркутск", "Норильск", "Крым"]


# ----------------------------------------------------------------


commands = "/ras - посмотреть расписание;\n/usd, /eur  - курс доллара и евро\n/cripta - криптовалюта мониторинг \n/weather - посмотреть погоду;\n/bus - расписание автобусов 509, 29;\n/roll - случайное число от 1 до 100; \n /flip, /coin - кинуть монетку"


@bot.message_handler(commands=['start'])
def welcome(message):
    sti = open('img/sticker.webp', 'rb')
    bot.send_sticker(message.chat.id, sti)

    # main buttons
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("🎲 Расписание")
    item2 = types.KeyboardButton("🌤 Погода")
    item3 = types.KeyboardButton("📉 Валюта/крипта")
    item4 = types.KeyboardButton("📃 Все команды")

    markup.add(item1, item2, item3, item4)  # put items

    bot.send_message(message.chat.id, "Добро пожаловать, {0.first_name}!\nЯ - <b>{1.first_name}</b>, бот созданным Тсуни Квером. (Все команды - '/help', перезапустить бота - '/start')\n\n👨🏻‍💻Создатель @tsuniqwer".format(message.from_user, bot.get_me()),
                     parse_mode='html', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def lalala(message):
    if message.chat.type == 'private':
            
        for i in sity:
            if message.text == i:
                sity2 = i
                mgr = owm.weather_manager()
                observation = mgr.weather_at_place(sity2)
                w = observation.weather

                # Temperature
                MidleTemperature = w.temperature('celsius')['temp']

                wind = w.wind()['speed']
                clouds = w.clouds
                status = w.detailed_status

                bot.send_message(message.chat.id,sity2 +":")
                bot.send_message(message.chat.id, "🌤Температура: " + str(MidleTemperature) + "°," + " \n💨Ветер: " + str(wind) + "м/c, \n🌫 Облачность: " + str(clouds) + "%")

                if status == 'light rain':
                    bot.send_message(
                        message.chat.id, "Сейчас идет маленький дождь 🌧")
                elif status == 'rain':
                    bot.send_message(message.chat.id, "Сейчас идет дождь 🌧")
                elif status == 'overcast clouds':
                    bot.send_message(message.chat.id, "Пасмурно 🌧")
                elif status == 'moderate rain':
                    bot.send_message(message.chat.id, "Умеренный дождь 🌧")
                return
               

        # РАСПИСАНИЕ
        if message.text == '🎲 Расписание':
            #monthUser = current_datetime.strftime("%A")
            #bot.send_message(message.chat.id,monthUser)
            urlDay = 'https://www.google.com/search?q=day+of+week+today&oq=day+of+week+today&aqs=chrome..69i57j0i22i30l9.699j0j7&sourceid=chrome&ie=UTF-8'       
            headers = {'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'}

            r = requests.get(urlDay, headers=headers)
            soup = BeautifulSoup(r.content, 'html.parser')

            dayNow = soup.find('div', class_='vk_bk dDoNo FzvWSb XcVN5d').text


            if str(dayNow) == "понедельник":
                dayOfweek = "Monday"
            elif str(dayNow) == "вторник":
                dayOfweek = "Tuesday"
            elif str(dayNow) == "среда":
                dayOfweek = "Wednesday"
            elif str(dayNow) == "четверг":
                dayOfweek = "Thursday"
            elif str(dayNow) == "пятница":
                dayOfweek = "Friday"
            elif str(dayNow) == "суббота":
             dayOfweek = "Saturday"
            elif str(dayNow) == "воскресенье":
                dayOfweek = "Sunday"
            bot.send_message(message.chat.id,dayOfweek)
            bot.send_message(message.chat.id, "Расписание на сегодня: \n(/ras - полное расписание.)")
            for day in timetable.all:

                if dayOfweek== "Monday":
                    bot.send_photo(message.chat.id, timetable.Monday) #понедельник
                    break
                elif dayOfweek == "Tuesday":
                    bot.send_photo(message.chat.id, timetable.Tuesday) #вторник
                    break
                elif dayOfweek == "Wednesday":
                    bot.send_photo(message.chat.id, timetable.Wednesday) #среда
                    break
                elif dayOfweek== "Thursday":
                    bot.send_photo(message.chat.id, timetable.Thursday) #четверг
                    break
                elif dayOfweek == "Friday":
                    bot.send_message(message.chat.id, "Cегодня пар нет! 🥳")
                    bot.send_photo(message.chat.id, timetable.Friday) #пятница
                    break
                elif dayOfweek == "Saturday":
                    bot.send_photo(message.chat.id, timetable.Saturday) #суббота
                    break
                elif dayOfweek == "Sunday":
                    bot.send_message(message.chat.id, "Cегодня пар нет! 🥳")
                    bot.send_photo(message.chat.id, timetable.Sunday) #воскресенье
                    break
                
        elif message.text == 'Расписание':
            ph1 = open('img/photo1.jpg', 'rb')
            bot.send_photo(message.chat.id, ph1)
        elif message.text == 'расписание':
            ph1 = open('img/photo1.jpg', 'rb')
            bot.send_photo(message.chat.id, ph1)
        elif message.text == '/ras':
            ph1 = open('img/photo1.jpg', 'rb')
            bot.send_photo(message.chat.id, ph1)

        elif message.text == 'Привет':
            sti = open('img/sticker2.webp', 'rb')
            bot.send_sticker(message.chat.id, sti)
            bot.send_message(message.chat.id, "Я тебя не помню. Напиши /help.")

        elif message.text == 'привет':
            sti = open('img/sticker2.webp', 'rb')
            bot.send_sticker(message.chat.id, sti)
            bot.send_message(message.chat.id, "Я тебя не помню. Напиши /help.")

        # -------------------------------------------------------------------------------------------------------
        # BUS
        elif message.text == "/bus":
            urlTime = 'https://tochnoe-moskovskoe-vremya.ru/'       
            headers = {'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'}

            r = requests.get(urlTime, headers=headers)
            soup = BeautifulSoup(r.content, 'html.parser')

            hour = soup.find('div', class_='dclock').text 

            hourNow = int(hour[:3])
    
            bot.send_message(message.chat.id, "🚌 Автобусы в шарагу: ")
            for i in bus.busOutPushkino:
                if i == hourNow:
                    bot.send_message(message.chat.id, bus.busOutPushkino[i])
                else:
                    continue

            bot.send_message(message.chat.id, "🚌 Автобусы домой: ")
            for i in bus.busInPushkino:
                if i == hourNow:
                    bot.send_message(message.chat.id, bus.busInPushkino[i])
                else:
                    continue

        # ВАЛЮТА

        elif message.text == '/usd':
            urlUsd = 'https://www.banki.ru/products/currency/usd/'       
            headers = {
                'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'}

            r = requests.get(urlUsd, headers=headers)
            soup = BeautifulSoup(r.content, 'html.parser')

            usd = soup.find('div', class_='currency-table__large-text').text

            # eur
            urlEur = 'https://www.banki.ru/products/currency/eur/'       
            r = requests.get(urlEur, headers=headers)
            soup = BeautifulSoup(r.content, 'html.parser')

            eur = soup.find('div', class_='currency-table__large-text').text

            gif1 = open('gif/gif4.mp4', 'rb')
            bot.send_video(message.chat.id, gif1, None)
            bot.send_message(message.chat.id, "usd: " +
                             str(usd) + "\t eur: " + str(eur))
        elif message.text == '/eur':
            urlUsd = 'https://www.banki.ru/products/currency/usd/'       
            headers = {
                'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'}

            r = requests.get(urlUsd, headers=headers)
            soup = BeautifulSoup(r.content, 'html.parser')

            usd = soup.find('div', class_='currency-table__large-text').text

            # eur
            urlEur = 'https://www.banki.ru/products/currency/eur/'       
            r = requests.get(urlEur, headers=headers)
            soup = BeautifulSoup(r.content, 'html.parser')

            eur = soup.find('div', class_='currency-table__large-text').text
            gif1 = open('gif/gif4.mp4', 'rb')
            bot.send_video(message.chat.id, gif1, None)
            bot.send_message(message.chat.id, "usd: " +
                             str(usd) + "\t eur: " + str(eur))

        elif message.text == '/cripta':
            urlUsd = 'https://www.banki.ru/products/currency/usd/'       
            headers = {
                'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'}
            # bitcoin
            urlbitcoin = 'https://coinmarketcap.com/ru/currencies/bitcoin/markets/'
            r = requests.get(urlbitcoin, headers=headers)
            soup = BeautifulSoup(r.content, 'html.parser')

            bitcoin = soup.find('div', class_='priceValue smallerPrice').text

            # Ethereum

            urlEthereum = 'https://coinmarketcap.com/ru/currencies/ethereum/'
            r = requests.get(urlEthereum, headers=headers)
            soup = BeautifulSoup(r.content, 'html.parser')

            ethereum = soup.find('div', class_='priceValue smallerPrice').text

            # Cardano

            urlCardano = 'https://coinmarketcap.com/ru/currencies/cardano/'
            r = requests.get(urlCardano, headers=headers)
            soup = BeautifulSoup(r.content, 'html.parser')

            cardano = soup.find('div', class_='priceValue').text

            # Binance Coin

            urlBinanceCoin = 'https://coinmarketcap.com/ru/currencies/binance-coin/'
            r = requests.get(urlBinanceCoin, headers=headers)
            soup = BeautifulSoup(r.content, 'html.parser')

            BinanceCoin = soup.find('div', class_='priceValue').text

            # Tether

            urlTether = 'https://coinmarketcap.com/ru/currencies/tether/'
            r = requests.get(urlTether, headers=headers)
            soup = BeautifulSoup(r.content, 'html.parser')

            Tether = soup.find('div', class_='priceValue').text

            # XRP

            urlXRP = 'https://coinmarketcap.com/ru/currencies/xrp/'
            r = requests.get(urlXRP, headers=headers)
            soup = BeautifulSoup(r.content, 'html.parser')

            xrp = soup.find('div', class_='priceValue').text

            # Solana

            urlSolana = 'https://coinmarketcap.com/ru/currencies/solana/'
            r = requests.get(urlSolana, headers=headers)
            soup = BeautifulSoup(r.content, 'html.parser')

            Solana = soup.find('div', class_='priceValue').text

            # Dogecoin

            urlDogecoin = 'https://coinmarketcap.com/ru/currencies/dogecoin/'
            r = requests.get(urlDogecoin, headers=headers)
            soup = BeautifulSoup(r.content, 'html.parser')

            Dogecoin = soup.find('div', class_='priceValue').text

            # Polkadot

            urlPolkadot = 'https://coinmarketcap.com/ru/currencies/polkadot-new/'
            r = requests.get(urlPolkadot, headers=headers)
            soup = BeautifulSoup(r.content, 'html.parser')

            Polkadot = soup.find('div', class_='priceValue').text

            # USDCoin

            urlUSDCoin = 'https://coinmarketcap.com/ru/currencies/usd-coin/'
            r = requests.get(urlUSDCoin, headers=headers)
            soup = BeautifulSoup(r.content, 'html.parser')

            USDCoin = soup.find('div', class_='priceValue').text

            gif1 = open('gif/gif3.mp4', 'rb')
            bot.send_video(message.chat.id, gif1, None)
            bot.send_message(message.chat.id, "Bitcoin: " + str(bitcoin) + "\nEthereum: " + str(ethereum) + "\nCardano: " + str(cardano) + "\nBinanceCoin: " + str(BinanceCoin) +
                             "\nTether: " + str(Tether) + "\nXRP: " + str(xrp) + "\nSolana: " + str(Solana) + "\nDogecoin: " + str(Dogecoin) + "\nPolkadot: " + str(Polkadot) + "\nUSDCoin: " + str(USDCoin))

        # Валюта/крипта кнопка:

        elif message.text == '📉 Валюта/крипта':
            urlUsd = 'https://www.banki.ru/products/currency/usd/'       
            headers = {
                'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'}

            r = requests.get(urlUsd, headers=headers)
            soup = BeautifulSoup(r.content, 'html.parser')

            usd = soup.find('div', class_='currency-table__large-text').text

            # eur
            urlEur = 'https://www.banki.ru/products/currency/eur/'       
            r = requests.get(urlEur, headers=headers)
            soup = BeautifulSoup(r.content, 'html.parser')

            eur = soup.find('div', class_='currency-table__large-text').text

            # bitcoin
            urlbitcoin = 'https://coinmarketcap.com/ru/currencies/bitcoin/markets/'
            r = requests.get(urlbitcoin, headers=headers)
            soup = BeautifulSoup(r.content, 'html.parser')

            bitcoin = soup.find('div', class_='priceValue smallerPrice').text

            # Ethereum

            urlEthereum = 'https://coinmarketcap.com/ru/currencies/ethereum/'
            r = requests.get(urlEthereum, headers=headers)
            soup = BeautifulSoup(r.content, 'html.parser')

            ethereum = soup.find('div', class_='priceValue smallerPrice').text

            # Cardano

            urlCardano = 'https://coinmarketcap.com/ru/currencies/cardano/'
            r = requests.get(urlCardano, headers=headers)
            soup = BeautifulSoup(r.content, 'html.parser')

            cardano = soup.find('div', class_='priceValue').text

            # Binance Coin

            urlBinanceCoin = 'https://coinmarketcap.com/ru/currencies/binance-coin/'
            r = requests.get(urlBinanceCoin, headers=headers)
            soup = BeautifulSoup(r.content, 'html.parser')

            BinanceCoin = soup.find('div', class_='priceValue').text

            # Tether

            urlTether = 'https://coinmarketcap.com/ru/currencies/tether/'
            r = requests.get(urlTether, headers=headers)
            soup = BeautifulSoup(r.content, 'html.parser')

            Tether = soup.find('div', class_='priceValue').text

            # XRP

            urlXRP = 'https://coinmarketcap.com/ru/currencies/xrp/'
            r = requests.get(urlXRP, headers=headers)
            soup = BeautifulSoup(r.content, 'html.parser')

            xrp = soup.find('div', class_='priceValue').text

            # Solana

            urlSolana = 'https://coinmarketcap.com/ru/currencies/solana/'
            r = requests.get(urlSolana, headers=headers)
            soup = BeautifulSoup(r.content, 'html.parser')

            Solana = soup.find('div', class_='priceValue').text

            # Dogecoin
            urlDogecoin = 'https://coinmarketcap.com/ru/currencies/dogecoin/'
            r = requests.get(urlDogecoin, headers=headers)
            soup = BeautifulSoup(r.content, 'html.parser')

            Dogecoin = soup.find('div', class_='priceValue').text

            # Polkadot

            urlPolkadot = 'https://coinmarketcap.com/ru/currencies/polkadot-new/'
            r = requests.get(urlPolkadot, headers=headers)
            soup = BeautifulSoup(r.content, 'html.parser')

            Polkadot = soup.find('div', class_='priceValue').text

            # USDCoin

            urlUSDCoin = 'https://coinmarketcap.com/ru/currencies/usd-coin/'
            r = requests.get(urlUSDCoin, headers=headers)
            soup = BeautifulSoup(r.content, 'html.parser')

            USDCoin = soup.find('div', class_='priceValue').text

            # -------------------------------------------------------------------------------------------------------

            bot.send_message(message.chat.id, "usd: " +
                             str(usd) + "\t eur: " + str(eur))
            bot.send_message(message.chat.id, "Bitcoin: " + str(bitcoin) + "\nEthereum: " + str(ethereum) + "\nCardano: " + str(cardano) + "\nBinanceCoin: " + str(BinanceCoin) +
                             "\nTether: " + str(Tether) + "\nXRP: " + str(xrp) + "\nSolana: " + str(Solana) + "\nDogecoin: " + str(Dogecoin) + "\nPolkadot: " + str(Polkadot) + "\nUSDCoin: " + str(USDCoin))

        # /HELP
        elif message.text == '📃 Все команды':
            bot.send_message(message.chat.id, commands)
        elif message.text == '/help':
            bot.send_message(message.chat.id, commands)

        # РОЛЛ
        elif message.text == '/roll':
            gif2 = open('gif/gif2.mp4', 'rb')
            bot.send_video(message.chat.id, gif2, None)
            sleep(1)
            bot.send_message(message.chat.id, str(random.randint(0, 100)))

        # ФЛИП
        elif message.text == '/coin':

            gif1 = open('gif/gif.mp4', 'rb')
            bot.send_video(message.chat.id, gif1, None)
            flip = str(random.randint(0, 1))
            sleep(1)
            if flip == "1":
                bot.send_message(message.chat.id, "Орел 🪙")
                gif1.close()
            else:
                bot.send_message(message.chat.id, "Решка 🪙")
                gif1.close()

        elif message.text == '/flip':
            gif1 = open('gif/gif.mp4', 'rb')
            bot.send_video(message.chat.id, gif1, None)
            flip = str(random.randint(0, 1))
            sleep(1)
            if flip == "1":
                bot.send_message(message.chat.id, "Орел 🪙")
                gif1.close()
            else:
                bot.send_message(message.chat.id, "Решка 🪙")
                gif1.close()

        # ПОГОДА
        elif message.text == '🌤 Погода':

            markup = types.InlineKeyboardMarkup(row_width=3)
            item1 = types.InlineKeyboardButton(
                "Москва🌈", callback_data='moscow')
            item2 = types.InlineKeyboardButton(
                "Пушкино🗽", callback_data='pushkino')
            item3 = types.InlineKeyboardButton(
                "Другой город📡", callback_data='other')
            item4 = types.InlineKeyboardButton(
                "Уведомление🔔", callback_data='notification')
            ph2 = open('img/photo2.jpg', 'rb')
            bot.send_photo(message.chat.id, ph2)

            markup.add(item1, item2, item3, item4)

            bot.send_message(message.chat.id, 'Какой город?',
                             reply_markup=markup)

        elif message.text == '/weather':
            markup = types.InlineKeyboardMarkup(row_width=3)
            item1 = types.InlineKeyboardButton(
                "Москва🌈", callback_data='moscow')
            item2 = types.InlineKeyboardButton(
                "Пушкино🗽", callback_data='pushkino')
            item3 = types.InlineKeyboardButton(
                "Другой город📡", callback_data='other')
            item4 = types.InlineKeyboardButton(
                "Уведомление🔔", callback_data='notification')
            ph2 = open('img/photo2.jpg', 'rb')
            bot.send_photo(message.chat.id, ph2)

            markup.add(item1, item2, item3, item4)

            bot.send_message(message.chat.id, 'Какой город?',reply_markup=markup)
     

        else:
            bot.send_message(message.chat.id, 'Я не знаю что ответить 😢')
            sti = open('img/sticker4.webp', 'rb')
            bot.send_sticker(message.chat.id, sti)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):

    try:
        if call.message:
            if call.data == 'moscow':
                sity = "Москва"
                mgr = owm.weather_manager()
                observation = mgr.weather_at_place(sity)
                w = observation.weather

                # Temperature
                MidleTemperature = w.temperature('celsius')['temp']

                wind = w.wind()['speed']
                rain = w.rain
                clouds = w.clouds
                status = w.detailed_status

                bot.send_message(call.message.chat.id, "🌤Температура: " + str(MidleTemperature) +
                                 "°," + " \n💨Ветер: " + str(wind) + "м/c, \n🌫 Облачность: " + str(clouds) + "%")

                if status == 'light rain':
                    bot.send_message(call.message.chat.id,
                                     "Сейчас идет маленький дождь 🌧")
                elif status == 'rain':
                    bot.send_message(call.message.chat.id,
                                     "Сейчас идет дождь 🌧")
                elif status == 'overcast clouds':
                    bot.send_message(call.message.chat.id, "Пасмурно 🌧")
                elif status == 'moderate rain':
                    bot.send_message(call.message.chat.id, "Умеренный дождь 🌧")

            elif call.data == 'pushkino':
                sity = "Пушкино"
                mgr = owm.weather_manager()
                observation = mgr.weather_at_place(sity)
                w = observation.weather

                # Temperature
                MidleTemperature = w.temperature('celsius')['temp']

                wind = w.wind()['speed']
                rain = w.rain
                clouds = w.clouds
                status = w.detailed_status

                bot.send_message(call.message.chat.id, "🌤Температура: " + str(MidleTemperature) +
                                 "°," + " \n💨Ветер: " + str(wind) + "м/c, \n🌫 Облачность: " + str(clouds) + "%")

                if status == 'light rain':
                    bot.send_message(call.message.chat.id,
                                     "Сейчас идет маленький дождь 🌧")
                elif status == 'rain':
                    bot.send_message(call.message.chat.id,
                                     "Сейчас идет дождь 🌧")
                elif status == 'overcast clouds':
                    bot.send_message(call.message.chat.id, "Пасмурно 🌧")
                elif status == 'moderate rain':
                    bot.send_message(call.message.chat.id, "Умеренный дождь 🌧")

            elif call.data == 'other':
                bot.send_message(call.message.chat.id, "Напиши город 👇🏻")

            elif call.data == 'notification':


                config.checker = 1 + config.checker
                if config.checker % 2 == 0:
                    bot.send_message(call.message.chat.id,
                                     'Уведомление о погоде включено ✅')

                    def schedule_checker():
                        while True:
                            schedule.run_pending()
                            sleep(1)

                    def function_to_run():
                        sity = "Москва"
                        mgr = owm.weather_manager()
                        observation = mgr.weather_at_place(sity)
                        w = observation.weather

                        # Temperature
                        MidleTemperature = w.temperature('celsius')['temp']

                        wind = w.wind()['speed']
                        clouds = w.clouds

                        return bot.send_message(call.message.chat.id, "Уведомление🔔\n\n🌤Температура: " + str(MidleTemperature) + "°," + " \n💨Ветер: " + str(wind) + "м/c, \n🌫 Облачность: " + str(clouds) + "%")

                    if __name__ == "__main__":
                        schedule.every().day.at("12:00").do(function_to_run)
                        
                        Thread(target=schedule_checker).start()
                else:
                    bot.send_message(call.message.chat.id,
                                     'Уведомление о погоде вылючено ❌')
                    schedule.clear()

            # remove inline buttons
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="",
                                  reply_markup=None)

            # show alert
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                      text="ЭТО ТЕСТОВОЕ УВЕДОМЛЕНИЕ!!11")

    except Exception as e:
        print(repr(e))


# RUN
bot.polling(none_stop=True)
