from __future__ import annotations
from typing import List, Self, TYPE_CHECKING
from sqlalchemy import select, BIGINT
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.db_session import Base
from .users_to_company import users_to_companies_association_table
from .products_to_companies import products_to_companies_association_table

if TYPE_CHECKING:
    from .product import Product
    from .user import User


class Company(Base):
    __tablename__ = 'companies'

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    client_id: Mapped[int]
    api_key: Mapped[str]
    company_name: Mapped[str]
    products: Mapped[List[Product]] = relationship(
        secondary=products_to_companies_association_table,
        back_populates="companies",
        lazy="selectin",
        cascade="all, delete"
    )
    users: Mapped[List[User]] = relationship(
        secondary=users_to_companies_association_table,
        back_populates="companies",
        lazy="selectin",
        cascade="all, delete"
    )

    @classmethod
    async def get_by_client_id(cls, client_id: int, session: AsyncSession) -> Self:
        _ = await session.execute(select(cls).where(cls.client_id == client_id))
        return _.scalar()

    @classmethod
    async def get_by_id(cls, id: int, session: AsyncSession) -> Self:
        _ = await session.execute(select(cls).where(cls.id == id))
        return _.scalar()

    async def save(self, session: AsyncSession):
        session.add(self)
        await session.commit()
