import requests
import config
from enum import Enum
import aiohttp
import asyncio
from typing import Optional, Dict, Any
import random


baseUrl = config.COMET_API_URL


class Endpoints(Enum):
    GET_MODELS = baseUrl + "/v1/models"
    TEXT_MODEL = baseUrl + "/v1/chat/completions"

class Methods(Enum):
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'

class CometApi:
    models = []
    default_headers = {
        'Authorization': 'Bearer ' + config.COMET_API_TOKEN
    }

    async def __fetchWithRetry(
        self,
        method: str,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        max_retries: int = 10,
        base_delay: float = 1.0,
        max_delay: float = 60.0,
    ):
        
        merged_headers = {**self.default_headers, **(headers or {})}

        async with aiohttp.ClientSession() as session:
            for attempt in range(max_retries + 1):
                try:
                    async with session.request(
                        method=method,
                        url=url,
                        params=params,
                        json=json_data,
                        headers=merged_headers,
                    ) as response:

                        if response.status == 200:
                            return await response.json() 


                except aiohttp.ClientError as e:
                    continue

                if attempt == max_retries:
                    raise Exception(f"Не удалось выполнить {method} запрос после {max_retries + 1} попыток")


                delay = min(base_delay * (2 ** attempt) + random.uniform(0, 1), max_delay)
                await asyncio.sleep(delay)

    async def getModels(self):
        response = await self.sendGetRequest(Endpoints.GET_MODELS.value)

        for model in response['data']:
            self.models.append(model["id"])
            
    async def sendPostRequest(
            self,
            url: str,
            body: dict,
    ):
        return await self.__fetchWithRetry(Methods.POST.value, url, json_data=body)

    async def sendGetRequest(
            self,
            url: str,
            params: dict = None
        ):
        return await self.__fetchWithRetry(Methods.GET.value, url, params)

    




class TextModels(CometApi):

    def __checkValidModel(self, modelName: str):
        if modelName not in super().models:
            return False
        
        else:
            return True
        
    async def sendTextRequest(self, modelName: str, promt: str, messagesHistory: list = []):
        if self.__checkValidModel(modelName):

            messages = [
                *messagesHistory,
                {
                    "content": promt,
                    "role": "user"
                },
            ]

            responseJson = await super().sendPostRequest(
                Endpoints.TEXT_MODEL.value, 
                {
                    "model": modelName,
                    "messages": messages,
                }
            )

            answerModel = responseJson['model']
            answerMessage = responseJson['choices'][0]['message']

            return {
                "model": answerModel,
                "answerText": answerMessage['content'],
                "answer": answerMessage,
            }
        
        else:
            return False
        



cometApi = CometApi()
textModels = TextModels()