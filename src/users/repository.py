import logging

from sqlalchemy import select

from src.repository import Repository
from src.users.models import User

logger = logging.getLogger(__name__)


class UserRepository(Repository[User]):
    """Repository for the User model."""

    _model = User

    async def by_email(self, email: str) -> User | None:
        """Get a user by their email address."""
        stmt = select(User).where(User.email == email)
        return (await self.session.execute(stmt)).scalars().first()
