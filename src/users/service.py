from sqlalchemy.ext.asyncio import AsyncSession

from src.exceptions import ORMDuplicateException
from src.service import CreateORMService, GetORMService
from src.users.exceptions import (
    UserAlreadyExistsError,
    UserBadCredentials,
)
from src.users.models import User
from src.users.repository import UserRepository
from src.utils.password import (
    BCryptPasswordService,
    PasswordService,
)


class UserService(GetORMService[User], CreateORMService[User]):
    """Service class for user-related operations."""

    def __init__(self, session: AsyncSession):
        self.session = session
        self._repository = UserRepository(session=session)

    async def create(self, obj: User) -> User:
        """Create a new user with hashed password."""
        if not obj.password:
            raise ValueError("Password must be provided")

        async with self.session.begin():
            password_service = BCryptPasswordService()
            hashed_password = password_service.hash(plain_password=obj.password)
            obj.password = hashed_password

            try:
                create = await super().create(obj=obj)
            except ORMDuplicateException as e:
                raise UserAlreadyExistsError(email=obj.email) from e

            return create

    async def authenticate(
        self,
        email: str,
        password: str,
        password_service: PasswordService = BCryptPasswordService(),
    ) -> User:
        """Authenticate a user by checking their email and password.

        If user is not found or password does not match, raises UserBadCredentials.
        """
        user = await self._repository.by_email(email=email)
        if user is None:
            raise UserBadCredentials()

        if not password_service.verify(
            plain_password=password, hashed_password=user.password
        ):
            raise UserBadCredentials()

        return user

    async def token(self, user: User) -> str:
        """Generate a JWT token for the given user."""
        from src.utils.jwt import JwtAuthenticationService

        jwt_service = JwtAuthenticationService()
        token = jwt_service.encode(user_id=str(user.id))
        return token
