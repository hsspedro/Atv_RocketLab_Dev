from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

from app.database import Base


class Categoria(Base):
    __tablename__ = "categorias"

    nome_categoria: Mapped[str] = mapped_column(String(100), primary_key=True)
    link_imagem: Mapped[str] = mapped_column(String(500))
