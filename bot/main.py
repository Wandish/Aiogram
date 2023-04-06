from bot import dp,bot,chatids_users, logger,user_languages
from aiogram import executor, types
from aiogram.utils.exceptions import BotBlocked
import text

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
            # Создание chatids.txt
            open("chatids.txt", "w").close()
            logger.error(e)
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
            
# Команда /share - Главное меню
@dp.message_handler(commands=['share'])#Не переводиться на англ.
async def share (message: types.Message):
    await bot.send_chat_action(message.from_user.id, 'typing')
    if message.from_user.id in user_languages and user_languages[message.from_user.id] == '🇬🇧English':
        await bot.send_message(message.from_user.id, text=text.eng_zag_share, parse_mode='HTML')
        await bot.send_message(message.from_user.id, text=text.eng_osn_share, parse_mode='HTML')
    else:
        await bot.send_message(message.from_user.id, text=text.zag_share, parse_mode='HTML')
        await bot.send_message(message.from_user.id, text=text.osn_share, parse_mode='HTML')

#Команда /send - Главное меню
@dp.message_handler(commands=['send'])
async def send_a_message(message: types.Message):
    #Проверка на админа
    if message.from_user.id in (759572442, 402411612):
        for user in chatids_users:
            try:
                await bot.send_message(user, message.text[message.text.find(' '):])
            except BotBlocked as e:
                logger.error(f'{e}: {user}')
    #если не админ выбивает стандартную (непонимайку)
    else:
        await bot.send_chat_action(message.from_user.id, 'typing')
        if message.from_user.id in user_languages and user_languages[message.from_user.id] == '🇬🇧English':
            await bot.send_message(message.from_user.id, text=text.eng_nezrozymiv, parse_mode='HTML')
            await bot.send_photo(message.from_user.id, open('image/nezrozymiv.jpg', 'rb'))
        else:
            await bot.send_message(message.from_user.id, text=text.nezrozymiv, parse_mode='HTML')
            await bot.send_photo(message.from_user.id, open('image/nezrozymiv.jpg', 'rb'))

if __name__ == '__main__':
    logger.info("Старт")
    executor.start_polling(dp, skip_updates=True)