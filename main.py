from dotenv import load_dotenv
import pymysql
import os
from os.path import join, dirname
import telebot
from aiogram import types, Bot
from aiogram.types.web_app_info import WebAppInfo
#from aiogram.utils import executor
from aiogram import Bot, Dispatcher, executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, Message


connection = pymysql.connect(host='localhost',
                             user='root',
                             password=''
                             )


API_TOKEN = '7060384912:AAGVitlqlRapKPWnEHkml0WkWw-GQR2be6I'
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)




@dp.message_handler(commands=['start'])
async def send_welcome(message: Message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    button = KeyboardButton("Web версия", web_app=WebAppInfo(url='https://telegram.mihailgok.ru'))
    keyboard.add(button)
    await message.answer("Привет!Нажми на кнопку для перехода на web", reply_markup=keyboard)



# Создаем объект курсора для выполнения SQL запросов
cursor = connection.cursor()

# Создаем базу данных
cursor.execute("CREATE DATABASE IF NOT EXISTS lioncetf_name")

# Выбираем созданную базу данных
cursor.execute("USE lioncetf_name")

# Создаем таблицу
cursor.execute("CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(255))")

@dp.message_handler(commands=['register'])
async def handle_start(message: Message):
    username = message.from_user.username
    # Проверка,осуществует ли пользователь в базе данных
    cursor.execute("SELECT * FROM users WHERE username = %s", (username))
    result = cursor.fetchone()
    if result:
        await message.answer('Вы уже зареганы')
    else:
         sql = "INSERT INTO users (username) VALUES (%s)"
         val = (username)
         cursor.execute(sql, val)
         await message.answer('Вы успешно зареганы')
# Фиксируем изменения
         connection.commit()
         #connection.close()
# Закрываем соединение с базой данных

        # cursor.close()

@dp.message_handler(commands=['delete'])
async def handle_start(message: Message):
    username = message.from_user.username
    # Проверка, существует ли пользователь в базе данных
    cursor.execute("SELECT * FROM users WHERE username = %s", (username))
    result = cursor.fetchone()
    if result:
# Удаляем пользователя из базы данных
         cursor.execute("DELETE FROM users WHERE username = %s", (username,))
         connection.commit()
         await message.answer('Вы успешно удалены')
    else:
         await message.answer('Вы не найдены')
         #connection.close()
# Закрываем соединение с базой данных
         #cursor.close()



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
