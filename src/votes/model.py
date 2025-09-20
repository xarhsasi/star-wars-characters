from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    SmallInteger,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from src.films.models import Film
from src.models import Base, Timestamps
from src.users.models import User


class Vote(Base, Timestamps):
    __tablename__ = "votes"
    __table_args__ = (UniqueConstraint("user_id", "film_id", name="uq_vote_user_film"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey(User.id, ondelete="CASCADE"), index=True
    )
    film_id: Mapped[int] = mapped_column(
        ForeignKey(Film.id, ondelete="CASCADE"), index=True
    )
    value: Mapped[int] = mapped_column(SmallInteger)
    feedback: Mapped[str] = mapped_column(String, nullable=True)
