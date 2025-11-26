import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from src.routes.start import start
from config import BOT_TOKEN
from src.database.database import init_db
from src.routes.profile import profile
from src.routes.payments import payments
from src.routes.aiModels.textModels import textModels
from src.routes.aiModels import aiModels
from src.utils.cometApi.cometApi import cometApi
from src.middlewares.getUserRepositoryMiddleware import GetUserRepositoryMiddleware
from src.utils.cometApi.checkTasksModels import checkTasksModels

logging.basicConfig(level=logging.INFO)

async def main():
    await init_db()
    await cometApi.getModels()
    await cometApi.getPricingModels()

    

    bot = Bot(token=BOT_TOKEN)
    asyncio.create_task(checkTasksModels(bot))
    dp = Dispatcher(storage=MemoryStorage())
    dp.callback_query.middleware(GetUserRepositoryMiddleware())
    dp.include_routers(
        start.router, 
        profile.router,
        payments.router,
        textModels.router,
        aiModels.router,
    )

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())