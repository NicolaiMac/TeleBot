from threading import Thread
import time
import sqlite3
import telebot
import pyowm
from colorama import init
from colorama import Fore, Back, Style
init()
print(Back.GREEN)
print(Fore.BLACK)
city = []
import codecs
with  codecs.open( "cities.txt", "r", "utf_8_sig" ) as f:
	for line in f:
		for word in line.split():
			city.append(word) 
bot = telebot.TeleBot("803245127:AAEdeY4Q9RMRG8xgfUlJ_r_QduIzXxuxcQc")
owm = pyowm.OWM('6d00d1d4e704068d70191bad2673e0cc', language = "ru")
def send_weather(bot):
	spam = False
	while(True):
		minut = time.strftime("%Y%m%d%H %M %S", time.localtime()).split()
		if (minut[1] == '00') and (spam == False):
			spam = True
			conn = sqlite3.connect('my.db')
			db_c = conn.cursor()
			db_c.execute('SELECT * FROM users')
			row = db_c.fetchone()
			while row is not None:
				observation = owm.weather_at_place(row[2])
				w = observation.get_weather()
				answer = "В городе " + row[2] +" сейчас " + w.get_detailed_status() + "\nТемпература: " + str(round(w.get_temperature('celsius')["temp"])) + " градусов" + "\nВлажность: " + str(w.get_humidity()) + "%" + "\nСкорость ветра: " + str(w.get_wind()["speed"]) + " м/с"
				bot.send_message(row[1], answer)
				row = db_c.fetchone()
			db_c.close()
			conn.close()
		if (minut[1]=='01'):
			spam = False
Thread(target=send_weather, args=(bot,)).start()
@bot.message_handler(content_types=['text'])
def send_echo(message):
	inputed = message.text.split()
	print(message.chat.id)
	print(inputed[0])
	check = False
	check2 = False
	for c in city:
		if (len(inputed)==1):
			if ((inputed[0] == c)):
				check =       True
				place = inputed[0]
				break
			else:
				check = False
		elif(len(inputed)==2):
			if ((inputed[1] == c)):
				check2 =       True
				place  = inputed[1]
				break
			else:
				check2 = False
		else:
			check  = False
			check2 = False
	if check:
		observation = owm.weather_at_place(place)
		w = observation.get_weather()
		answer = "В городе " + place +" сейчас " + w.get_detailed_status() + "\nТемпература: " + str(round(w.get_temperature('celsius')["temp"])) + " градусов" + "\nВлажность: " + str(w.get_humidity()) + "%" + "\nСкорость ветра: " + str(w.get_wind()["speed"]) + " м/с"
		bot.send_message(message.chat.id, answer)				
	elif (inputed[0] == "/start") or (inputed[0] == "/help"):
		print(inputed[0])
		bot.send_message(message.chat.id, "Здравтсвуйте, я погодный флекс бот или же просто бот для Игоря.\nЯ могу подсказать вам погоду в любом(практически) городе России.\nЕсли вы желаете подключить рассылку, то напишите мне '/addme (название города с большой буквы)'. Подключить можно только один город, но мой хозяин работает над тем, что бы увеличить колиство подключаемых городов \nЕсли вы уверенны что указали город верно, но я почему-то не знаю этот город, то сообщите об этом моему создателю по почте: nikita.yurikof@yandex.ru\nЧто бы увидеть это сообщение еще раз отправьте мне '/help'")
	elif ((inputed[0] == '/addme') and check2):
		conn = sqlite3.connect('my.db')
		db_c = conn.cursor()
		print('Новый')
		param = (int(message.chat.id),inputed[1])
		db_c.execute("INSERT INTO users (name, city) VALUES (?,?)",param)
		conn.commit()
		db_c.close()
		conn.close()
		print('complete')
		bot.send_message(message.chat.id, 'Поздравляем, теперь вы будете каждый час получать данные о погоде в городе ' + inputed[1] +'. \nЕсли вы хотите отказаться от рассылки просто напишите мне /removeme и я все сделаю сам')
	elif(inputed[0]=='/removeme'):
		conn = sqlite3.connect('my.db')
		db_c = conn.cursor()
		db_c.execute("DELETE FROM users WHERE name=?",(int(message.chat.id),))
		conn.commit()
		db_c.close()
		conn.close()
		bot.send_message(message.chat.id, 'Теперь вам не будут приходить уведомления о погоде')
	else:	
		bot.send_message(message.chat.id, "Пожалуйста введите название города")
bot.polling(none_stop = True)
input()