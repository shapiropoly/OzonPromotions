from sqlalchemy import Table, Column, ForeignKey, UniqueConstraint, BIGINT

from models.db_session import Base

products_to_companies_association_table = Table(
    "products_to_companies_association_table",
    Base.metadata,
    Column("id", BIGINT, primary_key=True, autoincrement=True),
    Column("product_id", ForeignKey("products.id"), nullable=False),
    Column("company_id", ForeignKey("companies.id"), nullable=False),
    UniqueConstraint("product_id", "company_id", name="uix_product_company")
)
