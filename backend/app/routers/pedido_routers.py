from app.schemas.pedido_schema import PedidoCreate, PedidoRead, PedidoUpdate
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.models.pedido import Pedido

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])


@router.post("/", response_model=PedidoRead)
def criar_pedido(pedido: PedidoCreate, db: Session = Depends(get_db)):
    novo_pedido = Pedido(**pedido.dict())

    db.add(novo_pedido)
    db.commit()
    db.refresh(novo_pedido)

    return novo_pedido


@router.get("/")
def listar_pedidos(
    last_id: str | None = Query(None),
    limit: int = Query(50, le=100),
    status: str | None = None,
    db: Session = Depends(get_db)
):
    query = db.query(Pedido)

    if status:
        query = query.filter(Pedido.status == status)

    if last_id:
        query = query.filter(Pedido.id_pedido > last_id)

    result = query.order_by(Pedido.id_pedido).limit(limit).all()

    next_cursor = result[-1].id_pedido if result else None

    return {
        "data": result,
        "next_cursor": next_cursor
    }


@router.get("/{id_pedido}", response_model=PedidoRead)
def buscar_pedido(id_pedido: str, db: Session = Depends(get_db)):
    pedido = db.query(Pedido).filter(Pedido.id_pedido == id_pedido).first()

    if not pedido:
        raise HTTPException(
            status_code=404,
            detail="Pedido não encontrado"
        )

    return pedido


@router.put("/{id_pedido}", response_model=PedidoRead)
def atualizar_pedido(id_pedido: str, dados: PedidoUpdate, db: Session = Depends(get_db)):
    pedido = db.query(Pedido).filter(Pedido.id_pedido == id_pedido).first()

    if not pedido:
        raise HTTPException(
            status_code=404,
            detail="Pedido não encontrado"
        )

    for key, value in dados.dict(exclude_unset=True).items():
        setattr(pedido, key, value)

    db.commit()
    db.refresh(pedido)

    return pedido


@router.delete("/{id_pedido}")
def deletar_pedido(id_pedido: str, db: Session = Depends(get_db)):
    pedido = db.query(Pedido).filter(Pedido.id_pedido == id_pedido).first()

    if not pedido:
        raise HTTPException(
            status_code=404,
            detail="Pedido não encontrado"
        )

    db.delete(pedido)
    db.commit()

    return {"message": "Pedido deletado"}
