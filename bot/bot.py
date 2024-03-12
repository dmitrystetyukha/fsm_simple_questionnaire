import logging

from aiogram import Bot

with open(".manager_tg_id") as manager_tg_id_file:
    MANAGER_TG_ID = manager_tg_id_file.read().replace("\n", "")

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
with open(".tg_token") as bot_token_file:
    bot = Bot(token=bot_token_file.read().replace("\n", ""))
