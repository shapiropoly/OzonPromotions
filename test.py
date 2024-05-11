from datetime import date

import asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from models.db_session import global_init, session_db, get_database_url
from models import Promotions, Companies, Users


async def main():
    await global_init()
    await create_user()


@session_db
async def create_company(session: AsyncSession):
    company = Companies(id=524, client_id=453445, api_key="342039489328werfw43294230jdks34230", company_name="Тест")
    await company.save(session=session)


@session_db
async def create_user(session: AsyncSession):
    user = Users(telegram_id=78594589458, username="test_username_3", name="name_3")
    await user.save(session=session)


@session_db
async def create_promo(session: AsyncSession):
    promotion = Promotions(
        id=434328,
        title="Распродажа 24.04",
        date_start=date(year=2024, month=4, day=24),
        date_end=date(year=2024, month=4, day=28),
        freeze_date=date(year=2024, month=4, day=28),
        participating_products_count=10,
        is_participating=True,
        discount_value=0.15)
    await promotion.save(session=session)


if __name__ == "__main__":
    print(get_database_url(alembic=True))
    asyncio.run(main())