import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import db

class Points_of_sale(db.Model):
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    cnpj: Mapped[str] = mapped_column(sa.String, nullable=False, unique=True)
    telephone: Mapped[str] = mapped_column(sa.String, nullable=False)
    address: Mapped[str] = mapped_column(sa.String, nullable=False)

    def __repr__(self) -> str:
        return f"Points_of_sale(id={self.id!r}, cnpj={self.cnpj!r}, telephone={self.telephone!r}, address={self.address!r})"