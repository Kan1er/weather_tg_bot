from tok import key, apiKey
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import requests
import json

bot = Bot(key)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def info(message:types.Message):
	markup = types.InlineKeyboardMarkup()
	markup.add(types.InlineKeyboardButton("Получить прогноз погоды",callback_data="city"))
	markup.add(types.InlineKeyboardButton("Список команд",callback_data="list"))
	await message.reply("Привет, тут вы можете узнать прогноз погоды", reply_markup=markup)

@dp.message_handler(commands=["listCity"])
async def reply(message: types.Message):
	markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
	markup.add(types.InlineKeyboardButton("Moscow"))
	markup.add(types.InlineKeyboardButton("Minsk"))
	markup.add(types.InlineKeyboardButton("London"))
	await message.reply("Привет",reply_markup=markup)

@dp.callback_query_handler()
async def callback(call):
	if call.data == "list":
		await call.message.answer("/listCity\n/start")
	elif call.data == "city":
		await call.message.answer("Введите город")

@dp.message_handler(content_types=["text"])
async def reply(message:types.Message):
	city = message.text.lower().strip()
	url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&lang=ru&appid={apiKey}&units=metric"
	res = requests.get(url)
	data = json.loads(res.text)
	if res.status_code == 200:
		temp = data['main']['temp']
		humidity = data['main']['humidity']
		pressure = data['main']['pressure']
		wind_speed = data['wind']['speed']
		desc = data['weather'][0]['description']
		list_emoji = ["🌡", "💧", "💨"]
		await message.reply(f"Погода в городе: {message.text}\n"
							f"Температура: {temp}°C{list_emoji[0]}\n"
							f"Влажность: {humidity}% {list_emoji[1]}\n"
							f"Давление: {pressure}Pa\n"
							f"Скорость ветра: {wind_speed} м/с {list_emoji[2]}\n"
							f"Описание: {desc}")

	elif res.status_code == 400:
		await message.reply(f"Город не найден")

executor.start_polling(dp)
