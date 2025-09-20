import http


class ORMNotFoundException(Exception):
    """Exception raised when a character is not found."""

    def __init__(self, id: int):
        self.detail = f"ORM model with ID {id} not found."
        self.status_code = http.HTTPStatus.NOT_FOUND
        super().__init__(self.detail)


class ORMDuplicateException(Exception):
    """Exception raised when a duplicate entry is attempted."""

    def __init__(self):
        self.detail = "Duplicate ORM object."
        self.status_code = http.HTTPStatus.CONFLICT
        super().__init__(self.detail)


class ServicePermissionDenied(Exception):
    """Exception raised when a user does not have permission to perform an action."""

    def __init__(self, detail: str = "Permission denied."):
        self.detail = detail
        self.status_code = http.HTTPStatus.FORBIDDEN
        super().__init__(self.detail)
