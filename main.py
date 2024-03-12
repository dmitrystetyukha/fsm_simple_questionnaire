import asyncio

from aiogram import Dispatcher

from bot import bot
from routers.agreement import AGREEMENT_ROUTER
from routers.questions import QUESTIONS_ROUTER

dp = Dispatcher()


# Запуск процесса поллинга новых апдейтов
async def main():
    dp.include_routers(AGREEMENT_ROUTER, QUESTIONS_ROUTER)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
