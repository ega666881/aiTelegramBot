import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from src.routes.start import start
from config import BOT_TOKEN
from src.database.database import init_db
from src.routes.profile import profile
from src.routes.payments import payments
from src.routes.textModels import textModels
from src.utils.cometApi.cometApi import cometApi, textModels as textModelsApi

logging.basicConfig(level=logging.INFO)

async def main():
    await init_db()
    await cometApi.getModels()

    print(await textModelsApi.sendTextRequest('gpt-4o', 'Привет'))
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())
    
    dp.include_routers(
        start.router, 
        profile.router,
        payments.router,
        textModels.router
    )

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())