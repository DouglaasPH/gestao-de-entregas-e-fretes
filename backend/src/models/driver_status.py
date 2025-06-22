import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import db

class Driver_status(db.Model):
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    name: Mapped[str] = mapped_column(sa.String, nullable=False, unique=True)

    driver: Mapped[list["Driver"]] = relationship(back_populates='driver_status')

    def __repr__(self) -> str:
        return f"Driver_status(id={self.id!r}, name={self.name!r})"