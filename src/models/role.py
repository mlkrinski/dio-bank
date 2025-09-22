from sqlalchemy.orm import Mapped, mapped_column, relationship
import sqlalchemy as sa

from src.models.base import db


class Role(db.Model):
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    name: Mapped[str] = mapped_column(sa.String, nullable=False)
    user: Mapped[list["User"]] = relationship(back_populates="role")  # noqa

    def __repr__(self):
        return f"Role(id={self.id!r}, Name={self.name!r})"
