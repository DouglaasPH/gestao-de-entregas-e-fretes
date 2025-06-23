import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import db

class Vehicle(db.Model):
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    plate_encrypted: Mapped[str] = mapped_column(sa.String, nullable=False, unique=True)
    model: Mapped[str] = mapped_column(sa.String, nullable=False)
    capacity: Mapped[str] = mapped_column(sa.String, nullable=False)


    vehicle_type_id: Mapped[int] = mapped_column(sa.ForeignKey('vehicle_type.id'))
    driver_id: Mapped[int] = mapped_column(sa.ForeignKey('driver.id'))

    vehicle_type: Mapped["Vehicle_type"] = relationship(back_populates='vehicle')
    driver: Mapped["Driver"] = relationship(back_populates='vehicle')
    orders: Mapped["Orders"] = relationship(back_populates='vehicle')

    def __repr__(self) -> str:
        return f"Vehicle(id={self.id!r}, plate={self.plate_encrypted!r}, model={self.model!r}, vehicle_type_id={self.vehicle_type_id!r}, capacity={self.capacity!r}, driver_id={self.driver_id!r})"