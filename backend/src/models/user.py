import os

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship
from cryptography.fernet import Fernet

from .base import db

key = os.getenv('SECRET_KEY').encode()
f = Fernet(key)

class User(db.Model):
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    name_encrypted: Mapped[str] = mapped_column(sa.String, nullable=False, unique=True)
    cpf_encrypted: Mapped[str] = mapped_column(sa.String, nullable=False, unique=True)
    telephone_encrypted: Mapped[str] = mapped_column(sa.String, nullable=False)
    email_encrypted: Mapped[str] = mapped_column(sa.String, nullable=False, unique=True)
    email_hash: Mapped[str] = mapped_column(sa.String, nullable=False, unique=True)
    password: Mapped[str] = mapped_column(sa.String, nullable=False)

    role_id: Mapped[str] = mapped_column(sa.ForeignKey('role.id'))

    role: Mapped["Role"] = relationship(back_populates='user')
    driver: Mapped["Driver"] = relationship(back_populates='user')
    orders: Mapped[list["Orders"]] = relationship(back_populates='user')
    
    
    # Deliver encrypted data to the database and return decrypted    

    # name
    @property
    def name(self):
        return f.decrypt(self.name_encrypted.encode()).decode()
    
    @name.setter
    def name(self, value):
        self.name_encrypted = f.encrypt(value.encode()).decode()
        

    # cpf
    @property
    def cpf(self):
        return f.decrypt(self.cpf_encrypted.encode()).decode()
    
    @cpf.setter
    def cpf(self, value):
        self.cpf_encrypted = f.encrypt(value.encode()).decode()


    # telephone
    @property
    def telephone(self):
        return f.decrypt(self.telephone_encrypted.encode()).decode()
    
    @telephone.setter
    def telephone(self, value):
        self.telephone_encrypted = f.encrypt(value.encode()).decode()
    

    # email
    @property
    def email(self):
        return f.decrypt(self.email_encrypted.encode()).decode()
    
    @email.setter
    def email(self, value):
        self.email_encrypted = f.encrypt(value.encode()).decode()

        
    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name_encrypted!r}, role_id={self.role_id!r})"