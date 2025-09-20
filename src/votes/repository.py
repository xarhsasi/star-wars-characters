from src.repository import Repository
from src.votes.model import Vote


class VoteRepository(Repository[Vote]):
    """Character repository."""

    _model = Vote

    SEARCH_QUERY_ATTR = "feedback"
