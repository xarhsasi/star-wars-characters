from sqlalchemy import Sequence, select

from src.films.models import Film
from src.repository import Repository


class FilmRepository(Repository[Film]):
    """Character repository."""

    _model = Film

    SEARCH_QUERY_ATTR = "title"
