from src.utils.cometApi.classifyModels import ModelsClasses
from ..cometApi import CometApi, ModelsClasses, Endpoints
import json

class TextModels(CometApi):

    def __checkValidModel(self, modelName: str):
        if modelName not in super().models:
            return False
        
        else:
            return True
    
    async def sendImageGenerateRequest(self, modelName: str, promt: str, messagesHistory: list = []):
        if self.__checkValidModel(modelName):
            messages = [
                *messagesHistory,
                {
                    "content": promt,
                    "role": "user"
                },
            ]

            response, session = await super().sendStreamingRequest(
                Endpoints.TEXT_MODEL.value, 
                {
                    "model": modelName,
                    "messages": messages,
                    "stream": True,
                }
            )
            try:
                async for line in response.content:
                    line = line.decode("utf-8").strip()
                    if line.startswith("data: "):
                        chunk_str = line[6:]
                        if chunk_str == "[DONE]":
                            break
                        try:
                            chunk = json.loads(chunk_str)
                            delta_content = chunk["choices"][0]["delta"].get("content", "")
                            if delta_content:
                                yield delta_content
                        except (json.JSONDecodeError, KeyError, IndexError):
                            continue
            finally:
                response.close()
                await session.close()


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
        
textModels = TextModels()