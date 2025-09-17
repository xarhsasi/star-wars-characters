from __future__ import annotations

from typing import Generic, Sequence, Type, TypeVar

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

_T = TypeVar("_T")  # ORM model type


class ORMGetService:
    def __init__(self, model):
        self.model = model
