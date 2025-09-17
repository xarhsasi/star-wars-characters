import http


class CharacterNotFoundException(Exception):
    """Exception raised when a character is not found."""

    def __init__(self, id: int):
        self.detail = f"Character with ID {id} not found."
        self.status_code = http.HTTPStatus.NOT_FOUND
        super().__init__(self.detail)
