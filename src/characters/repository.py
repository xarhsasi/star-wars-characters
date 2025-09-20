from src.characters.models import Character
from src.repository import Repository


class CharacterRepository(Repository[Character]):
    """Character repository."""

    _model = Character
    SEARCH_QUERY_ATTR = "name"
