import os

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship
from cryptography.fernet import Fernet

from .base import db

key = os.getenv('SECRET_KEY').encode()
f = Fernet(key)
class Points_of_sale(db.Model):
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    cnpj_encrypted: Mapped[str] = mapped_column(sa.String, nullable=False, unique=True)
    telephone_encrypted: Mapped[str] = mapped_column(sa.String, nullable=False)
    address_encrypted: Mapped[str] = mapped_column(sa.String, nullable=False)

    orders: Mapped["Orders"] = relationship(back_populates='points_of_sale')



    # Deliver encrypted data to the database and return decrypted    

    # cnpj
    @property
    def cnpj(self):
        return f.decrypt(self.cnpj_encrypted.encode()).decode()
    
    @cnpj.setter
    def cnpj(self, value):
        self.cnpj_encrypted = f.encrypt(value.encode()).decode()

        
    # telephone
    @property
    def telephone(self):
        return f.decrypt(self.telephone_encrypted.encode()).decode()
    
    @telephone.setter
    def telephone(self, value):
        self.telephone_encrypted = f.encrypt(value.encode()).decode()
    
    
    # address
    @property
    def address(self):
        return f.decrypt(self.address_encrypted.encode()).decode()
    
    @address.setter
    def address(self, value):
        self.address_encrypted = f.encrypt(value.encode()).decode()


    def __repr__(self) -> str:
        return f"Points_of_sale(id={self.id!r}, cnpj={self.cnpj_encrypted!r}, telephone={self.telephone_encrypted!r}, address={self.address_encrypted!r})"