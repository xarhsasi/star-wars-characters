import http


class ORMNotFoundException(Exception):
    """Exception raised when a character is not found."""

    def __init__(self, id: int):
        self.detail = f"ORM model with ID {id} not found."
        self.status_code = http.HTTPStatus.NOT_FOUND
        super().__init__(self.detail)
