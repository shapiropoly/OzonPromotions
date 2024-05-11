from sqlalchemy import Table, Column, ForeignKey, Integer, UniqueConstraint
from models.db_session import Base


companies_to_promotions_association_table = Table(
    "companies_to_promotions_association",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("company_id", ForeignKey("companies.id"), primary_key=True),
    Column("promotions_id", ForeignKey("promotions.id"), primary_key=True),
    UniqueConstraint("company_id", "promotions_id", name="idx_unique_companies_to_promotions")
)

