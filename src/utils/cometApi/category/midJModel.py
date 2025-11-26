from ..cometApi import CometApi, Endpoints
from ....database.database import AsyncSessionLocal
from ....database.repositories.modelTaskRepo import ModelTaskRepo


class MidJorneyModel(CometApi):
    
    async def checkTask(self, taskId: str):
        return await super().sendGetRequest(
            Endpoints.MIDJ_IMAGE_CHECK_TASK.value + f"{taskId}/fetch"
        )

    async def sendImageRequest(self, promt: str, modelName: str, telegram_id: int):
        async with AsyncSessionLocal() as session:
            taskRepo = ModelTaskRepo(session)
            task = await super().sendPostRequest(Endpoints.MIDJ_IMAGE_CREATE_TASK.value, {
                "prompt": promt,
                "botType": modelName
            })
           
            await taskRepo.createTask(
                task['result'],
                telegram_id,
                'mj',
            )

            return True

    
mjModel = MidJorneyModel()