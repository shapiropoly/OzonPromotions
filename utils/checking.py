from models import Company
from ozon.utils import Utils


async def check_connection(client_id, api_key):
    utils = Utils(api_key, client_id)
    return await utils.checking_connection()


# Проверка на одинаковый client_id и api_key в БД
async def check_double(client_id, api_key, session):
    company = await Company.get_by_client_id(client_id, session)
    if company:
        current_api_key = company.api_key

        if current_api_key == api_key:
            return True