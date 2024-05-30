from __future__ import annotations
from typing import Self, TYPE_CHECKING, List
from sqlalchemy import select, BIGINT
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.db_session import Base
from .users_to_company import users_to_companies_association_table

if TYPE_CHECKING:
    from . import Company


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(BIGINT, autoincrement=True, primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BIGINT, unique=True)
    username: Mapped[str]
    name: Mapped[str]
    companies: Mapped[List[Company]] = relationship(
        secondary=users_to_companies_association_table,
        back_populates="users",
        lazy="selectin",
        cascade="all, delete"
    )

    @classmethod
    async def get_user(cls, telegram_id: int, session: AsyncSession) -> Self:
        _= await session.execute(select(cls).where(cls.telegram_id == telegram_id))
        return _.scalar()

    async def save(self, session: AsyncSession):
        session.add(self)
        await session.commit()