from datetime import date

import asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from models.db_session import global_init, session_db, create_session
from models import Promotion, Company, User


async def main():
    await global_init()
    async with create_session() as session:
        user = await User.get_user(telegram_id=5454, session=session)
        company1 = Company(client_id=11, api_key="1_1", company_name="Company_1_1")
        company2 = Company(client_id=22, api_key="2_2", company_name="Company_1_1")

        # Добавление компаний к пользователю
        user.companies.append(company1)
        user.companies.append(company2)

        await user.save(session=session)
        await session.commit()

    # # oper = OperationName(supplier_oper_name="hello", add_to_other_payments=False)
        # user1 = User(telegram_id=111, username="username_1", name="name_1")
        # user2 = User(telegram_id=222, username="username_2", name="name_2")
        # cmpny1 = Company(client_id=123, api_key="342", company_name="company_1")
        # cmpny2 = Company(client_id=234, api_key="765", company_name="company_2")
        #
        # user1.companies = [cmpny1, cmpny2]
        # user2.companies = [cmpny2]
        #
        # await user1.save(session=session)
        # await user2.save(session=session)
        # await cmpny1.save(session=session)
        # await cmpny2.save(session=session)
    # await create_operation_name()
    # await create_company()




# async def main():
#
#     await global_init()
#     # await create_user()
#     await add_user_with_company()


@session_db
async def create_company(session: AsyncSession):
    company = Company(id=524, client_id=453445, api_key="342039489328werfw43294230jdks34230", company_name="Тест")
    await company.save(session=session)


@session_db
async def create_user(session: AsyncSession):
    user = User(telegram_id=122322, username="test_username_6", name="name_6")
    await user.save(session=session)


@session_db
async def create_promo(session: AsyncSession):
    promotion = Promotion(
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
    # print(get_database_url(alembic=False))
    asyncio.run(main())

