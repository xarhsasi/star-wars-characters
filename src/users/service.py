from sqlalchemy.ext.asyncio import AsyncSession

from src.users.exceptions import (
    UserBadCredentials,
)
from src.users.models import User
from src.users.repository import UserRepository
from src.utils.password import (
    BCryptPasswordService,
    PasswordService,
)


class UserAuthenticationService:
    """Service class for authentication-related operations."""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.user_repository = UserRepository(session=session)

    async def authenticate(
        self,
        email: str,
        password: str,
        password_service: PasswordService = BCryptPasswordService(),
    ) -> User:
        """Authenticate a user by checking their email and password.

        If user is not found or password does not match, raises UserBadCredentials.
        """
        user = self.user_repository.by_email(email=email)
        if user is None:
            raise UserBadCredentials()

        if not password_service.verify(
            plain_password=password, hashed_password=user.password
        ):
            raise UserBadCredentials()

        return user


class UserService:
    """Service class for user-related operations."""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.authentication_service = UserAuthenticationService(session=session)
