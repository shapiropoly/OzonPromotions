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


from .company import Company


class Product(Base):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(BIGINT, autoincrement=True, primary_key=True)
    product_id: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str]
    price: Mapped[int]
    action_price: Mapped[int]
    action_id: Mapped[int]
    companies: Mapped[List[Company]] = relationship(
        secondary=products_to_companies_association_table,
        back_populates="products",
        lazy="selectin",
        cascade="all, delete"
    )

    @classmethod
    async def get_product(cls, product_id: int, action_id: int, session: AsyncSession) -> 'Self':
        """
        Get object by product

        :param product_id: product id
        :param action_id: action id
        :param session: db session
        :return: Companies object
        """

        result = await session.execute(
            select(cls).where(cls.product_id == product_id, cls.action_id == action_id)
        )
        return result.scalar()

    async def save(self, session: AsyncSession):
        session.add(self)
        await session.commit()

    @classmethod
    async def delete_product(cls, product_id: int, action_id: int, session: AsyncSession) -> None:
        """
        Удалить товар по product_id и action_id

        :param product_id: product id
        :param action_id: action id
        :param session: сессия базы данных
        """

        product = await Product.get_product(product_id, action_id, session)

        if product:
            await session.execute(
                delete(products_to_companies_association_table).where(
                    products_to_companies_association_table.c.product_id == product.id
                )
            )
            await session.execute(
                delete(cls).where(cls.id == product.id)
            )
            await session.commit()

    @classmethod
    async def clear_products_table(cls, client_id: int, session: AsyncSession) -> None:
        """
        Очистить данные таблицы products связанные с компанией по client_id.

        :param client_id: client_id компании
        :param session: сессия базы данных
        """

        company = await Company.get_by_client_id(client_id, session)

        if company:
            product_ids = [product.id for product in company.products]

            await session.execute(delete(products_to_companies_association_table).where(
                products_to_companies_association_table.c.product_id.in_(product_ids)
            ))

            await session.execute(delete(cls).where(cls.id.in_(product_ids)))
            await session.commit()