import logging
from typing import Sequence

from sqlalchemy import delete, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.users.exceptions import (
    UserAlreadyExistsError,
    UserBadCredentials,
    UserNotFoundError,
)
from src.users.models import User
from src.users.schemas import UserCreate, UserUpdate
from src.utils.password import (
    BCryptPasswordService,
    PasswordService,
)

logger = logging.getLogger(__name__)


class UserRepository:
    _instance = User

    def __init__(self, session: AsyncSession):
        self.db = session

    async def authenticate(
        self,
        username: str,
        password: str,
        password_service: PasswordService = BCryptPasswordService(),
    ) -> User:
        """Authenticate a user by checking their username and password."""
        stmt = select(self._instance).filter_by(email=username)
        user = (await self.db.execute(statement=stmt)).scalar_one_or_none()
        if user is None:
            raise UserBadCredentials()

        if not password_service.verify(
            plain_password=password, hashed_password=user.password
        ):
            raise UserBadCredentials()

        return user

    async def create_user(
        self,
        user: UserCreate,
        password_service: PasswordService = BCryptPasswordService(),
    ) -> User:
        """Create a new user in the database."""
        # Make sure user is not already in the database.
        stmt = select(self._instance).filter_by(email=user.email)
        user_exists = (await self.db.execute(statement=stmt)).scalar_one_or_none()
        if user_exists is not None:
            raise UserAlreadyExistsError(email=user.email)

        # Hash the user's password before storing it in the database.
        hashed_password = password_service.hash(plain_password=user.password)
        # Add the newbie to the database.
        db_user = User(
            full_name=user.full_name,
            email=user.email,
            password=hashed_password,
        )
        self.db.add(db_user)
        await self.db.commit()
        logger.debug("User created: %s", db_user)
        return db_user

    async def retrieve_user(self, user_id: int) -> User:
        """Retrieve a single user from the database by providing the user's ID."""
        user = await self.db.get(self._instance, user_id)
        logger.debug("User retrieved: %s", user)
        if user is None:
            raise UserNotFoundError(identifier=user_id)
        return user

    async def users(self) -> Sequence[User]:
        """Retrieve all users from the database."""
        users = (await self.db.execute(select(self._instance))).scalars().all()
        logger.debug("Users retrieved: len %s", len(users))
        return users

    async def update_user(self, user_id: int, user: UserUpdate) -> User:
        """Update a user in the database."""
        db_user = await self.db.get(self._instance, user_id)
        if db_user is None:
            raise UserNotFoundError(identifier=user_id)

        try:
            await self.db.execute(
                update(self._instance)
                .where(self._instance.id == db_user.id)
                .values(**user.model_dump(exclude_unset=True, exclude_defaults=True))
            )
        except IntegrityError as e:
            # TODO: This should be UniqueValidationError not the generic IntegrityError.
            raise UserAlreadyExistsError(email=user.email) from e

        await self.db.commit()
        await self.db.refresh(db_user)
        logger.debug("User was updated to: %s", db_user)
        return db_user

    async def delete_user(self, user_id: int) -> int:
        """Delete a user from the database."""
        deleted_user = await self.db.execute(
            delete(self._instance).where(self._instance.id == user_id)
        )
        if deleted_user.rowcount == 0:
            raise UserNotFoundError(identifier=user_id)
        await self.db.commit()
        logger.debug("User deleted: %s", user_id)
        return deleted_user.rowcount
