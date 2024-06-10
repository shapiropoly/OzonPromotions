from __future__ import annotations
from datetime import datetime
from typing import Self, List, TYPE_CHECKING

from sqlalchemy import select, BIGINT, Integer, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.db_session import Base
from .products_to_companies import products_to_companies_association_table

if TYPE_CHECKING:
    from . import Company


class Product(Base):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(BIGINT, autoincrement=True, primary_key=True)
    product_id: Mapped[int] = mapped_column(Integer, nullable=False)
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
    async def get_product(cls, product_id: int, action_price: int, session: AsyncSession) -> 'Self':
        """
        Get object by product

        :param product_id: id
        :param action_price: price
        :param session: db session
        :return: Companies object
        """

        result = await session.execute(
            select(cls).where(cls.product_id == product_id, cls.action_price == action_price)
        )
        return result.scalar()

    async def save(self, session: AsyncSession):
        session.add(self)
        await session.commit()

    @classmethod
    async def clear_products_table(cls, session: AsyncSession) -> None:
        """
        Очистить таблицу products данные из таблицы связей.

        :param session: сессия базы данных
        """

        await session.execute(delete(products_to_companies_association_table))
        await session.execute(delete(cls))
        await session.commit()