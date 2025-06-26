import os, json

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship
from cryptography.fernet import Fernet

from .base import db

key = os.getenv('SECRET_KEY').encode()
f = Fernet(key)


class Driver(db.Model):
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    cnh_encrypted: Mapped[str] = mapped_column(sa.String, nullable=False, unique=True)

    driver_status_id: Mapped[int] = mapped_column(sa.ForeignKey('driver_status.id'))
    user_id: Mapped[int] = mapped_column(sa.ForeignKey('user.id'))

    driver_status: Mapped["Driver_status"] = relationship(back_populates='driver')
    user: Mapped["User"] = relationship(back_populates='driver')
    vehicle: Mapped["Vehicle"] = relationship(back_populates='driver')
    orders: Mapped["Orders"] = relationship(back_populates='driver')
    
    # Deliver encrypted data to the database and return decrypted

    # cnh
    @property
    def cnh(self):
        descryptography = f.decrypt(self.cnh_encrypted.encode()).decode()
        json_converted = json.loads(descryptography)
        return json_converted
    
    @cnh.setter
    def cnh(self, value):
        if isinstance(value, dict):
            serialized = json.dumps(value)
            self.cnh_encrypted = f.encrypt(serialized.encode()).decode()
        else:
            raise ValueError("CNH must be a dictionary!")


    def __repr__(self) -> str:
        return f"Driver(id={self.id!r}, user_id={self.user_id!r}, cnh={self.cnh_encrypted!r})"