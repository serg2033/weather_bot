import requests
import datetime
from config import tg_bot_token, open_weather_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor



bot = Bot(token=tg_bot_token)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply("hi! welcome to bot!")

@dp.message_handler(commands=["help"])
async def help(message: types.Message):
    await message.reply("""
    The following commands are avelible:

    /start -> Welcome message
    /help -> This Message
    """)




@dp.message_handler()
async def get_weather(message: types.Message):

    code_to_smile = {
        'Clear': 'Clear \U00002600',
        'Clouds': 'Clouds \U00002601',
        'Rain': 'Rain \U00002614',
        'Drizzle': 'Drizzle \U00002614',
        'Thunderstorm': 'Thunderstorm \U000026A1',
        'Snow': 'Snow \U0001F328',
        'Mist': 'Mist \U0001F32B',
    }

    try:
        r = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric"
        )
        data = r.json()

        city = data["name"]
        cur_weather = data["main"]["temp"]

        weather_description = data["weather"][0]["main"]
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = "Look out the window. I don't know what's there :)"

        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        sunrise = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        lenght_of_the_day = datetime.datetime.fromtimestamp(
            data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(data["sys"]["sunrise"])

        await message.reply(f'---{datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}---\n'
              f'The weather in {city}\nTemperature {cur_weather}°C {wd}\n'
              f'Humidity {humidity}%\nPressure {pressure} mmhg\nWind {wind} m/s\n'
              f'Sunrise {sunrise}\nSunset {sunset}\nLength of the day {lenght_of_the_day}\n'
              f'Have a good day!'
              )

    except:
        await message.reply("\U00002620 check the name of city")



if __name__ == '__main__':
    executor.start_polling(dp)