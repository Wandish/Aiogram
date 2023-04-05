from dotenv import load_dotenv, find_dotenv
from os import getenv
import logging
from chatids import chatids_users
from aiogram import Bot, Dispatcher, executor, types
import text


# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
load_dotenv(find_dotenv()) #подгрузить файл .env
bot = Bot(getenv('TEST_TOKEN')) #прочитать фай
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def language_selection(message: types.Message):
    #Если chat.id нет в сете (chatids_users) то добавляет
    if not str(message.from_user.id) in chatids_users:
        chatids_users.add(message.from_user.id)
        #Если chat.id нет в файле (chatids.txt) то добавляет
        try:
            if str(message.from_user.id) not in open('chatids.txt').read():
                chatids_file = open("chatids.txt", "a")
                chatids_file.write(str(message.from_user.id) + "\n")
                chatids_file.close()
        except FileNotFoundError as e:
            print(e) #---Записать в логинг----
            #Создание chatids.txt
            open("chatids.txt", "w").close()
    await bot.send_chat_action(message.from_user.id, 'typing')
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton(text = "🇺🇦Українська")
    btn2 = types.KeyboardButton(text ="🇬🇧English")
    kb.add(btn1, btn2,)
    await bot.send_message(message.from_user.id, text=text.language_selection, parse_mode="HTML")
    await bot.send_message(message.from_user.id, text=text.button_driver, parse_mode="HTML")
    await bot.send_message(message.from_user.id, text=text.eng_button_driver, parse_mode="HTML", reply_markup=kb)
    # await message.delete()


@dp.message_handler()
async def echo(message: types.Message):
    # old style:
    # await bot.send_message(message.from_user.id, message.text)

    await message.answer(message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)