from __future__ import annotations

from datetime import datetime
from typing import Self, TYPE_CHECKING, List

from sqlalchemy import select, BIGINT, Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.db_session import Base
from .companies_to_promotions import companies_to_promotions_association_table
from .products_to_promotions import products_to_promotions_association_table

if TYPE_CHECKING:
    from .company import Company
    from .products import Products


class Promotion(Base):
    __tablename__ = 'promotions'

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    title: Mapped[str]
    date_start: Mapped[datetime]
    date_end: Mapped[datetime]
    freeze_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    participating_products_count: Mapped[int]
    is_participating: Mapped[bool]
    discount_value: Mapped[float]
    companies: Mapped[List[Company]] = relationship(
        secondary=companies_to_promotions_association_table,
        back_populates="promotions")
    products: Mapped[List[Products]] = relationship(
        secondary=products_to_promotions_association_table,
        back_populates="promotions")

    @classmethod
    async def get_by_title(cls, name: str, session: AsyncSession) -> Self:
        """
        Get object by promo title

        :param name:
        :param title: promo title
        :param session: db session
        :return: List of Promos objects
        """
        _ = await session.execute(select(cls).where(cls.title == name))
        return _.scalar()

    async def save(self, session: AsyncSession):
        session.add(self)
        await session.commit()
