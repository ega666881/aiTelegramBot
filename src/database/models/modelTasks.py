from datetime import datetime
from sqlalchemy import Integer, String, DateTime, BigInteger, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import event
from .base import Base

class ModelTask(Base):
    __tablename__ = "models_tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True)
    task_id: Mapped[str] = mapped_column(String, nullable=True)
    model_name: Mapped[str] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    


