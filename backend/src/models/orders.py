import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import db

class Orders(db.Model):
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    weight_kg: Mapped[int] = mapped_column(sa.Integer, nullable=False)
    distance_km: Mapped[int] = mapped_column(sa.Integer, nullable=False)
    shipping_cost: Mapped[int] = mapped_column(sa.Integer, nullable=False)
    created: Mapped[int] = mapped_column(sa.DateTime, nullable=False)

    points_of_sale_id: Mapped[int] = mapped_column(sa.ForeignKey("points_of_sale.id"), nullable=False)
    driver_id: Mapped[int] = mapped_column(sa.ForeignKey("driver.id"), nullable=False)
    vehicle_id: Mapped[int] = mapped_column(sa.ForeignKey("vehicle.id"), nullable=False)
    load_type_id: Mapped[int] = mapped_column(sa.ForeignKey("load_type.id"), nullable=False)
    order_status_id: Mapped[int] = mapped_column(sa.ForeignKey("orders_status.id"), nullable=False)
    created_by: Mapped[int] = mapped_column(sa.ForeignKey("user.id"), nullable=False)
    
    points_of_sale: Mapped["Points_of_sale"] = relationship(back_populates='orders')
    driver: Mapped["Driver"] = relationship(back_populates='orders')
    vehicle: Mapped["Vehicle"] = relationship(back_populates='orders')
    load_type: Mapped["Load_type"] = relationship(back_populates='orders')
    orders_status: Mapped["Orders_status"] = relationship(back_populates='orders')
    user: Mapped["User"] = relationship(back_populates='orders')

    def __repr__(self) -> str:
        return f"Orders(id={self.id!r}, points_of_sale_id={self.points_of_sale_id!r}, weight_kg={self.weight_kg!r}, order_status_id={self.order_status_id!r})"