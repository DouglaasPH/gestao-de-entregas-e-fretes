import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import db

class Load_type(db.Model):
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    name: Mapped[str] = mapped_column(sa.String, nullable=False, unique=True)

    orders: Mapped[list["Orders"]] = relationship(back_populates='load_type')

    def __repr__(self) -> str:
        return f"Load_type(id={self.id!r}, name={self.name!r})"