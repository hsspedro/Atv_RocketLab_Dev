from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Float, Column, Integer

from app.database import Base


class Produto(Base):
    __tablename__ = "produtos"

    id_produto: Mapped[str] = mapped_column(String(32), primary_key=True)
    nome_produto: Mapped[str] = mapped_column(String(255))
    categoria_produto: Mapped[str] = mapped_column(String(100))
    peso_produto_gramas: Mapped[Optional[float]
                                ] = mapped_column(Float, nullable=True)
    comprimento_centimetros: Mapped[Optional[float]
                                    ] = mapped_column(Float, nullable=True)
    altura_centimetros: Mapped[Optional[float]
                               ] = mapped_column(Float, nullable=True)
    largura_centimetros: Mapped[Optional[float]
                                ] = mapped_column(Float, nullable=True)
    preco_BRL: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    media_avaliacoes = Column(Float, default=0.0)
    total_avaliacoes = Column(Integer, default=0)
