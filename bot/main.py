from dotenv import load_dotenv, find_dotenv
from os import getenv
import logging
from chatids import chatids_users
from aiogram import Bot, Dispatcher, executor, types
import text

# Запись логов
logging.basicConfig(level=logging.INFO)

# Конфигурация
load_dotenv(find_dotenv()) #подгрузить файл .env
bot = Bot(getenv('TEST_TOKEN')) #прочитать фай
dp = Dispatcher(bot)

# Создание словоря с iD и выбранным языком
user_languages = {}

# Команда /start - выбор языка
@dp.message_handler(commands=['start'])
async def language_selection(message: types.Message):
    # Если chat.id нет в сете (chatids_users) то добавляет
    if not str(message.from_user.id) in chatids_users:
        chatids_users.add(message.from_user.id)
        # Если chat.id нет в файле (chatids.txt) то добавляет
        try:
            if str(message.from_user.id) not in open('chatids.txt').read():
                chatids_file = open("chatids.txt", "a")
                chatids_file.write(str(message.from_user.id) + "\n")
                chatids_file.close()
        except FileNotFoundError as e:
            print(e) #---Записать в логинг----
            # Создание chatids.txt
            open("chatids.txt", "w").close()
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton(text = "🇺🇦Українська")
    btn2 = types.KeyboardButton(text ="🇬🇧English")
    kb.add(btn1, btn2)
    await bot.send_chat_action(message.from_user.id, 'typing')
    await bot.send_message(message.from_user.id, text=text.language_selection, parse_mode="HTML")
    await bot.send_message(message.from_user.id, text=text.button_driver, parse_mode="HTML")
    await bot.send_message(message.from_user.id, text=text.eng_button_driver, parse_mode="HTML", reply_markup=kb)
    # await message.delete()

# Функция для записи выбранного языка в словарь (user_languages)
@dp.message_handler(lambda message: message.text in ['🇺🇦Українська', '🇬🇧English'])
async def language_preservation(message: types.Message):
    user_languages[message.from_user.id] = message.text
    await bot.send_chat_action(message.from_user.id, 'typing')
    await bot.send_photo(message.from_user.id, open('image/start.jpg', 'rb'))
    await main_menu (message)
    
# Команда /menu - Главное меню
@dp.message_handler(commands=['menu'])
async def main_menu(message: types.Message):
        await bot.send_chat_action(message.from_user.id, 'typing')
        if message.from_user.id in user_languages and user_languages[message.from_user.id] == '🇬🇧English':
            await bot.send_message(message.from_user.id, text = text.eng_privetstvie)
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            btn1 = types.KeyboardButton(text = "\U0001f64fHelp the project")
            btn2 = types.KeyboardButton(text="\U0001faf6About us")
            kb.add(btn1, btn2)
            await bot.send_message(message.from_user.id, text=text.eng_button_driver,reply_markup=kb)
        else:
            await bot.send_message(message.from_user.id, text = text.privetstvie)
            kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            btn1 = types.KeyboardButton(text = "\U0001f198Отримати допомогу")
            btn2 = types.KeyboardButton(text ="\U0001f64fДопомогти проекту")
            btn3 = types.KeyboardButton(text ="\U0001f3ebОсвітні заходи")
            btn4 = types.KeyboardButton(text="\U0001faf6Про нас")
            kb.add(btn1, btn2, btn3, btn4)
            await bot.send_message(message.from_user.id, text=text.button_driver,reply_markup=kb)



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)