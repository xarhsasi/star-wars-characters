"""Main function for running the API service."""

# mypy: ignore-errors
from src.application import create_application

app = create_application()
