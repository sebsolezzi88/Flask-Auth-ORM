from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

class Users(db.Model):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)

    tareas: Mapped[list["Tareas"]] = relationship(back_populates="user", cascade="all, delete")


class Tareas(db.Model):
    __tablename__ = 'tareas'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    titulo: Mapped[str] = mapped_column(nullable=False)
    descripcion: Mapped[str] = mapped_column(nullable=True)
    fecha_creacion: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    user: Mapped[Users] = relationship(back_populates="tareas")
