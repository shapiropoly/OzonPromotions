from __future__ import annotations
from typing import List, Self, TYPE_CHECKING
from sqlalchemy import select, BIGINT
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.db_session import Base
from .users_to_company import users_to_companies_association_table
from .companies_to_promotions import companies_to_promotions_association_table

if TYPE_CHECKING:
    from .promotion import Promotion
    from .user import User


class Company(Base):
    __tablename__ = 'companies'

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    client_id: Mapped[int]
    api_key: Mapped[str]
    company_name: Mapped[str]
    promotions: Mapped[List[Promotion]] = relationship(
        secondary=companies_to_promotions_association_table,
        back_populates="companies"
    )
    users: Mapped[List[User]] = relationship(
        secondary=users_to_companies_association_table,
        back_populates="companies",
        lazy="selectin",
        cascade="all, delete"
    )

    @classmethod
    async def get_by_id(cls, id: int, session: AsyncSession) -> Self:
        _ = await session.execute(select(cls).where(cls.id == id))
        return _.scalar()

    async def save(self, session: AsyncSession):
        session.add(self)
        await session.commit()