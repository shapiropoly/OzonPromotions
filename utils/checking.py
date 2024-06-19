import asyncio

from ozon.utils import Utils


async def checking_user_company(user, company):
    """
    Gets user and company objects
    :param User: telegram_id
    :param Company: id
    :return: A tuple containing the client ID and API key of the company
    """
    if company in user.companies:
        return company.client_id, company.api_key


async def check_connection(client_id, api_key):
    utils = Utils(api_key, client_id)
    return await utils.checking_connection()


# async def main():
#     result = await checking_connection('62-b914c37417f7', '74392')
#     print(result)
#
# if __name__ == "__main__":
#     asyncio.run(main())


async def checking_user_client_id(user, company):
    """
    Gets user and company objects
    :param User: telegram_id
    :param Company: id
    :return: A tuple containing the client ID of the company
    """
    if company in user.companies:
        return str(company.client_id)


async def checking_user_api_key(user, company):
    """
    Gets user and company objects
    :param User: telegram_id
    :param Company: id
    :return: A tuple containing the API key of the company
    """
    if company in user.companies:
        return str(company.api_key)
