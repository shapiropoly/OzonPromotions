from sqlalchemy import Table, Column, ForeignKey, Integer, UniqueConstraint, BIGINT
from models.db_session import Base

users_to_companies_association_table = Table(
    "users_to_companies_association_table",
    Base.metadata,
    Column("id", BIGINT, primary_key=True, autoincrement=True),  # Новый столбец с автоинкрементом
    Column("user_id", ForeignKey("users.id"), nullable=False),
    Column("company_id", ForeignKey("companies.id"), nullable=False),
    UniqueConstraint("user_id", "company_id", name="uix_user_company")  # Уникальный индекс
)