from dotenv import load_dotenv, find_dotenv
from os import getenv
import logging
from aiogram import Bot, Dispatcher, executor, types
import text

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
load_dotenv(find_dotenv()) #подгрузить файл .env
bot = Bot(getenv('TEST_TOKEN')) #прочитать фай
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await bot.send_chat_action(message.chat.id, 'typing')
    await message.answer(text=text.language_selection)
    await message.answer(text=text.button_driver)
    await message.answer(text=text.eng_button_driver)
    # await message.delete()


@dp.message_handler()
async def echo(message: types.Message):
    # old style:
    # await bot.send_message(message.chat.id, message.text)

    await message.answer(message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)