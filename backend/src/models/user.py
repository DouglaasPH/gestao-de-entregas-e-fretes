import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import db

class User(db.Model):
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    name: Mapped[str] = mapped_column(sa.String, nullable=False, unique=True)
    cpf: Mapped[str] = mapped_column(sa.String, nullable=False, unique=True)
    telephone: Mapped[str] = mapped_column(sa.String, nullable=False)
    email: Mapped[str] = mapped_column(sa.String, nullable=False, unique=True)
    password: Mapped[str] = mapped_column(sa.String, nullable=False)

    role_id: Mapped[str] = mapped_column(sa.ForeignKey('role.id'))

    role: Mapped[list["Role"]] = relationship(back_populates='user')

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, role_id={self.role_id!r})"