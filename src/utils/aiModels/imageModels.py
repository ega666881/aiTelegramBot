from src.utils.cometApi.category.textModels import textModels
from src.utils.cometApi.category.midJModel import mjModel
from src.utils.cometApi.category.gemImageModel import gemModel
from src.database.models.user import User
from aiogram import types
import asyncio
import aiohttp
import re
import base64


async def sendRequest(modelName: str, user: User, promt: str, messagesHistory: list = []):
    modelResponse = await textModels.sendTextRequest(modelName, promt, messagesHistory)

    match = re.search(r'!\[.*?\]\((https?://[^\s)]+)\)', modelResponse['answerText'])
    url = match.group(1)
    modelResponse['answerPhoto'] = url

    return modelResponse

async def sendGemeniRequest(user: User, promt: str):
    data = await gemModel.sendGenerateRequest(promt)
    inline_data = data["candidates"][0]["content"]["parts"][0]["inlineData"]
    image_data_b64 = inline_data["data"]
    mime_type = inline_data["mimeType"] 

    image_bytes = base64.b64decode(image_data_b64)


    ext = mime_type.split("/")[-1]

    photo = types.BufferedInputFile(image_bytes, filename=f"image.{ext}")

    return photo

async def sendMjRequest(modelName: str, user: User, promt: str):
    return await mjModel.sendImageRequest(promt, modelName, user.telegram_id)


async def getImage(imageUrl: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(imageUrl) as resp:
            if resp.status == 200:
                image_data = await resp.read()
                photo = types.BufferedInputFile(image_data, filename="image.png")
                return photo
            else:
                raise Exception(f"Failed to download image: {resp.status}")