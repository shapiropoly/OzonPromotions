from __future__ import annotations
from typing import Self, TYPE_CHECKING, List

from sqlalchemy import select, BIGINT
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .users_to_company import users_to_company_association_table

from models.db_session import Base

if TYPE_CHECKING:
    from . import Companies


class Users(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(BIGINT, autoincrement=True, primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BIGINT, unique=True)
    username: Mapped[str]
    name: Mapped[str]
    companies: Mapped[List[Companies]] = relationship(
        secondary=users_to_company_association_table,
        back_populates="users")

    @classmethod
    async def get_users(cls, name: str, session: AsyncSession) -> Self:
        """
        Get object by company_name

        :param name: company_name
        :param session: db session
        :return: Companies object
        """

        _ = await session.execute(select(cls).where(cls.company_name == name))
        return _.scalar()

    async def save(self, session: AsyncSession):
        # oper = OperationName(supplier_oper_name="helloworld", add_to_other_payments=False)
        # await oper.save(session)
        session.add(self)
        await session.commit()
