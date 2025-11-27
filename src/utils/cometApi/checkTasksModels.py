from aiogram import Bot, types
from enum import Enum
from src.database.repositories.userRepo import UserRepository
from ...database.database import AsyncSessionLocal
from ...database.models.modelTasks import ModelTask
from ...database.repositories.modelTaskRepo import ModelTaskRepo
from ..cometApi.category.midJModel import mjModel
from src.utils.aiModels import imageModels
from src.routes.aiModels.imageModels.keyboards.mjAnswerKeyboard import mjAnswerKeyboard
import asyncio

class TasksCometStatus(Enum):
    SUCCESS = 'SUCCESS'

async def checkTasksModels(bot: Bot):
    while True:
        async with AsyncSessionLocal() as session:
            tasksRepo = ModelTaskRepo(session)
            userRepo = UserRepository(session)
            
            tasks = await tasksRepo.getAllTasks()
            for task in tasks:
                await userRepo.getUser(task.telegram_id)
                if task.model_name == 'mj':
                    taskResult = await mjModel.checkTask(task.task_id)
                    if taskResult['status'] == TasksCometStatus.SUCCESS.value:
                        
                        await bot.send_photo(
                            task.telegram_id,
                            photo=await imageModels.getImage(taskResult['imageUrl']),
                            reply_markup=mjAnswerKeyboard(userRepo.locale.image_models_locale.getMjAnswerButtons(), taskResult['image_urls'])
                        )
                        await tasksRepo.deleteTask(task)
        
        await asyncio.sleep(5)