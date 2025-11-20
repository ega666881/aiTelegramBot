from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery
from ..database.database import AsyncSessionLocal
from ..database.models.user import User, UserRepository


class GetUserRepositoryMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
        event: CallbackQuery,
        data: Dict[str, Any]
    ) -> Any:

        async with AsyncSessionLocal() as session:
            userRepo = UserRepository(session)
            await userRepo.getUser(event.from_user.id)
            data["userRepo"] = userRepo

            return await handler(event, data)