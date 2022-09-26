import requests
import datetime
from config import open_weather_token
from aiogram import types,Dispatcher
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
import os
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup,KeyboardButton,ReplyKeyboardRemove

async def on_startup(_):
    print('БОТ В ОНЛАЙНІ')

bot=Bot(token=os.getenv('TOKEN'))
dp=Dispatcher(bot)
#Start commands
@dp.message_handler(commands=['start'])
async def commands_start(message:types.Message):

    try:
        kb_client = ReplyKeyboardMarkup(resize_keyboard=True)
        b1 = KeyboardButton('Львів')
        b2 = KeyboardButton('Київ')
        b3 = KeyboardButton('Харків')
        b4 = KeyboardButton('Одеса')
        b5 = KeyboardButton('Хмельницький')
        kb_client.add(b1).add(b2).add(b3).add(b4).add(b5)
        await bot.send_message(message.from_user.id,'Привіт,Ведить 🏙Місто де хочете дізнатися погоду:',reply_markup=kb_client)
        await message.delete()
    except:
        await message.reply('спілкуваання тільки через пп :\n t.me/koplviv_bot')

@dp.message_handler(content_types='text')
async def get_weather(message: types.Message):
    code_to_smile = {
        "Clear": "Ясно☀\U00002600",
        "Clouds": "Хмарно⛅\U00002601",
        "Rain": "Дощ🌦\U00002614",
        "Drizzle": "Дощ🌦\U00002614",
        "Thunderstorm": "Гроза⛈\U000026A1",
        "Snow": "Сніг❄\U0001F328",
        "Mist": "Туман🌫\U0001F32B"
    }

    try:
        r = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric"
        )
        data = r.json()

        city = data["name"]
        cur_weather = data["main"]["temp"]
        #max_weather = data["main"]["temp_max"]
        #min_weather = data["main"]["temp_min"]

        weather_description = data["weather"][0]["main"]
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = "Подивись за вікном, не можу зрозуміти що за погода!"

        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        length_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(
            data["sys"]["sunrise"])

        await message.reply(f"🟡🔵{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}🟡🔵\n"
              f"🏙Погода в Місті: {city}\n🌡Температура: {cur_weather}C° {wd}\n"
              #f"Максимальна температура:{max_weather}\nМінімальна температура{min_weather}\n"              
              f"💧Вологість: {humidity}%\n🌍Атмосферний Тиск: {pressure} мм.рт.ст\n💨Вітер: {wind} м/с\n"
              f"🌄Схід Сонця: {sunrise_timestamp}\n🌅Захід Сонця: {sunset_timestamp}\n🕚Тривалість дня: {length_of_the_day}\n"
              f"📎Гарного дня!🇺🇦📎"
              )

    except:
        await message.reply("\U00002620 Перевірьте Назву Міста \U00002620")













executor.start_polling(dp,skip_updates=True,on_startup=on_startup)
