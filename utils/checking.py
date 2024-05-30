async def checking_user_company(user, company):
    """
    Gets user and company objects
    :param User: telegram_id
    :param Company: id
    :return: A tuple containing the client ID and API key of the company
    """
    if company in user.companies:
        return company.client_id, company.api_key


async def checking_user_client_id(user, company):
    """
    Gets user and company objects
    :param User: telegram_id
    :param Company: id
    :return: A tuple containing the client ID and API key of the company
    """
    if company in user.companies:
        return str(company.client_id)


async def checking_user_api_key(user, company):
    """
    Gets user and company objects
    :param User: telegram_id
    :param Company: id
    :return: A tuple containing the client ID and API key of the company
    """
    if company in user.companies:
        return str(company.api_key)
