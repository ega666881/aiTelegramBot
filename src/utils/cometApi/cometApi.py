import requests
import config
from enum import Enum
import aiohttp
import asyncio
from typing import Optional, Dict, Any
import random
from src.utils.cometApi.classifyModels import ModelsClasses
from . import classifyModels
import json

baseUrl = config.COMET_API_URL


class Endpoints(Enum):
    GET_MODELS = baseUrl + "/v1/models"
    TEXT_MODEL = baseUrl + "/v1/chat/completions"
    GET_PRICING = baseUrl + "/api/pricing"
    MIDJ_IMAGE_CREATE_TASK = baseUrl + "/mj/submit/imagine"
    MIDJ_IMAGE_CHECK_TASK = baseUrl + "/mj/task/"
    GEMENI_IMAGE = baseUrl + "/v1beta/models/"

class Methods(Enum):
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'

class CometApi:
    models = []
    modelsPrices = {}
    groupedModels = []
    default_headers = {
        'Authorization': 'Bearer ' + config.COMET_API_TOKEN,
        # 'Content-Type': 'application/json',
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
                        print(response)
                        if response.status == 200:
                            try:
                                return await response.json()

                            except:
                                return json.loads(await response.text())


                except aiohttp.ClientError as e:
                    print(e)
                    continue

                if attempt == max_retries:
                    raise Exception(f"Не удалось выполнить {method} запрос после {max_retries + 1} попыток")


                delay = min(base_delay * (2 ** attempt) + random.uniform(0, 1), max_delay)
                await asyncio.sleep(delay)
    
    async def sendStreamingRequest(self, url: str, body: dict):
        headers = {**self.default_headers}
        session = aiohttp.ClientSession()
        try:
            response = await session.post(url, json=body, headers=headers)
            if response.status != 200:
                await response.read() 
                response.close()
                await session.close()
                raise Exception(f"HTTP {response.status}")
            
            return response, session
        except Exception:
            await session.close()
            raise

    async def getModels(self):
        response = await self.sendGetRequest(Endpoints.GET_MODELS.value)
        data = response['data']

        for model in data:
            self.models.append(model["id"])

        self.groupedModels = classifyModels.getClassifyModels(data)
        
    
    async def getPricingModels(self):
        response = await self.sendGetRequest(Endpoints.GET_PRICING.value)
        data = response['data']
        for model in data:
            model_name: str = model["model_name"]
            quota_type = model["quota_type"]
            model_price = model["model_price"]
            if quota_type == 1 and model_price > 0:
                price_with_margin_usd = model_price * float(config.GROUP_RATIO) * float(config.MARGIN)
                cost_in_tokens = price_with_margin_usd / float(config.TOKEN_USD_PRICE)
                self.modelsPrices[model_name] = round(cost_in_tokens)
                
            
            else:
                BASE_PRICE = 1
                C_1K = float(model['model_ratio']) * BASE_PRICE * float(config.GROUP_RATIO)
                P_1K = C_1K / 0.3
                self.modelsPrices[model_name] = round(P_1K)
            
        
        with open('t.json', 'w') as file:
            file.write(json.dumps(self.modelsPrices, indent=4))

    def getModelsByCategory(self, categoryName: str):
        result = []
        for provider, models_list in self.groupedModels[categoryName].items():
            result.extend(models_list)

        return sorted(result)

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



        



cometApi = CometApi()
