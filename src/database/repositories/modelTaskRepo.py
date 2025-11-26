
from ..models.modelTasks import ModelTask
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, contains_eager
from sqlalchemy import select


class ModelTaskRepo:
    task: ModelTask

    def __init__(self, session: AsyncSession,):
        self.session = session

    async def getAllTasks(self):
        result = await self.session.execute(
            select(ModelTask)
        )
        return result.scalars().all()

    async def deleteTask(self, task: ModelTask):
        await self.session.delete(task)
        await self.session.commit()

    async def createTask(self, task_id: str, telegram_id: int, modelName: str):
        self.session.add(
            ModelTask(
                task_id = task_id,
                telegram_id = telegram_id,
                model_name = modelName
            )
        )
        await self.session.commit()
