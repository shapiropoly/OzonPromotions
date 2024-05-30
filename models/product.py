from __future__ import annotations
from datetime import datetime
from typing import Self, List, TYPE_CHECKING

from sqlalchemy import select, BIGINT
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.db_session import Base
from .products_to_companies import products_to_companies_association_table

if TYPE_CHECKING:
    from . import Company


class Product(Base):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(BIGINT, autoincrement=True, primary_key=True)
    product_id: Mapped[int]
    name: Mapped[str]
    price: Mapped[int]
    action_price: Mapped[int]
    companies: Mapped[List[Company]] = relationship(
        secondary=products_to_companies_association_table,
        back_populates="products",
        lazy="selectin",
        cascade="all, delete"
    )

    @classmethod
    async def get_items(cls, name: str, session: AsyncSession) -> Self:
        """
        Get object by company_name

        :param name: company_name
        :param session: db session
        :return: Companies object
        """

        _ = await session.execute(select(cls).where(cls.company_name == name))
        return _.scalar()

    async def save(self, session: AsyncSession):
        session.add(self)
        await session.commit()