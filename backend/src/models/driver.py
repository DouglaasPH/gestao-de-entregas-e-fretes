import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import db

class Driver(db.Model):
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    cnh_encrypted: Mapped[str] = mapped_column(sa.String, nullable=False, unique=True)

    driver_status_id: Mapped[int] = mapped_column(sa.ForeignKey('driver_status.id'))
    user_id: Mapped[int] = mapped_column(sa.ForeignKey('user.id'))

    driver_status: Mapped["Driver_status"] = relationship(back_populates='driver')
    user: Mapped["User"] = relationship(back_populates='driver')
    vehicle: Mapped["Vehicle"] = relationship(back_populates='driver')
    orders: Mapped["Orders"] = relationship(back_populates='driver')

    def __repr__(self) -> str:
        return f"Driver(id={self.id!r}, user_id={self.user_id!r}, cnh={self.cnh_encrypted!r})"