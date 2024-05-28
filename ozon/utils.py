from __future__ import print_function
import aiohttp
import asyncio


class Utils:
    def __init__(self, api_key, client_id):
        self.api_key = api_key
        self.client_id = client_id
        self.base_url = 'https://api-seller.ozon.ru'
        self.headers = {
            'Client-Id': self.client_id,
            'Api-Key': self.api_key,
            'Content-Type': 'application/json'
        }

    async def promos(self):
        endpoint = '/v1/actions'
        url = self.base_url + endpoint
        payload = {
            "dir": "ASC",
            "filter": {
                "since": "2024-01-01T00:00:00Z",
                "to": "2024-12-31T23:59:59Z"
            },
            "limit": 10,
            "offset": 0,
            "with": {
                "analytics_data": True,
                "financial_data": True
            }
        }

        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.get(url, json=payload) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    print(f"Error: {response.status}")
                    try:
                        error_response = await response.json()
                        print(error_response)
                    except aiohttp.ContentTypeError:
                        print("Response is not JSON")
                    return None

    async def promos_candidates(self, action_id):
        endpoint = '/v1/actions/candidates'
        url = self.base_url + endpoint
        payload = {
            "action_id": action_id,
            "limit": 10,
            "offset": 0
        }

        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.post(url, json=payload) as response:
                if response.status == 200:
                    all_candidates = await response.json()
                else:
                    print(f"Error: {response.status}")
                    try:
                        error_response = await response.json()
                        print(error_response)
                    except aiohttp.ContentTypeError:
                        print("Response is not JSON")
                    return None

        return all_candidates

    async def promos_products(self, action_id):
        endpoint = '/v1/actions/products'
        url = self.base_url + endpoint
        payload = {
            "action_id": action_id,
            "limit": 10,
            "offset": 0
        }

        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.post(url, json=payload) as response:
                if response.status == 200:
                    all_products = await response.json()
                else:
                    print(f"Error: {response.status}")
                    try:
                        error_response = await response.json()
                        print(error_response)
                    except aiohttp.ContentTypeError:
                        print("Response is not JSON")
                    return None

        return all_products

    async def promos_products_activate(self, action_id, products):
        endpoint = '/v1/actions/products/activate'
        url = self.base_url + endpoint
        payload = {
            "action_id": action_id,
            "products": products
        }

        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.post(url, json=payload) as response:
                if response.status == 200:
                    result = await response.json()
                else:
                    print(f"Error: {response.status}")
                    try:
                        error_response = await response.json()
                        print(error_response)
                    except aiohttp.ContentTypeError:
                        print("Response is not JSON")
                    return None

        return result

    async def promos_products_deactivate(self, action_id, products_ids):
        endpoint = '/v1/actions/products/deactivate'
        url = self.base_url + endpoint
        payload = {
            "action_id": action_id,
            "product_ids": products_ids
        }

        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.post(url, json=payload) as response:
                if response.status == 200:
                    result = await response.json()
                else:
                    print(f"Error: {response.status}")
                    try:
                        error_response = await response.json()
                        print(error_response)
                    except aiohttp.ContentTypeError:
                        print("Response is not JSON")
                    return None

        return result

    async def connection(self):
        promos = await self.promos()
        if promos:
            print("Акции:")
            print(promos)

        action_id = '1177179'  # Укажите здесь нужный action_id
        candidates = await self.promos_candidates(action_id)
        if candidates:
            print("Кандидаты:")
            print(candidates)

        products = await self.promos_products(action_id)
        if products:
            print("Товары в акциях:")
            print(products)


def main():
    util = Utils('4dcff177-2194-4062-a662-b914c37417f7', '74392')
    asyncio.run(util.connection())


if __name__ == "__main__":
    main()
