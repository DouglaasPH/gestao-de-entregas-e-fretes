import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import db

class Vehicle_type(db.Model):
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    name: Mapped[str] = mapped_column(sa.String, nullable=False, unique=True)

    vehicle: Mapped[list["Vehicle"]] = relationship(back_populates='vehicle_type')

    def __repr__(self) -> str:
        return f"Vehicle_type(id={self.id!r}, name={self.name!r})"