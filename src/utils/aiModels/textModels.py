from src.utils.cometApi.cometApi import textModels
from src.database.models.user import User


async def sendRequest(modelName: str, user: User, promt: str, messagesHistory: list = []):
    return await textModels.sendTextRequest('gpt-4o', promt, messagesHistory)
