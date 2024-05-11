from typing import Self

from sqlalchemy import select, BIGINT
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column

from models.db_session import Base


class OperationName(Base):
    __tablename__ = 'operation_names'

    id: Mapped[int] = mapped_column(BIGINT, autoincrement=True, primary_key=True)
    supplier_oper_name: Mapped[str]
    add_to_other_payments: Mapped[bool]

    @classmethod
    async def get_option_by_oper_name(cls, oper_name: str, session: AsyncSession) -> Self:
        """
        Get object by supplier_oper_name

        :param oper_name: supplier_oper_name
        :param session: db session
        :return: OperationName object
        """

        _ = await session.execute(select(cls).where(cls.supplier_oper_name == oper_name))
        return _.scalar()

    async def save(self, session: AsyncSession):
        # oper = OperationName(supplier_oper_name="helloworld", add_to_other_payments=False)
        # await oper.save(session)
        session.add(self)
        await session.commit()
