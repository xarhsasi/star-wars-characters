from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.models import Base, Timestamps


class User(Base, Timestamps):
    """The User model."""

    __name__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    password: Mapped[str] = mapped_column()
    full_name: Mapped[str] = mapped_column(String(200))
    is_active: Mapped[bool] = mapped_column(default=False)
