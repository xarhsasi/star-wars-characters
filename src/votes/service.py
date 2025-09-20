import logging

import sqlalchemy
import sqlalchemy.exc
from sqlalchemy.ext.asyncio import AsyncSession

from src.exceptions import (
    ORMDuplicateException,
    ORMNotFoundException,
    ServicePermissionDenied,
)
from src.films.models import Film
from src.films.repository import FilmRepository
from src.service import (
    CreateORMService,
    GetORMService,
    ListPaginationORMService,
    ORMBaseService,
    UpdateORMService,
)
from src.users.models import User
from src.users.repository import UserRepository
from src.votes.model import Vote
from src.votes.repository import VoteRepository

logger = logging.getLogger(__name__)


class VoteService(
    CreateORMService[Vote],
    GetORMService[Vote],
    UpdateORMService[Vote],
    ListPaginationORMService[Vote],
):
    """Film service."""

    def __init__(self, session: AsyncSession):
        self.session = session
        self._repository = VoteRepository(session)
        self._film_repository = FilmRepository(session)
        self._user_repository = UserRepository(session)
        super().__init__(repository=self._repository)

    async def vote(
        self, vote_id: int, user_id: int, score: int, feedback: str | None = None
    ) -> Vote:
        """Create or update a vote for a film."""
        async with self.session.begin():
            vote = await self.get(vote_id)
            if vote.user_id != user_id:
                raise ServicePermissionDenied(detail="Action not allowed.")

            if vote is None:
                v = Vote(
                    user_id=user_id, film_id=vote_id, value=score, feedback=feedback
                )
                updated_vote = await self.create(obj=v)
            else:
                updated_vote = await self.update(
                    id=vote.id, attrs={"value": score, "feedback": feedback}
                )
            return updated_vote
