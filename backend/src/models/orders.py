import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import db

class Orders(db.Model):
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    weight_kg: Mapped[int] = mapped_column(sa.Integer, nullable=False)
    distance_km: Mapped[int] = mapped_column(sa.Integer, nullable=False)
    shipping_cost: Mapped[int] = mapped_column(sa.Integer, nullable=False)
    created_by: Mapped[int] = mapped_column(sa.Integer, nullable=False)
    created: Mapped[int] = mapped_column(sa.DateTime, nullable=False)

    points_of_sale_id: Mapped[int] = mapped_column(sa.ForeignKey("points_of_sale.id"))
    driver_id: Mapped[int] = mapped_column(sa.ForeignKey("driver.id"))
    vehicle_id: Mapped[int] = mapped_column(sa.ForeignKey("vehicle.id"))
    load_type_id: Mapped[int] = mapped_column(sa.ForeignKey("load_type.id"))
    status_id: Mapped[int] = mapped_column(sa.ForeignKey("status_type_for_orders.id"))
    
    points_of_sale: Mapped[list["Points_of_sale"]] = relationship(back_populates='orders')
    driver: Mapped[list["Driver"]] = relationship(back_populates='orders')
    vehicle: Mapped[list["Vehicle"]] = relationship(back_populates='orders')
    load_type: Mapped[list["Load_type"]] = relationship(back_populates='orders')
    status_type_for_orders: Mapped[list["Status_type_for_orders"]] = relationship(back_populates='orders')

    def __repr__(self) -> str:
        return f"Orders(id={self.id!r}, points_of_sale_id={self.points_of_sale_id!r}, weight_kg={self.weight_kg!r}, status_id={self.status_id!r})"