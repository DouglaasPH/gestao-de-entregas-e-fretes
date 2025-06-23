import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import db

class Points_of_sale(db.Model):
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    cnpj_encrypted: Mapped[str] = mapped_column(sa.String, nullable=False, unique=True)
    telephone_encrypted: Mapped[str] = mapped_column(sa.String, nullable=False)
    address_encrypted: Mapped[str] = mapped_column(sa.String, nullable=False)

    orders: Mapped["Orders"] = relationship(back_populates='points_of_sale')

    def __repr__(self) -> str:
        return f"Points_of_sale(id={self.id!r}, cnpj={self.cnpj_encrypted!r}, telephone={self.telephone_encrypted!r}, address={self.address_encrypted!r})"