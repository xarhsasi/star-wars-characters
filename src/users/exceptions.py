"""User specific exceptions."""


class UserException(BaseException):
    """Base exception for user related errors."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class UserNotFoundError(UserException):
    """Exception raised when a user is not found."""

    def __init__(self, identifier: int | str):
        self.message = f"User {identifier} not found."
        super().__init__(self.message)


class UserBadCredentials(UserException):
    """Exception raised when a user is not found."""

    def __init__(self):
        self.message = "Bad Credentials"
        super().__init__(self.message)


class UserAlreadyExistsError(UserException):
    """Exception raised when a user already exists."""

    def __init__(self, email: str):
        self.message = f"User with email {email} already exists."
        super().__init__(self.message)
