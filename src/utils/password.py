import abc

from passlib.context import CryptContext


class PasswordService(abc.ABC):
    """The generic password service interface."""

    @abc.abstractmethod
    def hash(self, plain_password: str) -> str:
        """Hash a password and return the hashed version."""

    @abc.abstractmethod
    def verify(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password against a hashed password."""


class BCryptPasswordService(PasswordService):
    """A password service that uses the bcrypt hashing algorithm."""

    def __init__(self) -> None:
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash(self, plain_password: str) -> str:
        """Given a plain password, return the hashed version using bcrypt."""
        hashed_password = self.pwd_context.hash(plain_password)
        # Mypy complains that the return type is Any.
        if not isinstance(hashed_password, str):
            raise ValueError("Hashed password is not a string.")
        return hashed_password

    def verify(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a plain password against a hashed password using bcrypt."""
        verified_password = self.pwd_context.verify(
            plain_password, hashed_password
        )
        # Mypy complains that the return type is Any.
        if not isinstance(hashed_password, str):
            raise ValueError("Hashed password is not a string.")
        return verified_password
