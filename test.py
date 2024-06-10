from datetime import date

import asyncio

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from models.db_session import global_init, session_db, create_session, get_database_url
from models import Promotion, Company, User, Product
from ozon.utils import Utils
from utils.checking import checking_user_api_key, checking_user_client_id
from utils.product_message import product_message


async def main():
    await global_init()
    async with create_session() as session:
        user = await User.get_user(telegram_id=479546019, session=session)
        company = await Company.get_by_client_id(client_id=74392, session=session)
        # company = user.companies


        # products = company.products
        # print(products)
        #
        # await Product.clear_products_table(session=session)

        products2 = company.products

        print(products2)





        # util = Utils(await checking_user_api_key(user, company),
        #              await checking_user_client_id(user, company))
        # # Получение и сохранение продуктов
        # products = await util.connection()
        #
        # new_products = []




        # for company in user.companies:
        #     db_products = company.products
        #     for db_product in db_products:
        #         print("db_product: ", db_product.product_id, "action_price: ", db_product.action_price)

        # for product in products:
        #     check_product = await Product.get_product(product_id=product['id'], action_price=product['action_price'], session=session)
        #
        #     if not check_product:
        #         # print("Такого продукта нету! ", product)
        #         new_products.append(product)
        #
        #     # print("Product in Utils:", product['id'], "action_price:", product['action_price'])
        #     conditions = []
        #
        # for p in new_products:
        #     p['name'] = (await util.product_name(p['id']))['result']['name']
        #
        # print(new_products)
        #
        # for db_p in new_products:
        #     print(product_message(db_p))


                # for db_product in db_products:
                #
                #     print("DB Product:", db_product.product_id)
                #     condition = and_(
                #         product['id'] != db_product.product_id,
                #         product['action_price'] != db_product.action_price
                #     )
                #     conditions.append(condition)
                #
                # if not conditions:
                #     continue
                #
                # combined_conditions = and_(*conditions)
                # query = select(Product).filter(combined_conditions)
                # result = await session.execute(query)
                # matched_products = result.scalars().all()
                #
                # for product in matched_products:
                #     product_name_result = await util.product_name(product.id)
                #     product.name = product_name_result['result']['name']
                #     new_products.append(product)



# client_id = company.client_id
# api_key = company.api_key
# print(f"Client ID: {client_id}, API Key: {api_key}")
#
# user = await Company.users()
# await company.save(session=session)


# company1 = Company.get_by_id(client_id=74392)
# company3 = Company(client_id=123, api_key="3323982dhjf", company_name="name")
#
# product = Product(product_id=5454, name="name_1", price=1500, action_price=1000)
#
# company3.products.append(product)
#
#
#
# await company3.save(session=session)
# # await user1.save(session=session)
# await product.save(session=session)
# # await session.commit()




# user = await User.get_user(telegram_id=5454, session=session)
# company1 = Company(client_id=11, api_key="1_1", company_name="Company_1_1")
# company2 = Company(client_id=22, api_key="2_2", company_name="Company_1_1")
#
# # Добавление компаний к пользователю
# user.companies.append(company1)
# user.companies.append(company2)
#
# await user.save(session=session)
# await session.commit()

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
#     await global_init()
#     await create_user()
#     # await add_user_with_company()


@session_db
async def create_company(session: AsyncSession):
    company = Company(id=524, client_id=453445, api_key="342039489328werfw43294230jdks34230", company_name="Тест")
    await company.save(session=session)


@session_db
async def create_user(session: AsyncSession):
    user1 = User(telegram_id=23233, username="username", name="name")
    await user1.save(session=session)


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

