from aiogram import Bot, types
from ...database.database import AsyncSessionLocal
from ...database.models.modelTasks import ModelTask
from ...database.repositories.modelTaskRepo import ModelTaskRepo
from ..cometApi.category.midJModel import mjModel
import asyncio

async def checkTasksModels(bot: Bot):
    while True:
        async with AsyncSessionLocal() as session:
            tasksRepo = ModelTaskRepo(session)
            tasks = await tasksRepo.getAllTasks()
            for task in tasks:
                if task.model_name == 'mj':
                    taskResult = await mjModel.checkTask(task.task_id)
                    if taskResult['status'] == 'SUCCESS':
                        media_group = [
                            types.InputMediaPhoto(media=url) for url in taskResult['image_urls']
                        ]

                        await bot.send_media_group(task.telegram_id, media_group)
                        await tasksRepo.deleteTask(task)
        
        await asyncio.sleep(10)