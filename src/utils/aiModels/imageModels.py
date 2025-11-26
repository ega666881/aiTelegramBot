from src.utils.cometApi.category.textModels import textModels
from src.utils.cometApi.category.midJModel import mjModel
from src.database.models.user import User
from aiogram import types
import asyncio
import re

async def sendRequest(modelName: str, user: User, promt: str, messagesHistory: list = []):
    modelResponse = await textModels.sendTextRequest(modelName, promt, messagesHistory)

    match = re.search(r'!\[.*?\]\((https?://[^\s)]+)\)', modelResponse['answerText'])
    url = match.group(1)
    modelResponse['answerPhoto'] = url

    return modelResponse


async def sendMjRequest(modelName: str, user: User, promt: str):
    return await mjModel.sendImageRequest(promt, modelName, user.telegram_id)