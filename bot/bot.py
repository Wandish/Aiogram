from dotenv import load_dotenv, find_dotenv
from aiogram import Bot, Dispatcher
from os import path, getenv, mkdir
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime

# Конфигурация
load_dotenv(find_dotenv()) #подгрузить файл .env
bot = Bot(getenv('TEST_TOKEN')) #прочитать фай
dp = Dispatcher(bot)

# Создание словоря с iD и выбранным языком
user_languages = {}

#Проверят создан ли файл chatids.txt
if not path.exists("chatids.txt"):
    open("chatids.txt", "w").close()
#Загрузка массива с файла в SET (Разсылка идет по SET, не по файлу (файл выступает в роли истории))
chatids_file = open("chatids.txt", "r")
chatids_users = set ()
for line in chatids_file:
    chatids_users.add(line.strip())
chatids_file.close()

# создаем логгер и задаем уровень логирования
logger = logging.getLogger("main.py")
logger.setLevel(logging.INFO)
# создаем объект класса Formatter для форматирования вывода логов
formatter = logging.Formatter('%(asctime)s (%(filename)s:%(lineno)d %(threadName)s %(funcName)s) %(levelname)s - %(name)s: "%(message)s"',' %Y.%m.%d %H:%M:%S')
# создаем обработчик для вывода сообщений лога в консоль
console_output_handler = logging.StreamHandler()
console_output_handler.setLevel(logging.INFO)
console_output_handler.setFormatter(formatter)
# создаем обработчик для вывода сообщений лога в файл
if not path.exists("logs"):
    mkdir("logs")
log_file_path = "logs/" + datetime.now().strftime("%Y.%m.%d-%H.%M.%S") + ".log"
file_output_handler = RotatingFileHandler(log_file_path, mode='a', maxBytes=10485760, backupCount=5, encoding='utf-8', delay=False)
file_output_handler.setLevel(logging.INFO)
file_output_handler.setFormatter(formatter)
# добавляем обработчики к логгеру
logger.addHandler(console_output_handler)
logger.addHandler(file_output_handler)