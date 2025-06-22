import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import db

class Driver(db.Model):
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    cnh: Mapped[str] = mapped_column(sa.String, nullable=False, unique=True)

    driver_status_id: Mapped[int] = mapped_column(sa.ForeignKey('driver_status.id'))
    user_id: Mapped[int] = mapped_column(sa.ForeignKey('user.id'))

    driver_status: Mapped[list["Driver_status"]] = relationship(back_populates='Driver')
    user: Mapped[list["User"]] = relationship(back_populates='Driver')

    def __repr__(self) -> str:
        return f"Driver(id={self.id!r}, user_id={self.user_id!r}, cnh={self.cnh!r})"