from __future__ import print_function

import asyncio

import aiohttp


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

    async def checking_connection(self):
        endpoint = '/v1/actions'
        url = self.base_url + endpoint

        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.get(url) as response:
                if response.status == 200:
                    return 200
                else:
                    return 400

    async def promos(self):
        endpoint = '/v1/actions'
        url = self.base_url + endpoint

        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.get(url) as response:
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
            "action_id": action_id
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

    async def promos_products(self, action_id, action_title):
        endpoint = '/v1/actions/products'
        url = self.base_url + endpoint
        payload = {
            "action_id": action_id
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
        for product in all_products["result"]["products"]:
            product["action_id"] = action_id
            product["action_title"] = action_title
        return all_products

    async def all_promos_products(self, promos):
        all_products = []
        for action_id, action_title in promos.items():
            all_products.extend((await self.promos_products(action_id, action_title))['result']['products'])
        return all_products

    async def product_name(self, product_id):
        endpoint = '/v2/product/info'
        url = self.base_url + endpoint
        payload = {
            "product_id": product_id
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
                    return
                else:
                    print(f"Error: {response.status}")
                    try:
                        error_response = await response.json()
                        print(error_response)
                    except aiohttp.ContentTypeError:
                        print("Response is not JSON")
                    return None

    async def connection(self):
        promos = await self.promos()
        promos_dict = {}
        for promo in promos['result']:
            promos_dict[promo['id']] = promo['title']

        products = await self.all_promos_products(promos_dict)
        return products
