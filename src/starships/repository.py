from src.repository import Repository
from src.starships.models import Starship


class StarshipRepository(Repository[Starship]):
    """Starship repository."""

    _model = Starship
    SEARCH_QUERY_ATTR = "name"
