from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..database.models.user import User

async def getUser(session: AsyncSession, telegram_id: int) -> User:
    result = await session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
    return result.scalar_one_or_none()