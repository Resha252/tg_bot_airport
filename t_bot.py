#pip install aiogram

import json
from config import token
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from arrival import get_data, check_update

bot = Bot(token=token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

"""Функция создает необходимые нам кнопки в боте по команде /start"""
@dp.message_handler(commands="start")
async def start(message: types.Message):
    start_buttons = ['Все рейсы', 'Ожидаемые рейсы']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)

    await message.answer("Расписание рейсов", reply_markup=keyboard)

"""Функция отпраляет пользователь сообщения с информацией о всех прибывающих рейсах при нажатии на кновку Все рейсы"""
@dp.message_handler(Text(equals="Все рейсы"))
async def start_message(message: types.Message):
    url = "https://airportufa.ru/scoreboard/arrival/"
    get_data(url)      #вызываем функцию тем самым запуская парсер и обновляя информацию о рейсах в файле arrival_dict.json

    with open("arrival_dict.json") as file:
        arrival_dict = json.load(file)                    #читаем информциию о рейсах из arrival_dict.json

    for k, v in arrival_dict.items():                     #формируем отправлемое пользователю сообщение
        arrival = f"<b>{v['time']}</b>\n" \
                  f"<u>{v['city']}</u>\n" \
                  f"<u>{v['status']}</u>\n" \
                  f"Терминал №<b>{v['terminal']}</b>\n" \
                  f"{v['url']}"
        await message.answer(arrival)                    #отправлем сообщения

"""Функция отпраляет пользователь сообщения с информацией об ожидаемых рейсах при нажатии на кнопку Ожидаемые рейсы"""
@dp.message_handler(Text(equals="Ожидаемые рейсы"))
async def update_dict(message: types.Message):
    url = "https://airportufa.ru/scoreboard/arrival/"

    arrival_update = check_update(url)             #вызываем фнкцию-парсер chrck_update которая возвращает нам информацию только о жидаемых рейсах

    if len(arrival_update) >= 1:
        for k, v in arrival_update.items():        #формируем отправлемое пользователю сообщение
            arrival = f"<b>{v['time']}</b>\n" \
                      f"<u>{v['city']}</u>\n" \
                      f"<u>{v['status']}</u>\n" \
                      f"Терминал №<b>{v['terminal']}</b>\n" \
                      f"{v['url']}"
            await message.answer(arrival)          #отправлем сообщения
    else:
        await message.answer('На сегодня ожидаемых рейсов нет')

if __name__ == '__main__':
    executor.start_polling(dp)
