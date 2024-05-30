from datetime import date

import sqlalchemy as db
import psycopg2
from sqlalchemy.sql import select

from models.products_to_companies import companies_to_promo_association_table

URL_DATABASE = "postgresql://localhost:5432/postgres"

engine = db.create_engine(URL_DATABASE)

conn = engine.connect()

metadata = db.MetaData()

users = db.Table('users', metadata,
                 db.Column('username', db.String, primary_key=True),
                 db.Column('name', db.String),
                 db.Column('surname', db.String),
                 db.Column('api_key', db.String),
                 db.Column('client_id', db.String)
                 )


products_in_promo = db.Table('products_in_promo', metadata,
                 db.Column('promo_id', db.Integer, primary_key=True),
                 db.Column('title', db.String),
                 db.Column('date_start', db.DateTime),
                 db.Column('date_end', db.DateTime),
                 db.Column('freeze_date', db.DateTime),
                 db.Column('participating_products_count', db.Integer),
                 db.Column('is_participating', db.Boolean, default=True),
                 db.Column('discount_value', db.Double)
                 )


items = db.Table('items', metadata,
                 db.Column('products_id', db.Integer, primary_key=True),
                 db.Column('name', db.String),
                 db.Column('specification', db.String),
                 db.Column('price_before_promo', db.Double),
                 db.Column('price_after_promo', db.Double),
                 db.Column('count_products', db.Integer),
                 db.Column('date_start', db.DateTime),
                 db.Column('date_end', db.DateTime),
                 db.Column('categories', db.String),
                 db.Column('check_active_promo', db.Boolean, default=False)
                 )

metadata.create_all(engine)

insertion_query = users.insert().values([
    {'username': 'a_chekmarew', 'name': 'Андрей', 'surname': 'Чекмарев', 'api_key': '12224zfjsdlfj9334203xhd', 'client_id': '12224awe4'},
    {'username': 'ivanov_p', 'name': 'Петр', 'surname': 'Иванов', 'api_key': '2493240234dsfhksdfhks92', 'client_id': '3423dfs3'}
])

insertion_query_2 = products_in_promo.insert().values([
    {'promo_id': 34287, 'title': 'Распродажа 17.04', 'date_start': date(2024, 4, 17), 'date_end': date(2024, 4, 21), 'participating_products_count': 3, 'is_participating': False, 'discount_value': 0.15}
])

insertion_query_3 = items.insert().values([
    {'products_id': 34287, 'name': 'Футболка', 'specification': 'Черная, M', 'price_before_promo': 1990, 'price_after_promo': 1790, 'count_products' : 5, 'date_start': date(2024, 4, 17), 'date_end': date(2024, 4, 21), 'categories': 'Женская одежда', 'check_active_promo' : False}
])

conn.execute(insertion_query_3)
select_all_query = db.select(companies_to_promo_association_table)
select_all_results = conn.execute(select_all_query)

print(select_all_results.fetchall())
