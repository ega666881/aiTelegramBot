from src.utils.cometApi.category.textModels import textModels
from src.database.models.user import User


async def sendRequest(modelName: str, user: User, promt: str, messagesHistory: list = []):
    return await textModels.sendTextRequest('gpt-4o', promt, messagesHistory)
