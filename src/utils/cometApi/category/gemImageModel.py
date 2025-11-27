from ..cometApi import CometApi, Endpoints
from ....database.database import AsyncSessionLocal
from ....database.repositories.modelTaskRepo import ModelTaskRepo


class GemeniImageModel(CometApi):
    

    async def sendGenerateRequest(self, promt: str):

        response = await super().sendPostRequest(Endpoints.GEMENI_IMAGE.value + 'gemini-3-pro-image:generateContent', {
            "contents": [
                {
                    "role": 'user',
                    "parts": [
                        {
                            'text': promt,
                        }
                    ]
                }
            ],
            "generationConfig": {
                "responseModalities": [
                    "IMAGE"
                ],
                "imageConfig": {
                    "aspectRatio": "9:16"
                }
            }
        })
        
        return response

    
gemModel = GemeniImageModel()