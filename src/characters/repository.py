from sqlalchemy import Sequence, select

from src.characters.models import Character
from src.repository import Repository


class CharacterRepository(Repository[Character]):
    """Character repository."""

    _model = Character

    async def search(self, query: str) -> Sequence[Character]:
        """Search rows of the model by name. Default limit is 100."""
        stmt = (
            select(self._model)
            .where(self._model.name.ilike(f"%{query}%"))
            .order_by(self._model.id)
            .limit(50)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()
