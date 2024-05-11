from sqlalchemy import Table, Column, ForeignKey, Integer, UniqueConstraint
from models.db_session import Base


users_to_company_association_table = Table(
    "users_to_company_association",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("users_id", ForeignKey("users.id"), primary_key=True),
    Column("company_id", ForeignKey("companies.id"), primary_key=True),
    UniqueConstraint("users_id", "company_id", name="idx_unique_users_to_company")
)

