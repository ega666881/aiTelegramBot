from datetime import datetime
from sqlalchemy import Integer, String, DateTime, BigInteger, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import event
from .base import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True)
    username: Mapped[str] = mapped_column(String, nullable=True)
    tokens: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    lang: Mapped[str] = mapped_column(String, nullable=True, default='eng')
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    
    selected_models: Mapped["UserSelectedModel"] = relationship(
        "UserSelectedModel",
        back_populates="user",
        uselist=False,  # ← Это ключевое: не list, а один объект
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<User(telegram_id={self.telegram_id}, username={self.username})>"
    
class UserSelectedModel(Base):
    __tablename__ = "user_selected_models"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)
    text_models: Mapped[str] = mapped_column(String, nullable=True)
    audio_models: Mapped[str] = mapped_column(String, nullable=True)
    video_models: Mapped[str] = mapped_column(String, nullable=True)
    image_models: Mapped[str] = mapped_column(String, nullable=True)
    editing_models: Mapped[str] = mapped_column(String, nullable=True)
    other_models: Mapped[str] = mapped_column(String, nullable=True)
    embends_models: Mapped[str] = mapped_column(String, nullable=True)

    user: Mapped["User"] = relationship(back_populates="selected_models")


@event.listens_for(User, "init")
def init_user_selected_models(target, args, kwargs):
    target.selected_models = UserSelectedModel()