import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import db

class Orders_status(db.Model):
    __tablename__ = 'orders_status'
    
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    name: Mapped[str] = mapped_column(sa.String, nullable=False, unique=True)

    orders: Mapped[list["Orders"]] = relationship(back_populates='orders_status')

    def __repr__(self) -> str:
        return f"Orders_status(id={self.id!r}, name={self.name!r})"