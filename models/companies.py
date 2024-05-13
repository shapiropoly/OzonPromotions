from __future__ import annotations

from typing import List
from sqlalchemy import select, BIGINT
from typing import TYPE_CHECKING
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.db_session import Base
from .companies_to_promotions import companies_to_promotions_association_table
from .users_to_company import users_to_company_association_table

if TYPE_CHECKING:
    from .promotions import Promotions
    from .users import Users


class Companies(Base):
    __tablename__ = 'companies'

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    client_id: Mapped[int]
    api_key: Mapped[str]
    company_name: Mapped[str]
    promotions: Mapped[List[Promotions]] = relationship(
        secondary=companies_to_promotions_association_table,
        back_populates="companies")
    users: Mapped[List[Users]] = relationship(
        secondary=users_to_company_association_table,
        back_populates="companies")

    @classmethod
    async def get_by_name(cls, name: str, session: AsyncSession) -> List["Companies"]:
        """
        Get object by company_name

        :param name: company_name
        :param session: db session
        :return: List of Companies objects
        """
        _ = await session.execute(select(cls).where(cls.company_name == name))
        return _.scalar()

    async def save(self, session: AsyncSession):
        session.add(self)
        await session.commit()