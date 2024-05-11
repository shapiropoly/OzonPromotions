from sqlalchemy import Table, Column, ForeignKey, Integer, UniqueConstraint
from models.db_session import Base


products_to_promotions_association_table = Table(
    "products_to_promotions_association",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("products_id", ForeignKey("products.id"), primary_key=True),
    Column("promotions_id", ForeignKey("promotions.id"), primary_key=True),
    UniqueConstraint("products_id", "promotions_id", name="idx_unique_products_to_promotions")
)
